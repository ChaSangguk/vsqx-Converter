import json
from functools import lru_cache
from typing import Any, Dict
import logging
from os import path

__version__ = "0.9.9"
logger = logging.getLogger(__name__)

def read_json_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

@lru_cache(maxsize=32)
def get_convert_list_data(convert_type: str, convert_path: str = "list/convert.json") -> Dict[str, Dict[str, str]]:
    logger.info(f"변환 리스트 데이터 가져오기: {convert_type} from {convert_path}")
    list_data = read_json_file(convert_path)
    convert_entry = list_data.get(convert_type)
    if convert_entry is None:
        logger.error(f"변환 유형을 찾을 수 없습니다: {convert_type}")
        raise KeyError(convert_type)

    if isinstance(convert_entry, str):
        file_path = convert_entry
    elif isinstance(convert_entry, dict):
        file_path = convert_entry.get("path")
        if file_path is None:
            logger.error(f"변환 유형 {convert_type}에 path 필드가 없습니다.")
            raise KeyError("path")
    else:
        logger.error(f"변환 리스트 항목 형식이 올바르지 않습니다: {convert_type}")
        raise TypeError("convert list entry must be a string path or an object containing path")

    logger.info(f"변환 리스트 데이터 로드 완료: {file_path}")
    return read_json_file(file_path)

def load_lang_list(file_path: str = "list/convert.json") -> list[list[str]]:
    logger.info(f"언어 리스트 데이터 가져오기 from {file_path}")
    data = read_json_file(file_path)
    return [list(dict.fromkeys(item['from'] for item in data.values())), list(dict.fromkeys(item['to'] for item in data.values()))]
