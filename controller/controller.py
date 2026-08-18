import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

from config.setting import BASE_DIR
from controller.errorController import ConversionExecutionError
from model.conversion_request import ConversionRequest
from service.conversion_service import VsqxConversionService

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
        self.service = VsqxConversionService(convert_path=convert_path)

    def convert(self, vsqx_file_name: str) -> None:
        request = ConversionRequest(
            file_path=vsqx_file_name,
            convert_type=self.convert_type,
            convert_path=self.convert_path,
        )
        result = self.service.convert_file(request)
        if not result.success:
            raise ConversionExecutionError(result.error_message or f"변환 처리 실패: {vsqx_file_name}")

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
        requests = [
            ConversionRequest(
                file_path=file,
                convert_type=self.convert_type,
                convert_path=self.convert_path,
            )
            for file in vsqx_file_names
        ]

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {executor.submit(self.service.convert_file, request): request.file_path for request in requests}
            failed_files: list[tuple[str, str]] = []
            success = 0
            fail = 0

            for future in as_completed(futures):
                file = futures[future]
                try:
                    result = future.result()
                    if result.success:
                        success += 1
                        logger.info(f"파일 변환 성공: {file}")
                    else:
                        fail += 1
                        failed_files.append((str(file), result.error_message or "알 수 없는 오류"))
                        logger.error(f"파일 처리 중 오류가 발생했습니다: {file}: {result.error_message}")
                except Exception as error:
                    fail += 1
                    failed_files.append((str(file), str(error)))
                    logger.error(f"파일 처리 중 오류가 발생했습니다: {file}: {error}")

        if OnFinish:
            OnFinish(fail, success, failed_files)