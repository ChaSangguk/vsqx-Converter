import controller
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from typing import Literal

class VsqxConverterGUI:
    window: tk.Tk

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("VSQX Converter")
        self.window.geometry("120x120")
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self) -> None:
        tk.Button(self.window, text="Japanese to Korean", command=lambda: self.file_dialog("jpnTokor")).pack(pady=10)
        tk.Button(self.window, text="Korean to Japanese", command=lambda: self.file_dialog("korTojpn")).pack(pady=10)

    def file_dialog(self, type: str) -> None:
        file_path: tuple[str, ...] | Literal[""] = filedialog.askopenfilenames(
            filetypes=[("VSQX 파일", "*.vsqx")]
        )
        if file_path:
            for file in file_path:
                try:
                    controller.Controller(file, type).convert()
                except ValueError as e:
                    messagebox.showerror("오류", f"파일 처리 중 오류가 발생했습니다: {e}")
            messagebox.showinfo("완료", "변환이 완료되었습니다.")


gui = VsqxConverterGUI()
