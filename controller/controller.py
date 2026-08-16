import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Dict

import lxml.etree as ET

import model.vsqx_convert as vsqx_convert
from config.setting import BASE_DIR, get_convert_list_data
from controller.errorController import (
    ConversionError,
    ConversionExecutionError,
    ConvertListError,
    VSQXFileReadError,
)

'''
todo:
update 2026-08-05
    1. [ ] 변환 리스트 파일 경로를 고정된 주소가 아니라 외부에서 지정 가능하도록 개선
    2. [X] 오류 처리 개선
    3. [X] 로깅 파일 추가
'''

logger = logging.getLogger(__name__)

LIST_DIR = BASE_DIR / "list"
CONVERT_JSON_PATH = LIST_DIR / "convert.json"


class Controller:
    convert_path: str | Path
    convert_type: str

    def __init__(self, from_lang: str, to_lang: str, convert_path: str | Path = CONVERT_JSON_PATH) -> None:
        self.convert_type = f"{from_lang}To{to_lang}"
        self.convert_path = convert_path

    def _get_convert_list_data(self, type: str | None = None) -> Dict[str, Dict[str, str]] | None:
        if type is None:
            type = self.convert_type

        try:
            logger.info(f"변환 리스트 읽기 시작: {self.convert_path}")
            return get_convert_list_data(type, self.convert_path)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
            raise ConvertListError(f"변환 규칙 로드 실패: {self.convert_path} ({type})") from error

    def _get_vsqx_file(self, vsqx_file: str) -> ET._ElementTree:
        try:
            with open(vsqx_file, "rb") as f:
                logger.info(f"VSQX 파일 읽기 시작: {vsqx_file}")
                return ET.parse(f, parser=ET.XMLParser(strip_cdata=False, recover=True))
        except FileNotFoundError as error:
            raise VSQXFileReadError(f"VSQX 파일을 찾을 수 없습니다: {vsqx_file}") from error
        except PermissionError as error:
            raise VSQXFileReadError(f"VSQX 파일 접근 권한이 없습니다: {vsqx_file}") from error
        except (OSError, ET.XMLSyntaxError) as error:
            raise VSQXFileReadError(f"VSQX 파일 형식이 올바르지 않습니다: {vsqx_file}") from error

    def _build_output_path(self, vsqx_file_name: str) -> str:
        output_path = vsqx_file_name.replace(".vsqx", "_updated.vsqx")
        if Path(output_path).exists():
            original_path = Path(output_path)
            stem = original_path.stem
            suffix = original_path.suffix
            counter = 1
            while True:
                candidate = str(original_path.with_name(f"{stem}_{counter}{suffix}"))
                if not Path(candidate).exists():
                    return candidate
                counter += 1
        return output_path

    def convert(self, vsqx_file_name: str) -> None:
        try:
            logger.info(f"파일 변환 준비: {vsqx_file_name}")
            vsqx_file: ET._ElementTree = self._get_vsqx_file(vsqx_file_name)
            convert_file: Dict[str, Dict[str, str]] | None = self._get_convert_list_data(self.convert_type)

            if not convert_file:
                raise ConvertListError(f"변환 규칙이 비어 있습니다: {self.convert_type}")

            converter: vsqx_convert.VsqxConverter = vsqx_convert.VsqxConverter(vsqx_file, convert_file)
            converted_data: bytes = converter.convert(vsqx_file)

            output_path = self._build_output_path(vsqx_file_name)
            with open(output_path, "wb") as f_out:
                f_out.write(converted_data)
            logger.info(f"파일 변환 성공: {vsqx_file_name} -> {output_path}")
        except (ConvertListError, VSQXFileReadError, ConversionError) as error:
            logger.exception(f"변환 실패: {vsqx_file_name}")
            raise ConversionExecutionError(f"변환 처리 실패: {vsqx_file_name}: {error}") from error
        except OSError as error:
            logger.exception(f"출력 파일 저장 실패: {vsqx_file_name}")
            raise ConversionExecutionError(f"변환 결과 저장 실패: {vsqx_file_name}: {error}") from error

    def multi_convert(
        self,
        vsqx_file_name: tuple[str, ...],
        OnFinish: Callable[[int, int, list[tuple[str, str]]], None],
    ) -> None:
        thread = threading.Thread(target=self._background_convert_task, args=(vsqx_file_name, OnFinish), daemon=True)
        thread.start()

    def _background_convert_task(
        self,
        vsqx_file_names: tuple[str, ...],
        OnFinish: Callable[[int, int, list[tuple[str, str]]], None],
    ) -> None:
        vsqx_file_names = tuple(dict.fromkeys(vsqx_file_names))
        fail = 0
        success = 0
        failed_files: list[tuple[str, str]] = []

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {executor.submit(self.convert, file): file for file in vsqx_file_names}
            for future in as_completed(futures):
                file = futures[future]
                try:
                    future.result()
                    success += 1
                    logger.info(f"파일 변환 성공: {file}")
                except Exception as error:
                    fail += 1
                    failed_files.append((file, str(error)))
                    logger.error(f"파일 처리 중 오류가 발생했습니다: {file}: {error}")

        if OnFinish:
            OnFinish(fail, success, failed_files)