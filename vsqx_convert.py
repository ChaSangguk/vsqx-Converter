import json
from lxml import etree
'''
vsqx 파일 내 vstrack, vspart, note내 <p> 값을 파싱하여 미리 준비된 리스트에 따라 변환후 저장
'''
class VsqxConverter:
    def __init__(self, vsqx_file, convert_list):
        self.vsqx_file = vsqx_file
        self.convert_list = convert_list
        self.list_data = json.load(open(self.convert_list))
    def convert(self, convert_file, vsqx_file):
        root = vsqx_file.getroot()
        ns = {"v4": "http://www.yamaha.co.jp/vocaloid/schema/vsq4/"}
        for note in root.findall(".//v4:note/v4:p", namespaces=ns):
            origin_note = note.text
            result = []
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

