import argparse
import asyncio

from nl2sh.utils import CLIArgs, cmd


def main():
    """Entry point of the cli tool."""

    # Arguments parsing
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("--prompt", type=str, help="Prompt to give to the SLM.")
    args = CLIArgs(parser.parse_args())

    # Tool calling
    if args.prompt:
        asyncio.run(cmd(args.prompt))
