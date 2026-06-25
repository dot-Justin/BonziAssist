# 🚀 BonziAssist Setup Guide

A complete step-by-step guide to get BonziAssist running on your machine.

## Prerequisites

### 1. Install Python 3.8+
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
  - ✅ **IMPORTANT**: Check "Add Python to PATH" during installation
- **Linux**: `sudo apt install python3 python3-pip python3-venv`
- **macOS**: `brew install python3`

### 2. Install Visual C++ Build Tools (Windows Only)
BonziAssist requires PyAudio, which needs C++ build tools:
1. Download from [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Run installer → select "Desktop development with C++"
3. Restart your computer after installation

### 3. Verify Installation
```bash
python --version   # Should show Python 3.8+
pip --version      # Should show pip
```

## Step-by-Step Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/dot-Justin/BonziAssist.git
cd BonziAssist
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```
You should see `(venv)` at the beginning of your terminal prompt.

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
If you encounter errors with PyAudio on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

### Step 4: Configure Environment Variables
1. Navigate to the `helpers/` folder
2. You'll find a file named `.env.example`
3. Open it in a text editor
4. Follow the instructions in the file to fill in your API keys
5. **Rename** the file from `.env.example` to `.env`
6. Make sure it's saved in the `helpers/` folder

> ⚠️ **Common mistake**: Don't skip the `.example` removal! The file MUST be named exactly `.env` (no `.example` extension).

### Step 5: Run BonziAssist
```bash
python main.py
```

On first run, you'll be prompted to set up your microphone. Follow the on-screen instructions.

## Usage
1. Say **"Bonzi"** to activate the assistant
2. Wait for Bonzi to confirm he's listening
3. Speak your command or question
4. Bonzi will respond using the classic BonziBuddy voice!

## Troubleshooting

### "ModuleNotFoundError: No module named '...'"
```bash
pip install -r requirements.txt --upgrade
```

### Microphone not working
- Windows: Check microphone privacy settings (Settings → Privacy → Microphone)
- Linux: Install portaudio: `sudo apt install portaudio19-dev`
- Make sure no other app is using your microphone

### "FileNotFoundError: mic_config.json"
Run the program from the repository root directory (where `main.py` is located).

### TTS not working
The TETYYS SAPI4 API may occasionally be offline. Wait a few minutes and try again.

## Quick Check
Run this to verify your setup:
```bash
python -c "import pyaudio; import vosk; import dotenv; print('All imports OK!')"
```
If you see "All imports OK!", you're ready to go! 🎉

## Need Help?
Open an issue on GitHub with:
1. Your operating system
2. Python version (`python --version`)
3. The full error message (copy-paste, don't screenshot)
4. What you've tried so far
