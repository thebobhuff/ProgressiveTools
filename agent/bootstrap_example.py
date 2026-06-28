#!/usr/bin/env python3
"""
Bootstrap Example for JIT Agent Progressive Disclosure System.
This file shows how to configure and initialize an Antigravity SDK Agent
to avoid upfront loading of skills and memories, forcing Just-In-Time discovery.
"""

import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy

async def custom_approval_handler(tool_call):
    """
    Handler to prompt for user approval when executing commands.
    """
    print(f"\n⚠️ Agent is requesting to execute: {tool_call.arguments.get('CommandLine')}")
    response = input("Approve execution? (y/n): ")
    return response.lower().strip() == 'y'

def get_jit_agent_config() -> LocalAgentConfig:
    # 1. Define JIT System Instructions
    # This instructs the agent to read AGENTS.md first and use the catalogs
    # rather than expecting all skills/tools to be pre-loaded in context.
    jit_system_instructions = (
        "You are operating in a Just-in-Time (JIT) Progressive Disclosure environment.\n"
        "1. DO NOT attempt to load all skill directories or search the entire workspace on startup.\n"
        "2. First, read the workspace guide at AGENTS.md to understand the JIT Protocol.\n"
        "3. Locate needed skills in agent/skills/INDEX.md, tools in agent/tools/INDEX.md, "
        "and memories/history in agent/memories/INDEX.md.\n"
        "4. View only the specific files returned by the indexes to complete your task."
    )

    # 2. Setup safety policies to restrict agent to core lookup tools by default
    # This disables other tools unless explicitly permitted, preventing broad actions.
    jit_policies = [
        policy.deny_all(),                  # Block everything by default
        policy.allow("list_directory"),     # Allow directory listing
        policy.allow("search_directory"),   # Allow file content searching (ripgrep)
        policy.allow("find_file"),          # Allow locating files by name
        policy.allow("view_file"),          # Allow viewing individual file contents
        policy.allow("finish"),             # Allow completing the task
        policy.allow("edit_file"),          # Allow file editing
        policy.allow("create_file"),        # Allow file creation
        # Setup interactive confirmation for command execution (needed to run tools/scripts)
        policy.ask_user("run_command", handler=custom_approval_handler),
    ]

    # 3. Create config. Note that `skills_paths` is left EMPTY so that
    # the SDK does not automatically search and load all skills into context at start.
    config = LocalAgentConfig(
        system_instructions=jit_system_instructions,
        policies=jit_policies,
        skills_paths=[],  # Empty! We load skills dynamically when needed via view_file.
    )
    
    return config

async def main():
    config = get_jit_agent_config()
    
    print("Bootstrapping JIT Agent...")
    async with Agent(config) as agent:
        # Prompt the agent to trigger the JIT protocol
        prompt = (
            "I need to run the example tool to greet 'Bob'. "
            "Please find the tool, inspect how to run it, and execute it."
        )
        print(f"\nUser Prompt: {prompt}\n")
        response = await agent.chat(prompt)
        print("\nAgent Response:")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
