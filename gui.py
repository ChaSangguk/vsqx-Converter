import controller
import tkinter as tk
import tkinter.filedialog as filedialog

class VsqxConverterGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("VSQX Converter")
        self.window.geometry("400x200+400+200")
        self.create_widgets()
        self.window.mainloop()
    def create_widgets(self):
        tk.Button(self.window, text="Japanese to Korean", command=lambda: self.file_dialog("jpnTokor")).pack(pady=10)

        pass
    def file_dialog(self,type):
        file_path = filedialog.askopenfilenames(filetypes=[("VSQX files", "*.vsqx")])
        if file_path:
            for file in file_path:
                controller.Controller(file, type).convert()
        
gui = VsqxConverterGUI()
