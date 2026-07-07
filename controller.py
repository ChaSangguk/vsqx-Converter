import json
from typing import Dict, Optional

import lxml.etree as ET
import vsqx_convert

class Controller:
    convert_path: str

    def __init__(self, vsqx_file: str, convert_type: str) -> None:
        self.vsqx_file: str = vsqx_file
        self.convert_type: str = convert_type
        self.convert_path = "list/convert.json"
    def _get_convert_list_data(self, type: Optional[str] = None) -> Dict[str, str]:
        if type is None:
            type = self.convert_type
        with open(self.convert_path, "r", encoding="utf-8") as f:
            list_data: Dict[str, str] = json.load(f)

        file_path: Optional[str] = list_data.get(type)
        if file_path is None:
            raise ValueError("타입 오류")

        with open(file_path, "r", encoding="utf-8") as convert_f:
            return json.load(convert_f)
    
    def _get_vsqx_file(self) -> ET._ElementTree:
        with open(self.vsqx_file, "rb") as f:
            return ET.parse(f, parser=ET.XMLParser(strip_cdata=False, recover=True))

    def convert(self) -> None:
        vsqx_file = self._get_vsqx_file()
        try:
            convert_file: Dict[str, str] = self._get_convert_list_data(self.convert_type)
        except ValueError as e:
            print(f"Error: {e}")
            return
        converter: vsqx_convert.VsqxConverter = vsqx_convert.VsqxConverter(vsqx_file, convert_file)
        f: bytes = converter.convert(vsqx_file)
        with open(self.vsqx_file.replace('.vsqx', '_updated.vsqx'), "wb") as f_out:
            f_out.write(f)