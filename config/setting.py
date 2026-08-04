import json
from functools import lru_cache
from typing import Any, Dict


def read_json_file(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=32)
def get_convert_list_data(convert_type: str, convert_path: str = "list/convert.json") -> Dict[str, Dict[str, str]]:
    list_data = read_json_file(convert_path)
    file_path = list_data.get(convert_type)
    if file_path is None:
        raise KeyError(convert_type)

    return read_json_file(file_path)
