from __future__ import annotations

import io
import wave
from urllib.parse import quote_plus

import pyaudio
import requests

# Adapted from https://github.com/dot-Justin/BonziBuddy-TTS
# Credit to https://www.tetyys.com/SAPI4/


def _play_wav(data: bytes) -> None:
    with wave.open(io.BytesIO(data), "rb") as audio:
        player = pyaudio.PyAudio()
        stream = None
        try:
            stream = player.open(
                format=player.get_format_from_width(audio.getsampwidth()),
                channels=audio.getnchannels(),
                rate=audio.getframerate(),
                output=True,
            )
            while chunk := audio.readframes(1024):
                stream.write(chunk)
        finally:
            if stream is not None:
                stream.stop_stream()
                stream.close()
            player.terminate()


def say(text: str) -> None:
    encoded_text = quote_plus(text)
    tts_url = (
        "https://www.tetyys.com/SAPI4/SAPI4"
        f"?text={encoded_text}"
        "&voice=Adult%20Male%20%232%2C%20American%20English%20(TruVoice)"
        "&pitch=140&speed=157"
    )
    response = requests.get(tts_url, timeout=30)
    response.raise_for_status()
    _play_wav(response.content)
