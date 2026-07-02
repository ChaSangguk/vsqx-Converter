import json
import lxml
from lxml import etree
'''
vsqx 파일 내 vstrack, vspart, note내 <p> 값을 파싱하여 미리 준비된 리스트에 따라 변환후 저장
'''
class VsqxConverter:
    def __init__(self, vsqx_file, convert_list):
        self.vsqx_file = vsqx_file
        self.convert_list = convert_list
        self.list_data = json.load(open(self.convert_list))
    def _get_list_data(self, type):
        return self.list_data.get(type)
    def _get_vsqx_data(self):
        # vsqx 파일을 파싱하여 필요한 데이터를 추출하는 로직을 구현
        return etree.parse(self.vsqx_file,parser=etree.XMLParser(strip_cdata=False, recover=True))
    def convert(self, type):
        convert_list = self._get_list_data(type)
        vsqx_data = self._get_vsqx_data()
        root = vsqx_data.getroot()
        ns = {"v4": "http://www.yamaha.co.jp/vocaloid/schema/vsq4/"}
        for note in root.findall(".//v4:note/v4:p", namespaces=ns):
            origin_note = note.text
            print(f"Original note: {origin_note}")
            result = ''
            for n in origin_note.split():
                if n in convert_list:
                    result += convert_list[n]
                else:
                    result += n
            print(f"Converted note: {result}")
            note.text = etree.CDATA(result)
        return etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True)
        '''
        with open(self.vsqx_file.replace('.vsqx', '_updated.vsqx'), "wb") as f:
            f.write(etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True))
        '''


if __name__ == "__main__":
    vsqx_file = "test/test.vsqx"
    convert_list = "list/convert.json"
    converter = VsqxConverter(vsqx_file, convert_list)
    converter.convert("jtk")
