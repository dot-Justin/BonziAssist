import argparse
import importlib.util
import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
REQUIRED_PACKAGES = {
    "dotenv": "python-dotenv",
    "litellm": "litellm",
    "pyaudio": "pyaudio",
    "requests": "requests",
    "simpleaudio": "simpleaudio",
    "vosk": "vosk",
}


def missing_packages():
    missing = []
    for import_name, package_name in REQUIRED_PACKAGES.items():
        if importlib.util.find_spec(import_name) is None:
            missing.append(package_name)
    return missing


def load_env_file():
    env_path = PROJECT_ROOT / ".env"
    values = {}
    if not env_path.exists():
        return values

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def check_setup():
    errors = []
    warnings = []

    missing = missing_packages()
    if missing:
        errors.append(
            "Install missing packages with: "
            + f"{sys.executable} -m pip install -r requirements.txt"
            + f" (missing: {', '.join(missing)})"
        )

    env_path = PROJECT_ROOT / ".env"
    env_values = load_env_file()
    if not env_path.exists():
        errors.append("Create .env by copying .env.example, then set GROQ_API_KEY and LLM_PROVIDER.")
    else:
        for key in ("GROQ_API_KEY", "LLM_PROVIDER"):
            if not env_values.get(key) or env_values[key].startswith("your_"):
                errors.append(f"Set {key} in .env.")

    model_path = PROJECT_ROOT / "vosk" / "vosk-model-small-en-us-0.15"
    if not model_path.exists():
        errors.append("The Vosk model is missing. Expected: vosk/vosk-model-small-en-us-0.15")

    if not (PROJECT_ROOT / "canned_responses").exists():
        errors.append("The canned_responses folder is missing.")

    if not (PROJECT_ROOT / "config").exists():
        warnings.append("The config folder will be created on first microphone setup.")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Check and start BonziAssist.")
    parser.add_argument("--check", action="store_true", help="Only check setup and exit.")
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    errors, warnings = check_setup()

    for warning in warnings:
        print(f"Warning: {warning}")

    if errors:
        print("BonziAssist is not ready to start:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("BonziAssist setup looks ready.")
    if args.check:
        return

    from main import main as run_bonzi

    run_bonzi()


if __name__ == "__main__":
    main()
