from __future__ import annotations
from pathlib import Path
from datetime import datetime


def normalize_input_path(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def build_output_txt_path(output_dir: Path, audio_path: Path | None) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = "recording" if audio_path is None else audio_path.stem
    stem = stem.replace(" ", "_")
    return output_dir / f"{ts}_{stem}.txt"

