import json
import fileinput
'''
vsqx 파일 내 vstrack, vspart, note내 <p> 값을 파싱하여 미리 준비된 리스트에 따라 변환후 저장
'''
class VsqxConverter:
    def __init__(self, vsqx_file, convert_list):
        self.vsqx_file = vsqx_file
        self.convert_list = convert_list
        self.list_data = json.load(open(self.convert_list))
    def _get_list_data(self, type):
        return self.list_data.get(type, [])
    def convert(self, type):
        convert_list = self._get_list_data(type)
        with fileinput.FileInput(self.vsqx_file, inplace=True) as file:
            for line in file:
                pass




if __name__ == "__main__":
    vsqx_file = "test/test.vsqx"
    convert_list = "list/convert.json"
    converter = VsqxConverter(vsqx_file, convert_list)
    converter.convert("ktj")
