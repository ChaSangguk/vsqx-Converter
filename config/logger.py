import logging
import datetime
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "log"
def set_logger():
    ''' 로거 설정 함수'''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return
    os.makedirs(LOG_DIR, exist_ok=True)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(LOG_DIR / f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log", encoding='utf-8')

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)