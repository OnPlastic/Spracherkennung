from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from time import perf_counter

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as wav_write

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class RecordingSettings:
    samplerate: int = 16000
    channels: int = 1
    dtype: str = "float32"


def record_until_enter(
    *,
    output_dir: Path,
    settings: RecordingSettings = RecordingSettings(),
) -> Path:
    """
    Start microphone recording and stopo on ENTER.
    Saves WAV into output_dir and returns the path.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"{ts}_recording.wav"

    log.info(
        "Recording started (samplerate=%d, channels=%d) -> %s",
        settings.samplerate,
        settings.channels,
        out_path,
    )

    print("\nAufnahme läuft... Drücke <ENTER> zum Stoppen.\n")

    frames: list[np.ndarray] = []
    t0 = perf_counter()

    def callback(indata, frame_count, time_info, status):
        if status:
            log.warning("Audio status: %s", status)
        frames.append(indata.copy())

    with sd.InputStream(
        samplerate=settings.samplerate,
        channels=settings.channels,
        dtype=settings.dtype,
        callback=callback,
    ):
        input()  # Wait for ENTER

    dt = perf_counter() - t0

    if not frames:
        raise RuntimeError("Keine Audiodaten aufgenommen (frames leer).")

    audio = np.concatenate(frames, axis=0)

    # float32 -> int16 PCM for WAV
    audio = np.clip(audio, -1.0, 1.0)
    audio_i16 = (audio * 32767.0).astype(np.int16)

    wav_write(str(out_path), settings.samplerate, audio_i16)

    seconds = audio.shape[0] / float(settings.samplerate)
    log.info("Recording finished in %.2f s | audio_len=%.2f s", dt, seconds)
    print(f"\nAufnahme gespeichert: {out_path}\n")

    return out_path
