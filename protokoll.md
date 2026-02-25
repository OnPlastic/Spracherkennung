## Installation

Ich habe bereits ein eingerichtetes WSL. Ich habe geprüft ob Sound wiedergegeben werden kann und ob Sound aufgenommen werden kann.

1. Pakete in WSL installieren:

`sudo apt update && sudo apt install -y pulesaudio-utils libasound2-plugins`

2. Mikrofon/Lautsprecher testen

`pactl list sources short`

| |               |                 |     |   |       |         |
|-|---------------|-----------------|-----|---|-------|---------|
|1|RDPSink.monitor|module-rdp-sink.c|s16le|2ch|44100Hz|SUSPENDED|
|2|RDPSource|module-rdp-source.c|s16le|1ch|44100Hz|SUSPENDED|

>RDPSource = Microphone; RDPSink = Lautsprecher

![Anleitung zur Konfiguration von Mikrofon und Lautsprecher in WSL mit PulseAudio-Einstellungen](image1.png)

3. En/Decoder installieren

`sudo apt update
 sudo apt install -y ffmpeg`

 4. Virtuelle Umgebung anlegen

```
cd ~/dev/projects/spracherkennung  
mkdir -p transcribe && cd transcribe  
python3 -m venv .venv  
source .venv/bin/activate  
python -m pip install -U pip  
```

5. Projektstruktur Anlegen

```
cd ~/dev/projects/spracherkennung/transcribe

mkdir -p src/transcribe_cli
mkdir -p scripts
mkdir -p input/audio input/recordings
mkdir -p output/transcripts
mkdir -p logs
```

6. Kernpakete installieren (Ubuntu - PortAudio libs)

```
sudo apt install -y portaudio19-dev
```


7. Whisper und Sounddevice installieren

```
(dev_admin@DESKTOP-DELL:~/dev/projects/spracherkennung/transcribe$)  
source .venv/bin/activate
pip install -U openai-whisper
pip install sounddevice
```

8. Die "requirements.txt" schreiben

```
pip freeze > requirements.txt
```

9. Abschlusstest ob alles läuft

```
source .venv/bin/activate  
python -c "import whisper; print('whisper ok')"  
ffmpeg -version | head -n 1
```
![Bash terminal output showing successful verification of whisper installation and ffmpeg version](image2.png)

10. Optimierung für die Versionskontrolle - gitignore - anlegen

`touch .gitignore`

Inhalt

```
.venv/
__pycache__/
*.pyc
input/recordings/
output/
logs/
```
11. Versionskontrolle einrichten und Repo erstellen
```
bsh  
git --version  
>git version 2.43.0
```
falls nicht vorhanden git installieren
>sudo apt install git

```
bsh
cd ~/dev/projects/spracherkennung
git init
git status
```
12. Git initialisieren (.gitignore noch eine Ebene höher verschieben)

```
bsh
cd ~/dev/projects/spracherkennung
mv transcribe/.gitignore .
git init
```

13. Files stashen (adden) und commiten

```
git add . 
git commit -m "Initial project structure for speech recognition system"
```
14. **GitHub**-Repo anbinden

*https://gihub.com/OnPlastic*
Erstellen eines neuen Repos, Name: **Spracherkennung**
- kein README erzeugen
- kein .gitignore erzeugen
- kein License erzeugen

>Remote Repo SSH

```
git remote add origin git@github.com:OnPlastic/spracherkennung.git

git branch -M main
git push -u origin main
```

