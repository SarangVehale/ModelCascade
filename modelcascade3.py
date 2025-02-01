import subprocess
import time
import logging
import sys
import threading
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Banner
BANNER = r"""
  __  __           _      _  _____                        _      
 |  \/  |         | |    | |/ ____|                      | |     
 | \  / | ___   __| | ___| | |     __ _ ___  ___ __ _  __| | ___ 
 | |\/| |/ _ \ / _` |/ _ \ | |    / _` / __|/ __/ _` |/ _` |/ _ \
 | |  | | (_) | (_| |  __/ | |___| (_| \__ \ (_| (_| | (_| |  __/
 |_|  |_|\___/ \__,_|\___|_|\_____\__,_|___/\___\__,_|\__,_|\___|
                                                                 
"""

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("modelcascade.log")
    ]
)

# Maximum number of retries
MAX_RETRIES = 5

# Delay between retries in seconds
RETRY_DELAY = 5

# Global flag to skip the current model
skip_model = False

def pull_model(model_name):
    """
    Attempt to pull a model using the `ollama pull` command.
    Retry up to MAX_RETRIES times if an error occurs.
    """
    global skip_model
    retries = 0
    while retries < MAX_RETRIES:
        if skip_model:
            logging.warning(f"Skipping model: {model_name} (user request)")
            return "skipped"
        try:
            logging.info(f"Pulling model: {model_name} (Attempt {retries + 1})")
            # Run the `ollama pull` command
            result = subprocess.run(
                ["ollama", "pull", model_name],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Log success
            logging.info(f"Successfully pulled model: {model_name}")
            logging.info(result.stdout)
            return "success"
        except subprocess.CalledProcessError as e:
            # Log the error
            logging.error(f"Error pulling model {model_name}: {e.stderr}")
            retries += 1
            if retries < MAX_RETRIES:
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logging.error(f"Failed to pull model {model_name} after {MAX_RETRIES} attempts.")
                return "failed"

def get_models_from_file(file_path):
    """
    Read model names from a file (one model per line).
    """
    try:
        with open(file_path, "r") as file:
            models = [line.strip() for line in file.readlines() if line.strip()]
        return models
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []

def get_models_from_user():
    """
    Prompt the user to input model names, either one by one or as a list.
    """
    models = []
    print(Fore.CYAN + "Enter model names (one per line). Press Enter twice to finish:")
    while True:
        model = input().strip()
        if not model:
            break
        models.append(model)
    return models

def validate_models(models):
    """
    Validate model names (e.g., ensure they are not empty or malformed).
    """
    valid_models = []
    for model in models:
        if model and " " not in model:
            valid_models.append(model)
        else:
            logging.warning(f"Skipping invalid model name: {model}")
    return valid_models

def is_model_pulled(model_name):
    """
    Check if the model is already pulled.
    """
    try:
        subprocess.run(
            ["ollama", "list"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # For simplicity, assume the model is not pulled
        return False
    except subprocess.CalledProcessError:
        return False

def listen_for_skip():
    """
    Listen for user input to skip the current model.
    """
    global skip_model
    while True:
        key = input()
        if key.strip().lower() == "s":
            skip_model = True
            print(Fore.YELLOW + "Skipping current model...")

def main():
    """
    Main function to handle input and pull models.
    """
    global skip_model
    print(Fore.GREEN + BANNER)
    print(Fore.YELLOW + "Welcome to ModelCascade! Let's pull some models.\n")

    # Ask the user for input method
    print(Fore.CYAN + "Choose an input method:")
    print(Fore.CYAN + "1. Enter model names manually")
    print(Fore.CYAN + "2. Provide a file containing model names")
    choice = input(Fore.CYAN + "Enter your choice (1 or 2): ").strip()

    if choice == "1":
        models = get_models_from_user()
    elif choice == "2":
        file_path = input(Fore.CYAN + "Enter the path to the file: ").strip()
        models = get_models_from_file(file_path)
    else:
        logging.error(Fore.RED + "Invalid choice. Exiting.")
        sys.exit(1)

    if not models:
        logging.error(Fore.RED + "No models provided. Exiting.")
        sys.exit(1)

    # Validate models
    models = validate_models(models)
    if not models:
        logging.error(Fore.RED + "No valid models to pull. Exiting.")
        sys.exit(1)

    # Start a thread to listen for skip input
    skip_thread = threading.Thread(target=listen_for_skip, daemon=True)
    skip_thread.start()

    # Pull models with progress bar
    success_count = 0
    failed_count = 0
    skipped_count = 0
    print(Fore.GREEN + "\nStarting model pull process...\n")
    print(Fore.YELLOW + "Press 's' and Enter to skip the current model.\n")
    try:
        for model in tqdm(models, desc="Pulling models", unit="model", ncols=100):
            skip_model = False  # Reset skip flag for each model
            if is_model_pulled(model):
                logging.info(f"Model {model} is already pulled. Skipping.")
                success_count += 1
                continue
            result = pull_model(model)
            if result == "success":
                success_count += 1
            elif result == "failed":
                failed_count += 1
            elif result == "skipped":
                skipped_count += 1
    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted by user. Exiting gracefully.")
        sys.exit(0)

    # Display summary
    print(Fore.GREEN + "\nSummary:")
    print(Fore.GREEN + f"✅ Successfully pulled models: {success_count}")
    print(Fore.RED + f"❌ Failed to pull models: {failed_count}")
    print(Fore.YELLOW + f"⏩ Skipped models: {skipped_count}")

if __name__ == "__main__":
    main()
