import json
import os

# root = os.path.dirname(os.path.abspath(__name__))
# fewshots_path = os.path.join(root, "src", "nl2sh", "models", "fewshots.json")

# with open(fewshots_path, "r") as f:
#     fewshots = json.load(f)

# fewshots_text = "\n".join(
#     [f"EXAMPLE:\nINPUT: {item['nl']}\nOUTPUT:\n{item['output']}" for item in fewshots]
# )

system_prompt = f"""
You are a bash expert.
Your goal is to turn natural sentence into the corresponding bash commands.
"""
