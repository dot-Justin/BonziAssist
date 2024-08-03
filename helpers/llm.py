import os
from dotenv import load_dotenv
import litellm

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
llm_provider = os.getenv("LLM_PROVIDER")

if groq_api_key is None:
    raise ValueError("GROQ_API_KEY environment variable not found. Please set it in your .env file.")

if llm_provider is None:
    raise ValueError("LLM_PROVIDER environment variable not found. Please set it in your .env file.")

os.environ["GROQ_API_KEY"] = groq_api_key

def request(user_query, model="llama3-8b-8192", temperature=0.7, max_tokens=150):
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