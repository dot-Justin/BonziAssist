import subprocess
import webbrowser

try:
    import pyautogui
except Exception as e:
    raise ImportError("pyautogui is required for windows actions") from e

# Media control functions

def play_pause():
    """Toggle play/pause on the active media player."""
    pyautogui.press('playpause')

def next_track():
    """Skip to the next media track."""
    pyautogui.press('nexttrack')

def previous_track():
    """Return to the previous media track."""
    pyautogui.press('prevtrack')

def volume_up():
    """Increase system volume."""
    pyautogui.press('volumeup')

def volume_down():
    """Decrease system volume."""
    pyautogui.press('volumedown')

def mute_volume():
    """Mute or unmute system volume."""
    pyautogui.press('volumemute')

# Application launch helpers

def open_notepad():
    """Open Windows Notepad."""
    subprocess.Popen('notepad.exe')

def open_calculator():
    """Open Windows Calculator."""
    subprocess.Popen('calc.exe')

def open_file_explorer():
    """Open a new File Explorer window."""
    subprocess.Popen('explorer.exe')

def open_browser(url="https://www.google.com"):
    """Open the default web browser to the specified URL."""
    webbrowser.open(url)
