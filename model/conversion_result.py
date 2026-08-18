from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConversionResult:
    file_path: str | Path
    success: bool = False
    output_path: str | Path | None = None
    error_message: str | None = None


@dataclass
class BatchConversionResult:
    results: list[ConversionResult] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        return sum(1 for result in self.results if result.success)

    @property
    def fail_count(self) -> int:
        return len(self.results) - self.success_count

    @property
    def failed_files(self) -> list[tuple[str, str]]:
        return [
            (str(result.file_path), result.error_message or "알 수 없는 오류")
            for result in self.results
            if not result.success
        ]
