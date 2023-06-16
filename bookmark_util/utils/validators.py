from __future__ import annotations

from pathlib import Path
from typing import Union

def valid_dir(_dir: Union[str, Path] = None) -> Path:
    if not _dir:
        raise ValueError("Missing root_dir value")

    if not isinstance(_dir, Union[str, Path]):
        raise ValueError("_dir must be a str or Path object")

    if isinstance(_dir, str):
        _dir: Path = Path(_dir)

    if not _dir.is_dir():
        raise ValueError(f"root_dir is not a directory: {_dir}")

    if not _dir.exists():
        raise FileNotFoundError(f"Could not find root directory: {_dir}")

    return _dir
