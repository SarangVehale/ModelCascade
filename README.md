# ModelCascade 🚀

ModelCascade is a Python script designed to automate the process of pulling Ollama models using the `ollama pull` command. It supports retries, skips, graceful exits, and provides a user-friendly interface with progress tracking and colored output.

---

## Features ✨

- **Automated Model Pulling**: Pull multiple Ollama models sequentially.
- **Retry Mechanism**: Automatically retries failed pulls up to 5 times.
- **Skip Functionality**: Skip the current model during the process by pressing `s`.
- **Exit Functionality**: Gracefully exit the script at any time by pressing `e`.
- **Progress Bar**: Visual progress bar using `tqdm`.
- **Colored Output**: Enhanced UI with colored logs and messages using `colorama`.
- **Input Flexibility**: Accept model names via manual input or from a file.
- **Validation**: Validate model names to ensure they are not empty or malformed.
- **Summary Report**: Display a summary of successful, failed, and skipped pulls at the end.
- **Logging**: Save logs to a file (`modelcascade.log`) for future reference.

---

## Installation 🛠️

### Prerequisites
- Python 3.6 or higher.
- The `ollama` command-line tool must be installed and available in your system's PATH.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/SarangVehale/ModelCascade.git
   cd modelcascade
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python modelcascade.py
   ```

---

## Usage 🖥️

### Running the Script
1. Start the script:
   ```bash
   python modelcascade.py
   ```

2. Choose an input method:
   - **Manual Input**: Enter model names one by line. Press Enter twice to finish.
   - **File Input**: Provide the path to a file containing model names (one per line).

3. During the process:
   - Press `s` and Enter to skip the current model.
   - Press `e` and Enter to exit the script gracefully.

4. View the summary report at the end.

### Example
```bash
$ python modelcascade.py

  __  __           _        ______                              
 |  \/  |         | |      |  ____|                             
 | \  / | ___   __| | ___  | |__   _ __ ___   __ _ _ __ ___  ___ 
 | |\/| |/ _ \ / _` |/ _ \ |  __| | '_ ` _ \ / _` | '__/ _ \/ __|
 | |  | | (_) | (_| |  __/ | |____| | | | | | (_| | | |  __/\__ \
 |_|  |_|\___/ \__,_|\___| |______|_| |_| |_|\__,_|_|  \___||___/

Welcome to ModelCascade! Let's pull some models.

Choose an input method:
1. Enter model names manually
2. Provide a file containing model names
Enter your choice (1 or 2): 1
Enter model names (one per line). Press Enter twice to finish:
model1
model2
model3

Starting model pull process...

Press 's' and Enter to skip the current model.
Press 'e' and Enter to exit the script.

Pulling models:  33%|████████████████▌                          | 1/3 [00:05<00:10,  5.00s/model]
Successfully pulled model: model1
Pulling models:  67%|██████████████████████████████▍            | 2/3 [00:10<00:05,  5.00s/model]
s
Skipping current model...
Pulling models: 100%|████████████████████████████████████████| 3/3 [00:15<00:00,  5.00s/model]
Failed to pull model: model3

Summary:
✅ Successfully pulled models: 1
❌ Failed to pull models: 1
⏩ Skipped models: 1
```

---

## Requirements 📦

- Python 3.6+
- `tqdm` (for progress bar)
- `colorama` (for colored output)

Install the requirements using:
```bash
pip install -r requirements.txt
```

---

## Contributing 🤝

Contributions are welcome! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments 🙏

- Thanks to the creators of `tqdm` and `colorama` for their amazing libraries.
- Inspired by the need for automation in model management.

---

Happy modeling! 🎉


