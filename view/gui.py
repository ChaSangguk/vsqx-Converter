from controller.controller import Controller
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
from typing import Literal
import logging
from config.setting import load_lang_list

'''todo:
update 2026-07-29
- [ ] GUI 개선
- [ ] i18n 지원
- [ ] 파일 처리 중 오류 발생시 어떤 파일에서 오류가 발생했는지 표시
- [X] 변환 완료시 어떤 파일이 변환되었는지 표시
- [ ] 변환 중 로딩바 표시
- [ ] 변환 완료시 저장 위치 표시
- [ ] 변환 완료시 저장 위치 변경 가능하도록 개선
- [X] 멀티 스레딩 기반 비동기 처리로 GUI 멈춤 방지
'''
logger = logging.getLogger(__name__)
class VsqxConverterGUI:
    window: tk.Tk

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("VSQX Converter")
        self.window.geometry(f"{self.window.winfo_screenwidth() // 2}x{self.window.winfo_screenheight() // 2}")
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self) -> None:
        logger.info("GUI 위젯 생성 시작")
        lang_list = load_lang_list()
        tk.Label(self.window, text="출발 언어").pack(pady=5)
        self.from_lang_var = tk.StringVar(value=lang_list[0][0])
        ttk.Combobox(self.window, textvariable=self.from_lang_var, values=lang_list[0], state="readonly").pack(pady=5)
        tk.Label(self.window, text="도착 언어").pack(pady=5)
        self.to_lang_var = tk.StringVar(value=lang_list[1][0])
        ttk.Combobox(self.window, textvariable=self.to_lang_var, values=lang_list[1], state="readonly").pack(pady=5)
        tk.Button(self.window, text="파일 선택", command=lambda: self.file_dialog(self.from_lang_var.get(),self.to_lang_var.get())).pack(pady=5)
    def file_dialog(self, from_lang: str, to_lang: str) -> None:
        file_path: tuple[str, ...] | Literal[""] = filedialog.askopenfilenames(
            filetypes=[("VSQX 파일", "*.vsqx")]
        )
        controller = Controller(from_lang,to_lang)
        if not file_path:
            logger.info("파일 선택 취소")
            return
        file_path = tuple(dict.fromkeys(file_path))  # 중복 제거
        logger.info(f"선택된 파일: {file_path}")
        controller.multi_convert(file_path, self.on_convert_finish)

    def on_convert_finish(self, fail: int, success: int, failed_files: list[str]) -> None:
        logger.info(f"성공 : {success}, 실패 : {fail}")
        f = '\n'.join(failed_files)
        if failed_files:
            logger.info(f"실패한 파일: {failed_files}")
        self.window.after(0, lambda: messagebox.showinfo("완료", f"변환이 완료되었습니다. 실패: {fail}, 성공: {success} {f}"))