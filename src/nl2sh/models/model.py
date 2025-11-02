import threading
import os

from nl2sh.models.config import system_prompt
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from peft import PeftModel


def get_model_and_tokenizer() -> tuple[AutoTokenizer, AutoModelForCausalLM]:
    """Load the model and the tokenizer."""

    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    adapter_path = "BelGio13/Qwen2.5-0.5B-sft-nl2sh"

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    base_model = AutoModelForCausalLM.from_pretrained(
        model_name, device_map="auto", torch_dtype="auto"
    )
    model = PeftModel.from_pretrained(base_model, adapter_path)
    model.eval()

    return model, tokenizer


def generate_stream(model, tokenizer, prompt):
    """Prepare and start the generation."""

    # Prepare the system prompt
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {"role": "user", "content": prompt},
    ]

    # Apply the template
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    streamer = TextIteratorStreamer(
        tokenizer=tokenizer, skip_prompt=True, skip_special_tokens=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generation_kwargs = {**model_inputs, "max_new_tokens": 512, "streamer": streamer}

    # Starting the thread for generating the tokens
    t = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    t.start()

    return streamer
