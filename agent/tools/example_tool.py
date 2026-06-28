#!/usr/bin/env python3
"""
Example Tool Script
Demonstrates a CLI utility registered in agent/tools/INDEX.md.
"""
import argparse

def main():
    parser = argparse.ArgumentParser(description="Example tool for JIT agent discovery demo.")
    parser.add_argument("--name", type=str, default="Agent", help="Name to greet")
    args = parser.parse_args()
    
    print(f"Hello, {args.name}! The example tool executed successfully.")

if __name__ == "__main__":
    main()
