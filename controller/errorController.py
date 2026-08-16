class ConversionError(Exception):
    """기본 변환 예외"""


class ConvertListError(ConversionError):
    """변환 규칙 파일을 불러오지 못했을 때 발생하는 예외"""


class VSQXFileReadError(ConversionError):
    """VSQX 파일을 읽거나 파싱하지 못했을 때 발생하는 예외"""


class ConversionExecutionError(ConversionError):
    """변환 실행이 실패했을 때 발생하는 예외"""
