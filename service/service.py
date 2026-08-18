from pathlib import Path
import model.vsqx_convert
import logging
import json
import lxml.etree as ET
from config.setting import get_convert_list_data
from controller.errorController import *
logger = logging.getLogger(__name__)

class VsqxDataService:
    def __init__(self, type_name: str, convert_path: str | Path):
        self.convert_path = Path(convert_path)
        self.type_name = type_name
class service :
    def __init__(self, name, path):
        self.data = VsqxDataService(name,path)
        pass
    def get_convert_list_data(self, type: str) -> Dict[str, Dict[str, str]] | None:
        try:
            logger.info(f"변환 리스트 읽기 시작: {self.data.convert_path}")
            return get_convert_list_data(type, self.data.convert_path)
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as error:
            raise ConvertListError(f"변환 규칙 로드 실패: {self.convert_path} ({type})") from error

    def get_vsqx_file(self, vsqx_file: str) -> ET._ElementTree:
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
    