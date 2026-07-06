import vsqx_convert
typelist = ['korTojpn', 'jpnTokor']
class Controller:
    def __init__(self,file,type):
        self.file = file
        self.type = type
    def convert(self):
        converter = vsqx_convert.VsqxConverter(self.file, "list/convert.json")
        converter.convert(self.type)



