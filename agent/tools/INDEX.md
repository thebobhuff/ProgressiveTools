# JIT Custom Tools Catalog

This is the central index of all custom scripting utilities and developer tools available to agents in this workspace.

---

## 🔍 How to Use a Tool (Just-in-Time)

1. **Find a Tool**: Scan the **Available Tools** table below to find a tool that matches your required action.
2. **Read Usage**: Look at the parameters and execution instructions.
3. **Execute**: Run the script using the workspace command execution tool (e.g., `run_command` with `python3 agent/tools/...`).

---

## 🛠 Available Tools

| Tool Command / Script | Description | Parameters | Expected Output | Link to Script |
| :--- | :--- | :--- | :--- | :--- |
| `python3 agent/tools/example_tool.py` | A placeholder script illustrating CLI parameter handling. | `--name [str]` | Prints a greeting to console. | [example_tool.py](file:///Users/bobhuff/ProgressiveTools/agent/tools/example_tool.py) |
| `python3 agent/tools/lint_runner.py` | Parses a Python file to check syntax correctness and list elements missing docstrings. | `--file [str]` | Prints a syntax compile status and a list of functions/classes missing docstrings. | [lint_runner.py](file:///Users/bobhuff/ProgressiveTools/agent/tools/lint_runner.py) |

---

## 🆕 How to Add a New Tool

To add a new tool:
1. Create the script file in `agent/tools/` (e.g., `agent/tools/my_tool.py` or a shell script).
2. Ensure it is runnable and accepts standard command line arguments.
3. Document its parameters, purpose, and usage in this catalog table.
