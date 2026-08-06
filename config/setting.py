import json
from functools import lru_cache
from typing import Any, Dict
import logging

__version__ = "0.9.8"
logger = logging.getLogger(__name__)

def read_json_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=32)
def get_convert_list_data(convert_type: str, convert_path: str = "list/convert.json") -> Dict[str, Dict[str, str]]:
    logger.info(f"변환 리스트 데이터 가져오기: {convert_type} from {convert_path}")
    list_data = read_json_file(convert_path)
    file_path = list_data.get(convert_type)
    if file_path is None:
        logger.error(f"변환 유형을 찾을 수 없습니다: {convert_type}")
        raise KeyError(convert_type)

    logger.info(f"변환 리스트 데이터 로드 완료: {file_path}")
    return read_json_file(file_path)
