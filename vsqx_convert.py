import json
from lxml import etree
'''
vsqx 파일 내 vstrack, vspart, note내 <p> 값을 파싱하여 미리 준비된 리스트에 따라 변환후 저장
'''
class VsqxConverter:
    def __init__(self, vsqx_file = None, convert_file = None):
        self.vsqx_file = vsqx_file
        self.convert_file = convert_file
    def convert(self, vsqx_file = None, convert_file = None):
        if vsqx_file is None:
            vsqx_file = self.vsqx_file
        if convert_file is None:
            convert_file = self.convert_file
        assert vsqx_file is not None, "vsqx_file is required"
        assert convert_file is not None, "convert_file is required"
        root = vsqx_file.getroot()
        ns = {"v4": "http://www.yamaha.co.jp/vocaloid/schema/vsq4/"}
        for note in root.findall(".//v4:note/v4:p", namespaces=ns):
            origin_note = note.text
            result = []
            if origin_note is None:
                continue
            for n in origin_note.split():
                if n in convert_file:
                    result.append(convert_file[n])
                else:
                    result.append(n)
            note.set("lock", "1")
            note.text = etree.CDATA(' '.join(result))
        return etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True)
        '''
        with open(self.vsqx_file.replace('.vsqx', '_updated.vsqx'), "wb") as f:
            f.write(etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True))
        '''

