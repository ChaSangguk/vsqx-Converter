import json
from typing import Dict

import lxml.etree as ET
import vsqx_convert
from controller.error_controller import ErrorController
import logging
'''
todo:
update 2026-07-29
    1. [ ] 변환 리스트 파일 경로를 고정된 주소가 아니라 외부에서 지정 가능하도록 개선
    2. [ ] 오류 처리 개선
    3. [ ] 로깅 파일 추가
'''
logger = logging.getLogger(__name__)
class Controller:
    convert_path: str

    def __init__(self, vsqx_file: str, convert_type: str, convert_path: str = "list/convert.json") -> None:
        self.vsqx_file: str = vsqx_file
        self.convert_type: str = convert_type
        self.convert_path = convert_path
        self.error_controller = ErrorController()

    def _get_convert_list_data(self, type: str | None = None) -> Dict[str, Dict[str, str]]:
        if type is None:
            type = self.convert_type
        try:
            logger.info(f"변환 리스트 읽기 시작: {self.convert_path}")
            with open(self.convert_path, "r", encoding="utf-8") as f:
                list_data: Dict[str, str] = json.load(f)

            file_path: str | None = list_data.get(type)
            if file_path is None:
                raise KeyError(type)

            with open(file_path, "r", encoding="utf-8") as convert_f:
                return json.load(convert_f)
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as error:
            logger.error(f"변환 리스트 읽기 중 오류가 발생했습니다: {error}")
            self.error_controller.raise_error(error, "변환 리스트 읽기")
            raise AssertionError("unreachable")

    def _get_vsqx_file(self) -> ET._ElementTree:
        try:
            with open(self.vsqx_file, "rb") as f:
                logger.info(f"VSQX 파일 읽기 시작: {self.vsqx_file}")
                return ET.parse(f, parser=ET.XMLParser(strip_cdata=False, recover=True))
        except (FileNotFoundError, ET.XMLSyntaxError) as error:
            logger.error(f"VSQX 파일 읽기 중 오류가 발생했습니다: {error}")
            self.error_controller.raise_error(error, "VSQX 파일 읽기")
            raise AssertionError("unreachable")

    def convert(self) -> None:
        try:
            logger.info(f"파일 변환시작: {self.vsqx_file}")
            vsqx_file = self._get_vsqx_file()
            convert_file: Dict[str, Dict[str, str]] = self._get_convert_list_data(self.convert_type)

            converter: vsqx_convert.VsqxConverter = vsqx_convert.VsqxConverter(vsqx_file, convert_file)
            f: bytes = converter.convert(vsqx_file)
            with open(self.vsqx_file.replace('.vsqx', '_updated.vsqx'), "wb") as f_out:
                f_out.write(f)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, ET.XMLSyntaxError) as error:
            logger.error(f"파일 처리 중 오류가 발생했습니다: {error}")
            self.error_controller.raise_error(error, "변환 처리")