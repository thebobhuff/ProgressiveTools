#!/usr/bin/env python3
"""
AST-based Code Quality and Docstring Checker.
Verifies syntax correctness and checks that all classes, methods, and functions 
possess docstrings.
"""
import argparse
import ast
import os
import sys

def check_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error: Could not read file: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        tree = ast.parse(content)
    except SyntaxError as se:
        print("--- CODE QUALITY REPORT ---")
        print("Status: Syntax Check FAILED")
        print(f"Error: {se.msg} (line {se.lineno}, column {se.offset})")
        if se.text:
            print(f"Code context: {se.text.strip()}")
        sys.exit(0)

    print("--- CODE QUALITY REPORT ---")
    print("Status: Syntax Check PASSED\n")

    missing_docstrings = []
    total_elements = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total_elements += 1
            name = node.name
            doc = ast.get_docstring(node)
            elem_type = "Class" if isinstance(node, ast.ClassDef) else "Function/Method"
            if not doc:
                missing_docstrings.append((elem_type, name, node.lineno))

    print(f"Total checked (Classes/Functions/Methods): {total_elements}")
    if missing_docstrings:
        print(f"Found {len(missing_docstrings)} element(s) missing docstrings:")
        for elem_type, name, lineno in missing_docstrings:
            print(f"  - [{elem_type}] '{name}' on line {lineno}")
    else:
        print("✅ Success! All classes, methods, and functions have docstrings.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AST Code Quality Checker")
    parser.add_argument("--file", required=True, help="Path to Python file to analyze")
    args = parser.parse_args()
    check_file(args.file)
