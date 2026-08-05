import json
from typing import Dict

import lxml.etree as ET
import model.vsqx_convert as vsqx_convert
from config.setting import get_convert_list_data
from controller.error_controller import ErrorController
import logging
'''
todo:
update 2026-08-05
    1. [ ] 변환 리스트 파일 경로를 고정된 주소가 아니라 외부에서 지정 가능하도록 개선
    2. [X] 오류 처리 개선
    3. [X] 로깅 파일 추가
'''
logger = logging.getLogger(__name__)
class Controller:
    convert_path: str
    def __init__(self, convert_type: str, convert_path: str = "list/convert.json") -> None:
        self.convert_type: str = convert_type
        self.convert_path = convert_path
        self.error_controller = ErrorController()

    def _get_convert_list_data(self, type: str | None = None) -> Dict[str, Dict[str, str]]:
        if type is None:
            type = self.convert_type
        try:
            logger.info(f"변환 리스트 읽기 시작: {self.convert_path}")
            return get_convert_list_data(type, self.convert_path)
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as error:
            logger.error(f"변환 리스트 읽기 중 오류가 발생했습니다: {error}")
            self.error_controller.raise_error(error, "변환 리스트 읽기")
            raise AssertionError("unreachable")

    def _get_vsqx_file(self,vsqx_file: str) -> ET._ElementTree:
        try:
            with open(vsqx_file, "rb") as f:
                logger.info(f"VSQX 파일 읽기 시작: {vsqx_file}")
                return ET.parse(f, parser=ET.XMLParser(strip_cdata=False, recover=True))
        except (FileNotFoundError, ET.XMLSyntaxError) as error:
            logger.error(f"VSQX 파일 읽기 중 오류가 발생했습니다: {error}")
            self.error_controller.raise_error(error, "VSQX 파일 읽기")
            raise AssertionError("unreachable")

    def convert(self, vsqx_file_name: str) -> None:
        try:
            logger.info(f"파일 변환 준비: {vsqx_file_name}")
            vsqx_file = self._get_vsqx_file(vsqx_file_name)
            convert_file: Dict[str, Dict[str, str]] = self._get_convert_list_data(self.convert_type)

            converter: vsqx_convert.VsqxConverter = vsqx_convert.VsqxConverter(vsqx_file, convert_file)
            f: bytes = converter.convert(vsqx_file)
            with open(vsqx_file_name.replace('.vsqx', '_updated.vsqx'), "wb") as f_out:
                f_out.write(f)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, ET.XMLSyntaxError) as error:
            logger.error(f"파일 처리 중 오류가 발생했습니다: {error}")
            self.error_controller.raise_error(error, "변환 처리")