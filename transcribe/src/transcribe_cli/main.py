from __future__ import annotations

import os
import logging
from pathlib import Path

from dotenv import load_dotenv

from .logging_setup import setup_logging
from .config import load_config
from .paths import normalize_input_path, build_output_txt_path
from .output import write_txt
from .whisper_asr import transcribe_file_de
from .mailer import SmtpSettings, send_mail_text
from .recorder import record_until_enter


load_dotenv()


def ask_yes_no(prompt: str) -> bool:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("j", "ja", "y", "yes"):
            return True
        if ans in ("n", "nein", "no"):
            return False
        print("Bitte J oder N eingeben.")


def ask_choice(prompt: str, choices: tuple[str, ...]) -> str:
    while True:
        ans = input(prompt).strip().upper()
        if ans in choices:
            return ans
        print(f"Bitte {'/'.join(choices)} eingeben.")


def main() -> int:
    print("\n--- Spracherkennung by sIn ---\n")

    project_root = Path(__file__).resolve().parents[2]
    cfg = load_config(project_root)

    setup_logging(cfg.log_dir, cfg.log_level)
    log = logging.getLogger(__name__)
    log.info("Start Spracherkennung by sIn")

    output_dir = cfg.output_dir.resolve()

    # 1. Abfrage
    audio_vorhanden = ask_yes_no("Audio vorhanden? (J/N): ")

    audio_path: Path | None = None

    if audio_vorhanden:
        raw = input("Bitte Pfad zur Audio-Datei angeben: ").strip()
        audio_path = normalize_input_path(raw)
        if not audio_path.exists():
            print("Datei nicht gefunden:", audio_path)
            return 2
        print("Pfad gewählt:", audio_path)
    else:
        print("Recorder wird nach der dritten Abfrage gestartet.")

    # 2. Abfrage
    mode = ask_choice(
        "Ergebnis in .txt speichern (S), oder Mail senden (M)? ",
        ("S", "M"),
    )

    # 3. Abfrage (nur bei Mail)
    to_addr: str | None = None
    if mode == "M":
        to_addr = input("Bitte Mailadresse eingeben: ").strip()
        if not to_addr:
            print("Keine Mailadresse eingegeben.")
            return 3
        print("Mailadresse:", to_addr)

    # --- Recorder nach der 3. Abfrage ---
    if not audio_vorhanden:
        recordings_dir = project_root / "input" / "recordings"
        audio_path = record_until_enter(output_dir=recordings_dir)
        log.info("Recorded audio saved: %s", audio_path)
   
    # --- Type-Safety: audio_path muss jetzt gesetzt sein ---
    if audio_path is None:
        raise RuntimeError("Audio path should not be None at this point.")

    # --- Transkription ---
    log.info("Mode selected: %s", mode)
    print("\nTranskription startet...\n")
    txt = transcribe_file_de(audio_path)

    # --- Datei speichern ---
    out_txt = build_output_txt_path(output_dir, audio_path)
    write_txt(out_txt, txt)
    log.info("Ergebnis gespeichert: %s", out_txt)

    print("\nGespeichert:", out_txt)

    # --- Mailversand ---
    if mode == "M":
        log.info("Mail requested to: %s", to_addr)

        smtp = SmtpSettings(
            host="smtp.gmail.com",
            port=465,
            use_ssl=True,
            user=os.environ["SMTP_USER"],
            app_password=os.environ["SMTP_APP_PASSWORD"],
            from_name="Spracherkennung CLI",
        )

        subject = f"[Transkript] {out_txt.stem}"

        assert to_addr is not None  # for type checker

        send_mail_text(
            smtp=smtp,
            to_addr=to_addr,
            subject=subject,
            text_content=txt,
        )

        print("Mail wurde gesendet.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
