import subprocess
import time
import logging
import sys

# Banner
BANNER = r"""
  __  __           _        ______                              
 |  \/  |         | |      |  ____|                             
 | \  / | ___   __| | ___  | |__   _ __ ___   __ _ _ __ ___  ___ 
 | |\/| |/ _ \ / _` |/ _ \ |  __| | '_ ` _ \ / _` | '__/ _ \/ __|
 | |  | | (_) | (_| |  __/ | |____| | | | | | (_| | | |  __/\__ \
 |_|  |_|\___/ \__,_|\___| |______|_| |_| |_|\__,_|_|  \___||___/
"""

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
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
    print("Enter model names (one per line). Press Enter twice to finish:")
    while True:
        model = input().strip()
        if not model:
            break
        models.append(model)
    return models

def main():
    """
    Main function to handle input and pull models.
    """
    print(BANNER)
    print("Welcome to ModelCascade! Let's pull some models.\n")

    # Ask the user for input method
    print("Choose an input method:")
    print("1. Enter model names manually")
    print("2. Provide a file containing model names")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        models = get_models_from_user()
    elif choice == "2":
        file_path = input("Enter the path to the file: ").strip()
        models = get_models_from_file(file_path)
    else:
        logging.error("Invalid choice. Exiting.")
        sys.exit(1)

    if not models:
        logging.error("No models provided. Exiting.")
        sys.exit(1)

    # Pull models
    for model in models:
        success = pull_model(model)
        if not success:
            logging.error(f"Skipping model {model} due to repeated failures.")
        logging.info("Moving to the next model...\n")

if __name__ == "__main__":
    main()
