---
name: obsidian_search
description: "Guidelines on when and how to search the Obsidian Vault to retrieve user knowledge, API configurations, or context."
---

# Obsidian Memory Search Skill

Use this skill when the user asks a question that requires background context, previous architectural decisions, credentials/API setup details, or personal configuration history that might be stored in the Obsidian vault notes.

## Steps

1. **Detect Need for Vault Context**: Identify if the user's prompt references custom configurations (e.g. "MS Graph", "credentials", "auth tokens", "personal setups").
2. **Execute search_obsidian_vault**: Invoke the tool:
   ```json
   <tool_call>{"name": "search_obsidian_vault", "arguments": {"query": "<relevant keyword or phrase>"}}</tool_call>
   ```
3. **Inspect Results**: Read the matching files, scores, and sentence snippets returned.
4. **View Specific File if Needed**: If the snippets are incomplete, use the `view_file` tool to inspect the full contents of the chosen note inside the vault (e.g., `obsidian_vault/target_note.md`).
5. **Formulate Response**: Use the retrieved knowledge to answer the user or complete the API setup.
