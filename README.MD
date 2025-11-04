# 🧠 nl2sh : Your Offline AI Terminal Assistant

**nl2sh** is a command-line tool that translates your natural language instructions into validated shell commands. Powered by a lightweight, fine-tuned language model, it operates **entirely offline**, ensuring your data and command history never leave your machine.

Think of it as a smart, private assistant for your terminal.

---

## ✨ Key Features

-   🌍 **Fully Offline & Private**: Your instructions are processed locally. No API calls are made, and no data is sent to the cloud.
-   ⚡ **Lightweight & Fast**: Built to run efficiently on standard hardware, powered by a fine-tuned **Qwen2-0.5B-Instruct** model.
-   ✅ **Interactive Command Approval**: Never run a command blindly. nl2sh presents the generated command for your approval before execution.
-   🐍 **Modern Tech Stack**: Built with Python, Transformers, and FastAPI for a robust and maintainable foundation.

---

## ⚠️ A Note on the Current Model

The current version of the model is fine-tuned on the [`nl2bash` dataset](https://github.com/TellinaTool/nl2bash), which makes it highly proficient at generating a wide range of system-level shell commands (file manipulation, searching, system info, etc.).

However, it has **not yet been specifically fine-tuned on daily developer workflows**. While it might generate correct commands for tools like `git`, `docker`, `conda`, or `kubectl`, its performance on these is not yet optimized. Enhancing its capabilities for these real-world developer tools is the top priority for the next release.

---

## 🛠️ Installation

> pip install nl2sh

---

## 💻 Usage

Launch the interactive CLI directly from your terminal:

```bash
nl2sh
```

Then, type what you want to do in plain English. For example:

```
> list all the python files in the current directory.
```

nl2sh will process your request and suggest a command.

You can then **validate** (`y`) or **reject** (`n`) the command interactively.

#### **Controls**

-   Press **Enter** to submit your instruction.
-   Press **Ctrl + C** or leave empty to quit.

---

## 🚀 Performance Evaluation

We provide scripts to evaluate the model's performance on your machine.

### Memory Usage

To monitor the peak RAM consumed by the application during a session, run:

```bash
python scripts/performance_eval/memory_eval.py
```

Here is an example in my case (M4 Pro):
```
Starting script: 'python scripts/performance_eval/time_eval.py --verbose=0'
Main process started with PID: 36640
Monitoring RAM usage...
Current Total RAM Usage: 1469.66 MB

Script has finished.
==================================================
Maximum RAM Usage of the entire process tree: 1469.66 MB
==================================================
```

### Execution Speed

To measure the average time taken from instruction to command generation, run:

```bash
python scripts/performance_eval/time_eval.py
```

Here is a exemple in my case (M4 Pro):
```
============================== TIME EVALUATION ==============================
Startup time : 6.061269998550415 seconds
Average response time : 0.659301 ± 0.196201 seconds
Average response length : 43.500000 ± 19.841036 seconds
Average character per second : 65.978935 char/s
============================== END TIME EVALUATION ==============================
```

---

## 🗺️ Roadmap

| Feature | Description |
| :--- | :--- |
| 🧠 **User Context Awareness** | Allow the model to remember past commands within a session to adapt future generations to your workflow. |
| 🔁 **Mistake Regeneration** | If a generated command is incorrect, you'll be able to trigger a refined version without re-typing the query. |
| 🎯 **Improved Fine-Tuning** | The next training round will focus on realistic, everyday developer commands for tools (ex. `git`, `docker`, `aws`, `conda`, `kubectl`, `ffmpeg`) and a more natural language than the one the model have been finetuned on. |
| ⚙️ **Configurable Models** | Add a configuration file to allow users to specify different local models or LoRA adapters, enabling those with more powerful hardware (CPU/GPU) to leverage larger models. |

---

## 🧠 Model & Training Details

For more details about the models and the training details you can take a look at :

-   **Base Model**: [Qwen2-0.5B-Instruct on Hugging Face](https://huggingface.co/Qwen/Qwen2-0.5B-Instruct)
-   **Fine-tuned Adapters**: [Adapters on Hugging Face](https://huggingface.co/BelGio13/Qwen2.5-0.5B-sft-nl2sh)
-   **Fine-tuning results**: [Train and eval metrics values](https://wandb.ai/belv/nl2sh-sft)

The model was trained on the [`nl2bash` dataset](https://github.com/TellinaTool/nl2bash), a curated collection of natural language prompts and their corresponding Bash commands.

---

## 🤝 Contributing

Contributions are welcome! To get started with local development:

```bash
# Clone the repository
git clone https://github.com/BelGio13/nl2sh.git
cd nl2sh

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # (use venv\Scripts\activate on Windows)

# Install in editable mode
pip install -e .
```

Feel free to open issues or submit pull requests.

---

## 📚 Technologies Used

-   [Transformers (Hugging Face)](https://huggingface.co/transformers/)
-   [PyTorch](https://pytorch.org/)
-   [FastAPI](https://fastapi.tiangolo.com/)
-   Python 3.12

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🧑‍💻 Author

**Giovanni Belval**
<br>Machine Learning Engineer | Researcher
<br>[LinkedIn](https://www.linkedin.com/in/giovanni-belval-71551a169/) · [GitHub](https://github.com/BelGio13) · [X (Twitter)](https://x.com/b_gioo)
