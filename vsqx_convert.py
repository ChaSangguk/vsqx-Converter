from __future__ import annotations
from typing import Dict
from lxml import etree # type: ignore
'''
vsqx 파일 내 vstrack, vspart, note내 <p> 값을 파싱하여 미리 준비된 리스트에 따라 변환후 저장
'''
''' 
todo :
update 2026-07-29
    1. [X] 파일 종류에 따라 namespace를 범용적으로 사용가능하게 수정
    2. [ ] 단위 테스트 추가
'''
class VsqxConverter:
    vsqx_file: etree._ElementTree | None
    convert_file: Dict[str, Dict[str, str]] | None

    def __init__(self, vsqx_file: etree._ElementTree | None = None, convert_file: Dict[str, Dict[str, str]] | None = None) -> None:
        self.vsqx_file = vsqx_file
        self.convert_file = convert_file

    def convert(self, vsqx_file: etree._ElementTree | None = None, convert_file: Dict[str, Dict[str, str]] | None = None) -> bytes:
        if vsqx_file is None:
            vsqx_file = self.vsqx_file
        if convert_file is None:
            convert_file = self.convert_file

        assert vsqx_file is not None, "vsqx_file is required"
        assert convert_file is not None, "convert_file is required"

        root: etree._Element = vsqx_file.getroot()
        ns_uri: Dict[str, str] = root.nsmap
        for (NS, uri) in ns_uri.items():
            if NS is None:
                path = ".//ns0:note/ns0:p"
                NS = "ns0"
            else:
                path = f".//{NS}:note/{NS}:p"
            for note in root.findall(path, namespaces={NS : uri}):
                origin_note: str | None = note.text
                if origin_note is None:
                    continue
                result: list[str] = []
                for i in convert_file["multiple"]:
                    if i not in origin_note:
                        continue
                    origin_note = origin_note.replace(i, convert_file["multiple"][i])
                for n in origin_note.split():
                    if n in convert_file["singular"]:
                        result.append(convert_file["singular"][n])
                    else:
                        result.append(n)
                note.set("lock", "1")
                note.text = etree.CDATA(" ".join(result))
        return etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True)