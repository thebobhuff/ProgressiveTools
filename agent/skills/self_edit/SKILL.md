---
name: self_edit
description: "Guidelines and safety procedures for editing, updating, and extending the ProgAgent framework's own code files."
---

# Agent Self-Editing Code Skill

Use this skill when the user asks you to modify your own code, add features to the TUI, expand Ollama parameters, or change tool execution behavior.

## Steps

1. **Locate Target Module**: Use `find_file` or search the directories to locate the correct file inside the `progagent/` codebase (e.g. `progagent/agent.py` or `progagent/tui.py`).
2. **Inspect Existing Implementation**: Read the target file using `view_file` around the lines you want to modify to understand the structure, imports, and indentation.
3. **Plan Changes**: Write down the exact lines to replace. Ensure that you maintain PEP8 python styling and do not break imports.
4. **Apply Changes**: Use the `edit_file` tool to replace the target code. Avoid replacing the entire file; perform precise edits:
   ```json
   <tool_call>{"name": "edit_file", "arguments": {"file_path": "progagent/agent.py", "target_content": "<old lines>", "replacement_content": "<new lines>"}}</tool_call>
   ```
5. **Verify Syntax and Functionality**: 
   Run a syntax check using `python3 -m py_compile <file_path>` or run tests using `run_command`.
6. **Error Recovery**: If the compiler reports a syntax error, immediately inspect the logs, identify the mistake, and apply a correction. Do not leave the workspace code in a broken state.
