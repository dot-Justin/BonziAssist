# Getting Started

This guide walks through the first run of BonziAssist from a fresh clone.

## Prerequisites

- Python 3.10 or newer
- A working microphone
- Windows users: Visual C++ Build Tools, which are needed by PyAudio on many machines
- A Groq API key for the default LiteLLM provider

## Install

Clone the repository and enter the project folder:

```bash
git clone https://github.com/dot-Justin/BonziAssist.git
cd BonziAssist
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Copy the example environment file to the project root:

```bash
copy helpers\.env.example .env
```

Edit `.env` and set your values:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your-api-key-here
```

BonziAssist also supports `helpers\.env` for compatibility, but keeping `.env` in the project root matches the commands in this guide.

## Start BonziAssist

Run the app from the project root:

```bash
python main.py
```

On the first run, choose the microphone input device. The selected device is saved to `mic_config.json`.

After startup, say `Bonzi`. Once Bonzi responds, speak your command.

## Troubleshooting

### `GROQ_API_KEY environment variable not found`

Make sure `.env` exists in the project root and contains `GROQ_API_KEY`.

### `LLM_PROVIDER environment variable not found`

Make sure `.env` contains `LLM_PROVIDER=groq`.

### PyAudio fails to install on Windows

Install Visual C++ Build Tools, restart the terminal, reactivate the virtual environment, and run:

```bash
pip install -r requirements.txt
```

### Wrong microphone selected

Delete `mic_config.json` and start again:

```bash
del mic_config.json
python main.py
```

### Bonzi does not hear the wake word

Check that the Vosk model exists at `vosk/vosk-model-small-en-us-0.15`, then try again in a quieter room and speak the wake word clearly.

### No spoken response

The text-to-speech response depends on the TETYYS SAPI4 endpoint. If it is unavailable, wait a moment and try again.
