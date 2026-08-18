from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Sequence

import lxml.etree as ET

import model.vsqx_convert as vsqx_convert
from config.setting import get_convert_list_data
from controller.errorController import ConvertListError, VSQXFileReadError
from model.conversion_request import ConversionRequest
from model.conversion_result import BatchConversionResult, ConversionResult

logger = logging.getLogger(__name__)


class VsqxConversionService:
    def __init__(self, convert_path: str | Path | None = None) -> None:
        self.convert_path = Path(convert_path) if convert_path is not None else None

    def load_conversion_map(
        self,
        convert_type: str,
        convert_path: str | Path | None = None,
    ) -> dict[str, dict[str, str]]:
        target_path = self.convert_path if convert_path is None else Path(convert_path)
        try:
            logger.info(f"변환 리스트 읽기 시작: {target_path}")
            return get_convert_list_data(convert_type, target_path)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
            raise ConvertListError(f"변환 규칙 로드 실패: {target_path} ({convert_type})") from error

    def read_vsqx_file(self, vsqx_file: str | Path) -> ET._ElementTree:
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

    def _build_output_path(self, vsqx_file_name: str | Path) -> str:
        output_path = str(vsqx_file_name).replace(".vsqx", "_updated.vsqx")
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

    def convert_file(self, request: ConversionRequest) -> ConversionResult:
        try:
            logger.info(f"파일 변환 준비: {request.file_path}")
            convert_map = self.load_conversion_map(request.convert_type, request.convert_path)
            if not convert_map:
                raise ConvertListError(f"변환 규칙이 비어 있습니다: {request.convert_type}")

            vsqx_file = self.read_vsqx_file(request.file_path)
            converter = vsqx_convert.VsqxConverter(vsqx_file, convert_map)
            converted_data = converter.convert(vsqx_file)

            output_path = self._build_output_path(request.file_path)
            with open(output_path, "wb") as f_out:
                f_out.write(converted_data)

            logger.info(f"파일 변환 성공: {request.file_path} -> {output_path}")
            return ConversionResult(file_path=request.file_path, success=True, output_path=output_path)
        except (ConvertListError, VSQXFileReadError) as error:
            logger.exception(f"변환 실패: {request.file_path}")
            return ConversionResult(file_path=request.file_path, success=False, error_message=str(error))
        except OSError as error:
            logger.exception(f"출력 파일 저장 실패: {request.file_path}")
            return ConversionResult(
                file_path=request.file_path,
                success=False,
                error_message=f"변환 결과 저장 실패: {request.file_path}: {error}",
            )

    def convert_batch(self, requests: Sequence[ConversionRequest]) -> BatchConversionResult:
        results = [self.convert_file(request) for request in requests]
        return BatchConversionResult(results=results)
