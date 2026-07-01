import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

try:
    import litellm
except ModuleNotFoundError:
    litellm = None

HELPERS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = HELPERS_DIR.parent

if load_dotenv is not None:
    load_dotenv(PROJECT_DIR / ".env")
    load_dotenv(HELPERS_DIR / ".env", override=True)


def get_missing_dependencies():
    missing = []
    if load_dotenv is None:
        missing.append("python-dotenv")
    if litellm is None:
        missing.append("litellm")
    return missing


def get_missing_environment():
    missing = []
    if os.getenv("LLM_PROVIDER") is None:
        missing.append("LLM_PROVIDER")
    if os.getenv("GROQ_API_KEY") is None:
        missing.append("GROQ_API_KEY")
    return missing


def get_config_status():
    return get_missing_dependencies() + get_missing_environment()


def require_config():
    missing_dependencies = get_missing_dependencies()
    if missing_dependencies:
        raise ModuleNotFoundError(
            "Missing Python package(s): "
            + ", ".join(missing_dependencies)
            + ". Run `pip install -r requirements.txt` first."
        )

    missing_environment = get_missing_environment()
    if missing_environment:
        raise ValueError(
            "Missing environment variable(s): "
            + ", ".join(missing_environment)
            + ". Copy helpers/.env.example to helpers/.env and fill in the values."
        )

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    return os.getenv("LLM_PROVIDER")


def request(user_query, model="llama3-8b-8192", temperature=0.7, max_tokens=150):
    llm_provider = require_config()
    messages = [
        {"role": "system", "content": """You are a helpful new state of the art assistant, called BonziAssist. You are based on the old BonziBuddy archetecture, and have the same voice.
         You are the backend for a new project, where instead of the user typing to an LLM, they speak. Manage your responses as such.
         All of your responses are fairly short, one to two sentences long, unless the user specifically requests a longer answer.
         You never use markdown formatting, output everything as if it will be read aloud literally.
         If the user misspells or uses the wrong words to convey something, do your best to interpret.
         If the user says anything like 'nevermind' or 'go away', simply output 'Ok.'
         If the user says a single word, or a few words strung together that don't make any sense, (after examining and trying to interpret), say 'Sorry, something went wrong.'"""},
        {"role": "user", "content": user_query}
    ]

    response = litellm.completion(
        model=f"{llm_provider}/{model}",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content
