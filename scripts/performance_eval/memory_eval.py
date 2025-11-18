import subprocess
import argparse
import psutil
import time
import os


def monitor_external_script(script_to_run: list[str], verbose: bool = True):
    """
    Executes a given Python script and monitors the total RAM usage of its entire process tree.

    Args:
        script_to_run (list): A list containing the command and its arguments,
                                e.g., ['python', 'your_script.py'].
    """
    if not os.path.exists(script_to_run[1]):
        if verbose:
            print(f"Error: The script '{script_to_run[1]}' was not found.")
        return

    if verbose:
        print(f"Starting script: '{' '.join(script_to_run)}'")

    try:
        # Launch the user's script as a subprocess
        # Popen is used for non-blocking execution, so we can monitor it simultaneously.
        proc = subprocess.Popen(script_to_run)
        main_process = psutil.Process(proc.pid)

        if verbose:
            print(f"Main process started with PID: {main_process.pid}")

    except (psutil.NoSuchProcess, FileNotFoundError) as e:
        if verbose:
            print(f"Error starting process: {e}")
        return

    max_ram_usage = 0
    if verbose:
        print("Monitoring RAM usage...")

    try:
        # Loop as long as the main process of the user's script is running
        while main_process.is_running():
            total_ram_usage = 0

            # Use a try-except block to handle processes that might terminate
            # during the monitoring loop.
            try:
                # Get the parent process's memory
                total_ram_usage += main_process.memory_info().rss

                # Get all descendant processes (children, grandchildren, etc.)
                descendants = main_process.children(recursive=True)
                for child in descendants:
                    try:
                        total_ram_usage += child.memory_info().rss
                    except psutil.NoSuchProcess:
                        # This child terminated since we got the list, so we skip it.
                        continue

                # Update the maximum RAM usage if the current usage is higher
                if total_ram_usage > max_ram_usage:
                    max_ram_usage = total_ram_usage

                # Display the current total RAM usage in megabytes (MB)
                if verbose:
                    print(
                        f"\rCurrent Total RAM Usage: {total_ram_usage / (1024 * 1024):.2f} MB",
                        end="",
                    )

            except psutil.NoSuchProcess:
                # The main process terminated, so we break the loop.
                break

            # Poll for memory usage every half a second.
            time.sleep(0.5)

    except KeyboardInterrupt:
        if verbose:
            print("\nMonitoring stopped by user. Killing the subprocess.")
        main_process.kill()  # Terminate the subprocess if monitoring is interrupted

    finally:
        # Ensure the subprocess is terminated before exiting
        if main_process.is_running():
            main_process.wait()  # Wait for the process to finish naturally

        # A final check after the process has ended to capture last-moment memory usage
        if total_ram_usage > max_ram_usage:
            max_ram_usage = total_ram_usage

        if verbose:
            print(f"\n\nScript has finished.")
            print("=" * 50)
            print(
                f"Maximum RAM Usage of the entire process tree: {max_ram_usage / (1024 * 1024):.2f} MB"
            )
            print("=" * 50)


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
    monitor_external_script(
        ["python", "scripts/performance_eval/time_eval.py", "--verbose=0"],
        verbose=(args.verbose == 1),
    )
