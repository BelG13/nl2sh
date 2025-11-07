import httpx
import json
import re
import os
import subprocess
import asyncio

from json_repair import repair_json

from rich import print
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text


async def get_commands(prompt: str):
    """Prompt the model to generate a command."""

    url = "http://127.0.0.1:8000/api/generate-stream"
    data = {"prompt": prompt}
    content = ""

    # Stream the text in the terminal
    # TODO: remove streaming - not needed anymore.
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, json=data) as response:
            async for chunk in response.aiter_text():
                content += chunk
                # print(f"[magenta]{chunk}[/magenta]", end="")

    # Parse the result
    content_json = re.findall(pattern=r"{.*}", string=content, flags=re.DOTALL)
    if not len(content_json):
        print("[red]Error while searching for the match.[/red]")
        return {}

    if not (content_json := repair_json(content_json[0])):
        print("[red]Error while cleaning the slm response")
        return {}

    return json.loads(content_json)


def display_cli_command(prompt: str):
    """
    Displays the model's response in a nested panel layout, asks for
    confirmation, and executes the commands.
    """

    console = Console()
    danger_map = {
        0: {"color": "green", "description": "Harmless (Read-only)"},
        1: {"color": "bright_green", "description": "Low Risk (Creation/Navigation)"},
        2: {"color": "yellow", "description": "Moderate Risk (Permissions/Execution)"},
        3: {"color": "orange3", "description": "High Risk (Deletion/Overwrite)"},
        4: {"color": "dark_orange", "description": "Very High Risk (System Changes)"},
        5: {"color": "bold red", "description": "Maximum Danger (Irreversible)"},
    }

    while True:
        # --- 1. Extract data and set up danger level styles ---
        response_data = asyncio.run(get_commands(prompt))
        commands = response_data.get("command", [])
        danger_level = response_data.get("danger_level", 0)

        if not commands:
            console.print(
                Panel(
                    "[bold red]Error: The model did not return any commands.[/bold red]",
                    border_style="red",
                )
            )

            user_confirmation = Confirm.ask(
                "\nDo you want to regenerate the command(s) ?", default=False
            )
            if user_confirmation:
                continue
            return

        danger_info = danger_map.get(danger_level, danger_map[5])

        # --- 2. Build the nested panel structure ---
        command_display_str = (
            "\n".join(f"{i + 1}. {cmd}" for i, cmd in enumerate(commands))
            if len(commands) > 1
            else commands[0]
        )

        command_sub_panel = Panel(
            Text(command_display_str, style="bright_white"),
            title="[bold blue]Bash Command(s)[/bold blue]",
            border_style="blue",
            expand=False,
            padding=(1, 2),
        )

        danger_text = Text.from_markup(
            f"\n[{danger_info['color']}]"
            f"Danger Level: {danger_level} - {danger_info['description']}"
            f"[/{danger_info['color']}]"
        )

        # A Group makes multiple rich renderables act as a single unit
        panel_content = Group(command_sub_panel, danger_text)

        main_panel = Panel(
            panel_content,
            title="[bold cyan]NL2SH Command Center[/bold cyan]",
            border_style="cyan",
            padding=1,
        )

        # --- 3. Display the main panel and ask for confirmation ---
        console.print(main_panel)

        try:
            # Describe each option
            console.print("\n[bold]Available actions:[/bold]")
            console.print("[green]y[/green]: Execute the command(s)")
            console.print("[red]n[/red]: Cancel")
            console.print("[yellow]r[/yellow]: Regenerate the command(s)")

            user_confirmation = Prompt.ask(
                "\nDo you want to execute the command(s)?",
                default="n",
                choices=["y", "n", "r"],
                case_sensitive=False,
            )
        except KeyboardInterrupt:
            console.print("\n[bold red]❌ Execution cancelled by user.[/bold red]")
            return

        # --- 4. Take actions based on user confirmation ---

        # Abort the execution
        if user_confirmation == "n":
            console.print("[bold red]❌ Execution cancelled by user.[/bold red]")
            return

        # Regenerate the commands
        if user_confirmation == "r":
            continue

        # Execute the commands
        console.print("\n[bold green]Executing...[/bold green]")
        for cmd in commands:
            console.print(f"Running: [yellow]{cmd}[/yellow]")

            # Special handling for 'cd' remains
            if cmd.strip().startswith("cd "):
                try:
                    path = cmd.strip().split(maxsplit=1)[1]
                    os.chdir(os.path.expanduser(path))
                    console.print(
                        Panel(
                            f"Changed directory to: {os.getcwd()}",
                            title="[green]✅ Success[/green]",
                            border_style="green",
                        )
                    )
                except Exception as e:
                    console.print(
                        Panel(
                            f"Error executing 'cd': {e}",
                            title="[red]❌ Error[/red]",
                            border_style="red",
                        )
                    )
                    break
                continue

            # Use subprocess.run to wait for the command to complete and capture its output
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            # Display stdout in a success panel
            if result.stdout:
                console.print(
                    Panel(
                        result.stdout.strip(),
                        title=f"[green]✅ Output for: {cmd}[/green]",
                        border_style="green",
                    )
                )

            # Display stderr in an error panel and halt execution
            if result.stderr:
                console.print(
                    Panel(
                        result.stderr.strip(),
                        title=f"[red]❌ Error for: {cmd}[/red]",
                        border_style="red",
                    )
                )
                console.print(
                    "[bold red]Halting execution of further commands.[/bold red]"
                )
                break

        return
