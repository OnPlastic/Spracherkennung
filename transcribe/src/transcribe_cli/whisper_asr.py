from __future__ import annotations
from time import perf_counter
import logging
from pathlib import Path
import whisper


log = logging.getLogger(__name__)

_MODEL = None
_MODEL_NAME = "large-v3"


def get_model():
    global _MODEL
    if _MODEL is None:
        log.info("Loading Whisper model: %s", _MODEL_NAME)
        _MODEL = whisper.load_model(_MODEL_NAME)
        log.info("Whisper model loaded: %s", _MODEL_NAME)
    return _MODEL


def transcribe_file_de(audio_path: Path) -> str:
    """
    Transkribiert eine Audiodatei mit Whisper.
    - Modell: large-v3
    - Sprache: Deutsch (de)
    - Output: reiner TEXT
    """
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = get_model()

    log.info("Transcription started: %s", audio_path)
    t0 = perf_counter()
    # fp16 nur auf GPU sinnvoll; auf CPU kann fp16 Probleme machen
    result = model.transcribe(
        str(audio_path),
        language="de",
        task="transcribe",
        fp16=False,
    )

    dt = perf_counter() - t0
    text = (result.get("text") or "").strip()
    log.info("Transcription finished in %.2f s | chars=%d", dt, len(text))
    return text
