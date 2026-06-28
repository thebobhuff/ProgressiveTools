"""
TUI Console for ProgAgent using Python Rich.
Renders a live dual-pane layout showing the Chat interface on the left and 
the JIT progressive disclosure activity console on the right.
"""
import sys
import time
from datetime import datetime
from queue import Queue
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

console = Console()

class ProgAgentTUI:
    def __init__(self, model_name="hermes3"):
        self.model_name = model_name
        self.chat_history = []
        self.jit_logs = []
        self.layout = Layout()
        self.log_queue = Queue()
        self.setup_layout()

    def setup_layout(self):
        """
        Configures the rich layout split panes.
        """
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        self.layout["body"].split_row(
            Layout(name="chat", ratio=3),
            Layout(name="jit", ratio=2)
        )

    def add_chat(self, sender: str, message: str):
        """
        Adds a message to the chat view.
        """
        color = "cyan" if sender.lower() == "user" else "green"
        self.chat_history.append((sender, message, color))

    def log_jit(self, category: str, action: str):
        """
        Logs a JIT action (e.g., skill index consulted, tool executed) to the side panel.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.jit_logs.append((timestamp, category, action))
        # Keep logs list size managed
        if len(self.jit_logs) > 30:
            self.jit_logs.pop(0)

    def get_header(self) -> Panel:
        grid = Text.assemble(
            ("● ", "green bold blink"),
            ("PROGAGENT CORE ", "bold white"),
            (f"| Model: {self.model_name} | Local JIT Engine Running", "dim white")
        )
        return Panel(grid, style="blue")

    def get_footer(self) -> Panel:
        return Panel(
            Text("Commands: [Type prompt & press Enter] | Ctrl+C to Exit", style="dim white"),
            style="blue"
        )

    def get_chat_panel(self) -> Panel:
        text = Text()
        for sender, msg, color in self.chat_history[-15:]:  # Show last 15 messages
            text.append(f"[{sender.upper()}] ", style=f"{color} bold")
            text.append(f"{msg}\n\n", style="white")
        return Panel(text, title="💬 Chat History", border_style="cyan")

    def get_jit_panel(self) -> Panel:
        text = Text()
        for ts, category, action in self.jit_logs[-15:]:
            text.append(f"[{ts}] ", style="dim white")
            text.append(f"[{category.upper()}] ", style="magenta bold")
            text.append(f"{action}\n", style="yellow")
        return Panel(text, title="⚙️ JIT Discovery Log", border_style="magenta")

    def update_render(self):
        self.layout["header"].update(self.get_header())
        self.layout["chat"].update(self.get_chat_panel())
        self.layout["jit"].update(self.get_jit_panel())
        self.layout["footer"].update(self.get_footer())

    def prompt_user(self, live: Live) -> str:
        """
        Suspends Live render to safely fetch user terminal input, then resumes.
        """
        live.stop()
        try:
            user_input = console.input("\n[bold cyan]Prompt > [/]")
            # Clear input line
            print("\033[A\033[2K", end="")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting ProgAgent...")
            sys.exit(0)
        live.start()
        return user_input

    def prompt_approval(self, live: Live, command: str) -> bool:
        """
        Asks user to approve command execution.
        """
        live.stop()
        console.print(f"\n[bold yellow]⚠️ JIT Request to Execute: {command}[/]")
        try:
            choice = console.input("[bold yellow]Approve execution? (y/n): [/]").strip().lower()
            print("\033[A\033[2K\033[A\033[2K", end="")  # Clear prompt lines
        except (KeyboardInterrupt, EOFError):
            choice = 'n'
        live.start()
        return choice == 'y'
