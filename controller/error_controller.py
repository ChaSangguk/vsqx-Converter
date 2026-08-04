from __future__ import annotations

import json
import logging
logger = logging.getLogger(__name__)
class ErrorController:
    def raise_error(self, error: Exception, context: str) -> None:
        if isinstance(error, FileNotFoundError):
            raise ValueError(f"{context} 중 오류가 발생했습니다: 파일을 찾을 수 없습니다.") from error
        if isinstance(error, json.JSONDecodeError):
            raise ValueError(f"{context} 중 오류가 발생했습니다: 파일 형식이 올바르지 않습니다.") from error
        if isinstance(error, KeyError):
            raise ValueError(f"{context} 중 오류가 발생했습니다: 설정 값이 올바르지 않습니다.") from error
        raise ValueError(f"{context} 중 오류가 발생했습니다: {error}") from error
