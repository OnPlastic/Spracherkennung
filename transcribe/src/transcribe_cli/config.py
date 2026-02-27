from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class AppConfig:
    output_dir: Path
    log_dir: Path
    log_level: str


def load_config(project_root: Path) -> AppConfig:
    cfg_path = project_root / "config.toml"

    if not cfg_path.exists():
        raise FileNotFoundError(f"config.toml nicht gefunden: {cfg_path}")

    with cfg_path.open("rb") as f:
        raw = tomllib.load(f)

    t = raw.get("transcription", {})
    l = raw.get("logging", {})
    log_dir = project_root / l.get("log_dir", "logs")
    log_level = str(l.get("level", "INFO")) 
    output_dir = project_root / t.get("output_dir", "output/transcripts")

    return AppConfig(
        output_dir=output_dir,
        log_dir=log_dir,
        log_level=log_level       
    )