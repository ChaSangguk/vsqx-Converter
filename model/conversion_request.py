from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConversionRequest:
    file_path: str | Path
    convert_type: str
    convert_path: str | Path | None = None
