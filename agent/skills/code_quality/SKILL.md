---
name: code_quality
description: "Guidelines and steps to check Python file structures, syntax, and docstring coverage using the lint_runner tool."
---

# Code Quality and Documentation Review

Use this skill when you need to inspect the quality, syntax validity, or docstring coverage of a Python module in the workspace.

## Prerequisites
- The target python file must exist in the workspace.
- The `agent/tools/lint_runner.py` script must be available.

## Steps

1. **Locate the Target File**: Identify the absolute or relative path to the Python file that needs review.
2. **Execute Lint Check**: Run the lint analysis tool by executing the following command:
   ```bash
   python3 agent/tools/lint_runner.py --file <target_file_path>
   ```
3. **Parse results**:
   - **Syntax check**: Verify the compile status. If `Failed`, review the specific syntax error line and fix it.
   - **Docstring coverage**: Check the list of functions/classes missing docstrings.
4. **Fix Issues**:
   - For syntax errors: fix the code.
   - For missing docstrings: add descriptive docstrings to the classes/functions.
5. **Re-Run Validation**: Re-run the command from Step 2 to verify that all issues have been successfully resolved.
