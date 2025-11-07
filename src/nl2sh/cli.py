import asyncio

from nl2sh.utils import display_cli_command
from nl2sh.server.utils import start_and_wait_server_startup
from rich import print


def main():
    """Entry point of the cli tool."""

    # start and wait for the server.
    # works fine when the server is already running.
    asyncio.run(start_and_wait_server_startup())

    try:
        while True:
            print("\n> ", end="")
            prompt = input()

            # API calls and rendering
            if prompt.lower() in ["quit", "exit", "stop"]:
                return
            elif prompt == "":
                continue
            else:
                display_cli_command(prompt)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

    except Exception as e:
        print(f"{type(e)}: {e}")
