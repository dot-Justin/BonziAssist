# Getting Started with BonziAssist

This walkthrough is for the common stuck point: “I did everything and it still feels flipped.”

## Requirements (Windows-first)

1. **Python 3.10+** — https://www.python.org/downloads/ (check “Add Python to PATH”)
2. **Visual C++ Build Tools** — https://visualstudio.microsoft.com/visual-cpp-build-tools/ (needed for `pyaudio` / `vosk` wheels on some machines)
3. A working **microphone**
4. An LLM API key (default path uses **Groq**)

## Install (5 steps)

```bash
git clone https://github.com/dot-Justin/BonziAssist.git
cd BonziAssist
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

## Configure the LLM (the usual blocker)

```bash
# From repo root:
cp helpers/.env.example helpers/.env
```

Edit `helpers/.env`:

- Set `LLM_PROVIDER=groq` (or another LiteLLM-supported provider)
- Set `GROQ_API_KEY=...` from https://console.groq.com/keys
- Remove any leftover instruction / placeholder lines

**Important:** the file must be named exactly `helpers/.env` (not `.env.example`).

## Download the Vosk model (if missing)

The wake-word path expects:

`vosk/vosk-model-small-en-us-0.15`

If that folder is empty/missing, download the small English model from https://alphacephei.com/vosk/models and extract it into `vosk/`.

## Run

```bash
python main.py
```

1. First run may ask you to **pick a microphone** — choose the device you speak into.
2. Wait until the console shows listening activity.
3. Say **“Bonzi”** (short phrase). You should hear a canned acknowledgment.
4. Then speak your request; Bonzi replies via TTS (TETYYS SAPI4).

## If it “feels flipped” / nothing happens

| Symptom | Fix |
|---|---|
| No mic prompt / silence | Re-run and set `prompt_every_time` via mic config, or delete `mic_config.json` and restart |
| Hears text but never answers | Check `helpers/.env` exists and `GROQ_API_KEY` is valid |
| Hears nothing useful | Move closer to mic; wake words are fuzzy (“bones”, “ponzi”, etc. are aliases) |
| `pyaudio` install fails | Install Visual C++ Build Tools, then `pip install pyaudio` again |
| TTS errors | Confirm outbound HTTPS to `tetyys.com` is allowed |

## Quick sanity checks

```bash
python -c "from helpers import llm; print('llm import ok')"
python -c "import vosk, pyaudio; print('vosk/pyaudio ok')"
ls helpers/.env
ls vosk/vosk-model-small-en-us-0.15
```

## Still stuck?

Open an issue with: OS version, Python version, the last 20 console lines, and whether `helpers/.env` exists (redact keys).
