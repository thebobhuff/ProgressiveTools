"""
Command Line Entrypoint for ProgAgent.
Launches the Live Console TUI and orchestrates the JIT Agent run loop.
"""
import argparse
import asyncio
import os
import sys
from rich.console import Console
from rich.live import Live

from progagent.agent import JITAgent
from progagent.llm import OllamaClient
from progagent.memory import ObsidianMemory
from progagent.tui import ProgAgentTUI

console = Console()

def setup_dummy_vault(vault_path: str):
    """
    Creates a sample Obsidian vault with a demonstration note if it doesn't exist.
    """
    if not os.path.exists(vault_path):
        os.makedirs(vault_path)
        note_content = (
            "# Microsoft Graph Integration Guidelines\n"
            "This document logs the JIT specifications for MS Graph integration.\n"
            "Endpoint Target: https://graph.microsoft.com/v1.0/me\n"
            "Required Permissions: User.Read, Mail.Read, Calendars.ReadWrite\n"
            "Flow: Use oauth2 device-code flow or authorization-code flow to get token.\n"
        )
        with open(os.path.join(vault_path, "MS_Graph_API.md"), "w", encoding='utf-8') as f:
            f.write(note_content)

async def run_tui(args):
    setup_dummy_vault(args.vault)

    # Initialize modules
    llm = OllamaClient(model=args.model, base_url=args.ollama_url)
    memory = ObsidianMemory(vault_path=args.vault)
    tui = ProgAgentTUI(model_name=args.model)
    agent = JITAgent(llm=llm, memory=memory, tui=tui)

    # Boot logs
    tui.add_chat("Agent", "Hello! I am ProgAgent, your JIT local coding assistant. How can I help you today?")
    tui.log_jit("init", "ProgAgent JIT core initialized. Standby.")
    tui.update_render()

    with Live(tui.layout, console=console, refresh_per_second=4, screen=True) as live:
        while True:
            tui.update_render()
            live.update(tui.layout)
            
            # Fetch user prompt (TUI handles stopping Live render safely)
            user_input = tui.prompt_user(live)
            if not user_input.strip():
                continue
            
            if user_input.strip().lower() in ("exit", "quit"):
                tui.add_chat("Agent", "Goodbye!")
                tui.update_render()
                live.update(tui.layout)
                await asyncio.sleep(1)
                break
            
            # Execute step
            await agent.step(user_input, live)

def main():
    parser = argparse.ArgumentParser(description="ProgAgent: Local JIT Developer Agent")
    parser.add_argument("--model", default="hermes3", help="Ollama model name (e.g. hermes3, llama3.1)")
    parser.add_argument("--vault", default="./obsidian_vault", help="Obsidian vault directory path")
    parser.add_argument("--ollama-url", default="http://localhost:11434", help="Ollama API base URL")
    args = parser.parse_args()

    try:
        asyncio.run(run_tui(args))
    except KeyboardInterrupt:
        print("\nExiting ProgAgent...")

if __name__ == "__main__":
    main()
