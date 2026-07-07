import controller
import tkinter as tk
import tkinter.filedialog as filedialog
from typing import Literal

class VsqxConverterGUI:
    window: tk.Tk

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("VSQX Converter")
        self.window.geometry("400x200+400+200")
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self) -> None:
        tk.Button(self.window, text="Japanese to Korean", command=lambda: self.file_dialog("jpnTokor")).pack(pady=10)

    def file_dialog(self, type: str) -> None:
        file_path: tuple[str, ...] | Literal[""] = filedialog.askopenfilenames(
            filetypes=[("VSQX files", "*.vsqx")]
        )
        if file_path:
            for file in file_path:
                controller.Controller(file, type).convert()


gui = VsqxConverterGUI()
