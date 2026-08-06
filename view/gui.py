from controller.controller import Controller
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from typing import Literal
import logging

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
        self.window.geometry("120x240")
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self) -> None:
        logger.info("GUI 위젯 생성 시작")
        # todo - 출발 드롭박스 도착 드롭박스 이 형태로 변경
        tk.Button(self.window, text="Japanese to English", command=lambda: self.file_dialog("jpnToeng")).pack(pady=10)
        tk.Button(self.window, text="Japanese to Korean", command=lambda: self.file_dialog("jpnTokor")).pack(pady=10)
        tk.Button(self.window, text="Korean to Japanese", command=lambda: self.file_dialog("korTojpn")).pack(pady=10)

    def file_dialog(self, type: str) -> None:
        file_path: tuple[str, ...] | Literal[""] = filedialog.askopenfilenames(
            filetypes=[("VSQX 파일", "*.vsqx")]
        )
        controller = Controller(type)
        if not file_path:
            logger.info("파일 선택 취소")
            return
        
        controller.multi_convert(file_path, self.on_convert_finish)

    def on_convert_finish(self, fail: int, success: int) -> None:
        logger.info(f"성공 : {success}, 실패 : {fail}")
        messagebox.showinfo("완료", f"변환이 완료되었습니다. 실패: {fail}, 성공: {success}")