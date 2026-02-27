from __future__ import annotations
import logging
from pathlib import Path
from datetime import datetime


def setup_logging(log_dir: Path, level: str = "INFO") -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    logfile = log_dir / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    numeric_level = getattr(logging, level.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(numeric_level)

    # keine doppelten Handler bei wiederholtem Start 
    if root.handlers:
        root.handlers.clear()

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    ch = logging.StreamHandler()
    ch.setLevel(numeric_level)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setLevel(numeric_level)
    fh.setFormatter(fmt)
    root.addHandler(fh)

    logging.getLogger(__name__).info("Logging initialized: %s", logfile)
    return logfile
