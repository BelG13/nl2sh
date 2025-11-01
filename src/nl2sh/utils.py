import httpx

from rich import print
from argparse import Namespace


class CLIArgs:
    def __init__(self, args: Namespace):
        assert hasattr(args, "prompt")
        self.prompt: str = args.prompt


async def cmd(prompt):
    """Prompt the model to generate a command."""

    url = "http://127.0.0.1:8000/api/generate-stream"
    data = {"prompt": prompt}

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, json=data) as response:
            async for chunk in response.aiter_text():
                print(f"[magenta]{chunk}[/magenta]", end="")
