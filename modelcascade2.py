import subprocess
import time
import logging
import sys
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Banner
BANNER = r"""

.___  ___.   ______    _______   _______  __        ______     ___           _______.  ______     ___       _______   _______
|   \/   |  /  __  \  |       \ |   ____||  |      /      |   /   \         /       | /      |   /   \     |       \ |   ____|
|  \  /  | |  |  |  | |  .--.  ||  |__   |  |     |  ,----'  /  ^  \       |   (----`|  ,----'  /  ^  \    |  .--.  ||  |__
|  |\/|  | |  |  |  | |  |  |  ||   __|  |  |     |  |      /  /_\  \       \   \    |  |      /  /_\  \   |  |  |  ||   __|
|  |  |  | |  `--'  | |  '--'  ||  |____ |  `----.|  `----./  _____  \  .----)   |   |  `----./  _____  \  |  '--'  ||  |____
|__|  |__|  \______/  |_______/ |_______||_______| \______/__/     \__\ |_______/     \______/__/     \__\ |_______/ |_______|


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

def pull_model(model_name):
    """
    Attempt to pull a model using the `ollama pull` command.
    Retry up to MAX_RETRIES times if an error occurs.
    """
    retries = 0
    while retries < MAX_RETRIES:
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
            return True
        except subprocess.CalledProcessError as e:
            # Log the error
            logging.error(f"Error pulling model {model_name}: {e.stderr}")
            retries += 1
            if retries < MAX_RETRIES:
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logging.error(f"Failed to pull model {model_name} after {MAX_RETRIES} attempts.")
                return False

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

def main():
    """
    Main function to handle input and pull models.
    """
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

    # Pull models with progress bar
    success_count = 0
    failed_count = 0
    print(Fore.GREEN + "\nStarting model pull process...\n")
    try:
        for model in tqdm(models, desc="Pulling models", unit="model", ncols=100):
            if is_model_pulled(model):
                logging.info(f"Model {model} is already pulled. Skipping.")
                success_count += 1
                continue
            if pull_model(model):
                success_count += 1
            else:
                failed_count += 1
    except KeyboardInterrupt:
        print(Fore.RED + "\nProcess interrupted by user. Exiting gracefully.")
        sys.exit(0)

    # Display summary
    print(Fore.GREEN + "\nSummary:")
    print(Fore.GREEN + f"Successfully pulled models: {success_count}")
    print(Fore.RED + f"Failed to pull models: {failed_count}")

if __name__ == "__main__":
    main()
