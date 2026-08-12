from config import logger as config_logger
from view.gui import VsqxConverterGUI
import logging

config_logger.set_logger()
logger = logging.getLogger(__name__)
logger.info("VSQX Converter 실행")
gui = VsqxConverterGUI()
logger.info("VSQX Converter 종료")