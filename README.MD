<div style="text-align: center;">

<img src="assets/BonziASSIST_bg.png" alt="Shiny Text" style="width:70%; height:auto;">

</div>



## BonziAssist: Your New (Old) Assistant!



This project uses the [TETYYS generator](https://www.tetyys.com/SAPI4/). Also see: [BonziBuddy-TTS](https://github.com/dot-Justin/BonziBuddy-TTS).



### ⚠️ Do Not Abuse the API ⚠️



BonziAssist revives the classic BonziBuddy assistant in a modern, voice-activated form, allowing you to interact with an AI through spoken commands. Here’s a bit more about what makes BonziAssist special and how to use it.



### Features



- **Voice Activation**: Simply say "`Bonzi`" and once you hear Bonzi confirm he's listening, you're ready to go!

- **Text-to-Speech**: Utilizes the nostalgic BonziBuddy voice for responses, thanks to the [TETYYS SAPI4 API](https://www.tetyys.com/SAPI4/).

- **Real-Time Interaction**: Communicate in real-time, with responses generated through a lightweight LLM.



### Installation



1. Clone this repository.

2. Ensure you have [Python](https://www.python.org/downloads/) and [Visual CPP Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed.

3. Install dependencies: `pip install -r requirements.txt`.

4. Set up your environment variables. Edit the `.env.example` file in `helpers/` and follow the instructions there. Rename it to `.env`.



### Usage



To start BonziAssist:



```bash

python main.py

```



You will be prompted to configure your microphone settings upon the first run.



### Troubleshooting

- **Microphone not detected**: Ensure your microphone is set as the default recording device in Windows settings.

- **API Errors**: Check your internet connection as the TTS requires the TETYYS API.



## TODO

- [x] **Add LiteLLM**: Enable Bonzi to talk back to you

- [ ] **HIGH PRIO: Improve STT Accuracy**: Potentially use a bigger VOSK model

- [ ] **Improve STT Speed**: Potentially use a different package

- [ ] **Improve TTS Speed**: Find a way to run locally for quicker responses

- [ ] **Offline Functionality**: Use fully offline APIs such as Ollama

- [ ] **Add Voice Volume Control**

- [ ] **Add simple windows functions**: Such as Media control, opening apps, etc.

- [ ] **Add interruption support**: Potentially via a hotkey (press esc to interrupt)

- [ ] **Add fancy splash screen**



#### Continuous goals

- When VOSK misunderstands, add to the list of phrases Bonzi will respond to

- Update system prompt to give more personality and functionality

- Optimize Performance



Contributors are welcome to help with these tasks. If you are interested, please fork the repository, make your changes, and submit a pull request.



## How it Works

1. Listening: The system starts by listening for the activation word "Bonzi".

2. Processing: Speech is converted to text and processed by an LLM.

3. Responding: The response is converted to speech using the SAPI4 API.



## Credits

- [TETYYS](https://www.tetyys.com/) for the SAPI4 API.

- [Vosk](https://alphacephei.com/vosk/) for offline STT.



