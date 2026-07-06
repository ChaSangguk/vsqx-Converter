import vsqx_convert
import lxml.etree as ET
import json

class Controller:
    def __init__(self,vsqx_file,convert_type):
        self.vsqx_file = vsqx_file
        self.convert_type = convert_type
        self.convert_path = "list/convert.json"
    def _get_convert_list_data(self,type):
        with open(self.convert_path, "r") as f:
            list_data = json.load(f)
            if type in list_data:
                return json.load(open(list_data.get(type)+".json"))
            else:
                raise ValueError("타입 오류")
    
    def _get_vsqx_file(self):
        with open(self.vsqx_file, "rb") as f:
            return ET.parse(f, parser=ET.XMLParser(strip_cdata=False, recover=True))
    def convert(self):
        vsqx_file = self._get_vsqx_file()
        try :
            convert_file = self._get_convert_list_data(self.convert_path)
        except ValueError as e:
            print(f"Error: {e}")
            return
        converter = vsqx_convert.VsqxConverter(vsqx_file, convert_file)
        f = converter.convert(convert_file, vsqx_file)
        with open(self.vsqx_file.replace('.vsqx', '_updated.vsqx'), "wb") as f_out:
            f_out.write(f)



