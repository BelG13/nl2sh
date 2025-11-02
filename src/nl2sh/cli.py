import asyncio

from nl2sh.utils import cmd, display_cli_command
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

            # Tool calling
            if prompt:
                content_json = asyncio.run(cmd(prompt))
                display_cli_command(content_json)
            else:
                print("\nOperation cancelled by user.")
                break

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
