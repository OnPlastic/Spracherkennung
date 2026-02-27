from __future__ import annotations
from pathlib import Path
import logging
from .logging_setup import setup_logging

from .paths import normalize_input_path, build_output_txt_path
from .output import write_txt
from .config import load_config


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
	print("\n--- Spracherkennung v1 (Block A) ---\n")

	# Output 'dir' aus config.toml nutzen wir gleich in A4.
	# Für A3 wird es fest auf den Pfad:
	# Output_Dir = Path("output/transcripts").resolve()

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
		print(
			"Recorder wird nach der dritten Abfrage gestartet. "
			"(noch nicht implementiert)."
		)

	# 2. Abfrage
	mode = ask_choice(
		"Ergebnis in .txt speichern (S), oder  Mail senden (M)?",
		("S", "M"),
	)

	# 3. Abfrage (nur bei Mail)
	to_addr: str | None = None
	if mode == "M":
		to_addr = input("Bitte Mailadresse eingeben: ").strip()
		print("Mailadresse:", to_addr)

	# Dummy-Transkript schreiben (für Block A)
	dummy = "TESTTRANSKRIPT (Block A)"
	# output_dir = Path("output/transcripts").resolve()
	project_root = Path(__file__).resolve().parents[2]
	cfg = load_config(project_root)
	log = logging.getLogger(__name__)
	setup_logging(cfg.log_dir, cfg.log_level)
	log.info("Start Spracherkennung sIn (Block A)")
	output_dir = cfg.output_dir.resolve()
	out_txt = build_output_txt_path(output_dir, audio_path)
	write_txt(out_txt, dummy)
	log.info("Ergebnis gespeichert: %s", out_txt)

	print("\nGespeichert:", out_txt)

	if mode == "M":
		print("Mailversand inst in Block C dran. (Noch nicht implementiert)")

	if not audio_vorhanden:
		print("Recorder ist in Block D dran. (Noch nicht implementiert)")

	return 0


if __name__ == "__main__":
	raise SystemExit(main())
