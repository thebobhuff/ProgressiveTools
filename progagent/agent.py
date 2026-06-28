"""
Core JIT Agent Execution Loop.
Manages tool registration, execution, and LLM orchestration.
"""
import os
import subprocess
import sys
import traceback
from rich.console import Console

console = Console()

class JITAgent:
    def __init__(self, llm, memory, tui=None):
        self.llm = llm
        self.memory = memory
        self.tui = tui
        self.messages = []
        self.tools = {}
        self.setup_tools()

    def setup_tools(self):
        """
        Registers core agent execution capabilities.
        """
        self.tools = {
            "list_directory": self.list_directory,
            "view_file": self.view_file,
            "search_directory": self.search_directory,
            "find_file": self.find_file,
            "create_file": self.create_file,
            "edit_file": self.edit_file,
            "run_command": self.run_command,
            "search_obsidian_vault": self.search_obsidian_vault,
        }

    def get_system_prompt(self) -> str:
        """
        Constructs the JIT instruction set and tool schemas.
        """
        tool_descriptions = (
            "- list_directory(directory_path: str)\n"
            "- view_file(file_path: str, start_line: int = 1, end_line: int = 100)\n"
            "- search_directory(query: str, directory_path: str)\n"
            "- find_file(name_pattern: str, directory_path: str)\n"
            "- create_file(file_path: str, content: str)\n"
            "- edit_file(file_path: str, target_content: str, replacement_content: str)\n"
            "- run_command(command: str)\n"
            "- search_obsidian_vault(query: str)\n"
        )
        
        return (
            "You are ProgAgent, a local developer agent running on a JIT Progressive Disclosure model.\n"
            "To optimize token count and efficiency, you must load files and code only when needed.\n"
            "\n"
            "Operational Guidelines:\n"
            "1. Read only the catalogs (INDEX.md) first to locate instructions, files, or custom scripts:\n"
            "   - Skills Catalog: agent/skills/INDEX.md (guides for specialized workflows like editing yourself)\n"
            "   - Tools Catalog: agent/tools/INDEX.md (scripts and CLI utilities available)\n"
            "   - Memories Catalog: agent/memories/INDEX.md (architectural overviews, docs)\n"
            "2. Read specific sub-folders or files only AFTER finding them in the catalog index.\n"
            "3. You have self-editing capability. You can view, edit, and create code files inside the workspace.\n"
            "\n"
            "Available Tools:\n"
            f"{tool_descriptions}\n"
            "You MUST call tools using XML-like tags matching this JSON layout:\n"
            "<tool_call>{\"name\": \"tool_name\", \"arguments\": {\"arg1\": \"value1\"}}</tool_call>\n"
            "Do not output markdown code blocks or conversational text around the tool call. "
            "Output ONE tool call at a time. After execution, you will receive the result and continue your turn."
        )

    async def step(self, user_prompt: str, live_render) -> str:
        """
        Main interactive turn-based loop. Evaluates LLM responses and executes tools.
        """
        self.messages.append({"role": "user", "content": user_prompt})
        
        # Log to chat
        if self.tui:
            self.tui.add_chat("user", user_prompt)
            self.tui.update_render()
            live_render.update(self.tui.layout)

        while True:
            system_prompt = self.get_system_prompt()
            response = self.llm.generate_chat(self.messages, system_prompt=system_prompt)
            
            # Check for error outputs (like Ollama offline)
            if response.startswith("[ERROR:"):
                if self.tui:
                    self.tui.add_chat("agent", response)
                    self.tui.update_render()
                    live_render.update(self.tui.layout)
                return response

            tool_calls = self.llm.parse_tool_calls(response)
            
            if not tool_calls:
                # No more tools to execute, final conversational response
                self.messages.append({"role": "assistant", "content": response})
                if self.tui:
                    self.tui.add_chat("agent", response)
                    self.tui.update_render()
                    live_render.update(self.tui.layout)
                return response

            # Execute the first parsed tool call
            tool_call = tool_calls[0]
            name = tool_call["name"]
            arguments = tool_call["arguments"]

            if self.tui:
                self.tui.log_jit("tool_call", f"Invoking {name}...")
                self.tui.update_render()
                live_render.update(self.tui.layout)

            # Check tool permission / approval if running command
            approved = True
            if name == "run_command":
                cmd = arguments.get("command", "")
                if self.tui:
                    approved = self.tui.prompt_approval(live_render, cmd)
                else:
                    # CLI default fallback
                    console.print(f"\n⚠️ JIT Request to Execute: {cmd}")
                    choice = input("Approve command execution? (y/n): ")
                    approved = choice.strip().lower() == 'y'

            if approved:
                try:
                    tool_result = self.execute_tool(name, arguments)
                except Exception as e:
                    tool_result = f"Error during tool execution: {e}\n{traceback.format_exc()}"
            else:
                tool_result = "Execution Denied by User."

            # Append the tool execution result back to messages
            self.messages.append({
                "role": "assistant", 
                "content": f"<tool_response>{tool_result}</tool_response>"
            })
            
            if self.tui:
                self.tui.log_jit("tool_response", f"{name} executed successfully.")
                self.tui.update_render()
                live_render.update(self.tui.layout)

    def execute_tool(self, name: str, arguments: dict) -> str:
        """
        Executes a registered tool by name.
        """
        tool_func = self.tools.get(name)
        if not tool_func:
            return f"Error: Tool '{name}' is not registered."
        return tool_func(**arguments)

    # --- Tool Implementations ---

    def list_directory(self, directory_path: str = ".") -> str:
        try:
            items = os.listdir(directory_path)
            # Differentiate directories from files
            out = []
            for item in sorted(items):
                full_path = os.path.join(directory_path, item)
                if os.path.isdir(full_path):
                    out.append(f"[DIR] {item}/")
                else:
                    out.append(f"[FILE] {item}")
            return "\n".join(out) if out else "(Empty Directory)"
        except Exception as e:
            return f"Error listing directory: {e}"

    def view_file(self, file_path: str, start_line: int = 1, end_line: int = 100) -> str:
        try:
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' does not exist."
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            start = max(1, start_line) - 1
            end = min(len(lines), end_line)
            
            view_lines = lines[start:end]
            numbered_lines = [f"{i + start + 1}: {line}" for i, line in enumerate(view_lines)]
            return "".join(numbered_lines) if numbered_lines else "(Empty Line Range)"
        except Exception as e:
            return f"Error viewing file: {e}"

    def search_directory(self, query: str, directory_path: str = ".") -> str:
        try:
            results = []
            for root, _, files in os.walk(directory_path):
                if ".git" in root or ".venv" in root:
                    continue
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            for idx, line in enumerate(f):
                                if query.lower() in line.lower():
                                    results.append(f"{filepath}:{idx + 1}: {line.strip()}")
                                    if len(results) >= 30: # Cap result list to keep prompt clean
                                        break
                    except Exception:
                        continue
            return "\n".join(results) if results else "No matches found."
        except Exception as e:
            return f"Error searching directory: {e}"

    def find_file(self, name_pattern: str, directory_path: str = ".") -> str:
        try:
            matches = []
            for root, _, files in os.walk(directory_path):
                for file in files:
                    if re.search(name_pattern, file, re.IGNORECASE):
                        matches.append(os.path.join(root, file))
            return "\n".join(matches) if matches else "No files found matching pattern."
        except Exception as e:
            return f"Error finding file: {e}"

    def create_file(self, file_path: str, content: str) -> str:
        try:
            dir_name = os.path.dirname(file_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Success: File '{file_path}' created."
        except Exception as e:
            return f"Error creating file: {e}"

    def edit_file(self, file_path: str, target_content: str, replacement_content: str) -> str:
        try:
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' does not exist."
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if target_content not in content:
                return "Error: Target content to replace not found in the file. Ensure indentation matches exactly."

            new_content = content.replace(target_content, replacement_content, 1)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"Success: File '{file_path}' modified."
        except Exception as e:
            return f"Error editing file: {e}"

    def run_command(self, command: str) -> str:
        try:
            res = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            out = f"STDOUT:\n{res.stdout}\n"
            if res.stderr:
                out += f"STDERR:\n{res.stderr}\n"
            return out
        except subprocess.TimeoutExpired:
            return "Error: Command execution timed out after 30 seconds."
        except Exception as e:
            return f"Error running command: {e}"

    def search_obsidian_vault(self, query: str) -> str:
        results = self.memory.search_vault(query)
        if not results:
            return "No matching obsidian notes found."
        
        output = []
        for r in results:
            if "error" in r:
                return r["error"]
            output.append(f"Note: {r['file']} (Relevance Score: {r['score']})\nSnippet: {r['snippets']}\n")
        return "\n".join(output)
