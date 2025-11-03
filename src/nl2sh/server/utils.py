import os
import asyncio
import httpx
import subprocess
import getpass

from platformdirs import user_log_dir


def start_server():
    """Start the inference server."""

    # Get the standard log directory path
    log_dir = user_log_dir("nl2sh", getpass.getuser())
    os.makedirs(log_dir, exist_ok=True)

    app_location = "nl2sh.server.server:app"

    log_stdout_path = os.path.join(log_dir, "log_stdout.log")
    log_stderr_path = os.path.join(log_dir, "log_stdeer.log")

    process = subprocess.Popen(
        args=[
            "uvicorn",
            app_location,
        ],
        stdout=open(log_stdout_path, "w"),
        stderr=open(log_stderr_path, "w"),
    )

    print(f"Server process started with PID: {process.pid}.")


async def start_and_wait_server_startup():
    """Wait till the inference server is on."""

    server_already_started = False
    count = 0
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://127.0.0.1:8000/api/ready")
                response = response.json()

            if response["is_ready"]:
                return True
            else:
                await asyncio.sleep(2 ** (count := count + 1))

        except httpx.ConnectError:
            if not server_already_started:
                print("Starting the inference server...")
                start_server()
                server_already_started = True
            await asyncio.sleep(2 ** (count := count + 1))
