import os
import asyncio
import httpx
import subprocess


def start_server():
    """Start the inference server."""

    current_dir = os.getcwd()
    root_dir = os.path.dirname(os.path.abspath(__name__))
    app_location = "src.nl2sh.server.server:app"

    os.chdir(root_dir)
    os.makedirs("logs", exist_ok=True)

    process = subprocess.Popen(
        args=[
            "uvicorn",
            app_location,
        ],
        stdout=open(os.path.join(root_dir, "logs", "log_stdout.log"), "w"),
        stderr=open(os.path.join(root_dir, "logs", "log_stderr.log"), "w"),
    )
    os.chdir(current_dir)

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
            print("Starting the inference server...")
            if not server_already_started:
                start_server()
                server_already_started = True
            await asyncio.sleep(2 ** (count := count + 1))
