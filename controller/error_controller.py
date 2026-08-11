from __future__ import annotations

import json
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ErrorResult:
    context: str
    message: str
    fatal: bool = True
    details: str | None = None

class ErrorController:
    def handle_error(self, error: Exception, context: str) -> ErrorResult:
        if isinstance(error, FileNotFoundError):
            message = f"{context} 중 오류가 발생했습니다: 파일을 찾을 수 없습니다."
        elif isinstance(error, json.JSONDecodeError):
            message = f"{context} 중 오류가 발생했습니다: 파일 형식이 올바르지 않습니다."
        elif isinstance(error, KeyError):
            message = f"{context} 중 오류가 발생했습니다: 설정 값이 올바르지 않습니다."
        else:
            message = f"{context} 중 오류가 발생했습니다: {error}"

        logger.error(message)
        return ErrorResult(context=context, message=message, details=str(error))
