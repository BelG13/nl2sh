import asyncio
import os
import torch
import time
import signal
import json
import argparse

from nl2sh.utils import get_commands
from nl2sh.server.utils import start_and_wait_server_startup
from typing import Literal


def run_eval(verbose: Literal[True, False] = True):
    """Entry point of the cli tool."""

    if verbose:
        print("\n", "=" * 30 + " TIME EVALUATION " + "=" * 30)

    # start and wait for the server.
    start_time = time.time()
    pid = asyncio.run(start_and_wait_server_startup(verbose=False))
    startup_time = time.time() - start_time

    # We run our test on the following prompt list.
    prompts = [
        "Show me all the files in the current directory",
        "Display IP address and login time of the current user's session",
        "Display a garbled ascii-art of a cow saying 'hello' backwards",
        "Find all *.py files under current directory",
    ]

    # Evaluation loop
    times = []
    char_count = []

    for prompt in prompts:
        try:
            start_time = time.time()
            json_response = asyncio.run(get_commands(prompt))
            times.append(time.time() - start_time)
            char_count.append(len(json.dumps(json_response)))

        # Unexcpected error (ex. The model generated an answer in the wrong format)
        # are discarted in the time evaluation.
        except Exception as e:
            pass

    # Stop the inference server
    os.kill(pid, signal.SIGTERM)

    # get time statistics
    times = torch.Tensor(times)
    average_response_time = times.mean()
    std_response_time = times.std()

    # get length statistics
    char_count = torch.Tensor(char_count)
    average_response_length = char_count.mean()
    std_response_length = char_count.std()

    if verbose:
        print(f"Startup time : {startup_time} seconds")
        print(
            f"Average response time : {average_response_time:2f} ± {std_response_time:2f} seconds"
        )
        print(
            f"Average response length : {average_response_length:2f} ± {std_response_length:2f} seconds"
        )
        print(
            f"Average character per second : {(average_response_length / average_response_time):2f} char/s"
        )
        print("=" * 30 + " END TIME EVALUATION " + "=" * 30, "\n")

    return {
        "eval_response_time": [average_response_time, std_response_time],
        "eval_response_length": [average_response_length, std_response_length],
        "char_per_second": average_response_time / average_response_length,
    }


if __name__ == "__main__":
    # For downstream tasks (ex. Memory evaluation)
    # we don't want this model to have any verbosity.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose",
        type=int,
        choices=[0, 1],
        default=1,
        help="Verbosity level of the evaluation script.",
    )
    args = parser.parse_args()
    run_eval(args.verbose)
