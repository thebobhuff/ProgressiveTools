# JIT Skills Catalog

This is the central index of all custom skills available to agents in this workspace.

---

## 🔍 How to Use a Skill (Just-in-Time)

1. **Find a Match**: Scan the **Available Skills** table below to see if any matches your sub-task.
2. **Retrieve Instructions**: View the `SKILL.md` file inside the corresponding skill directory (e.g. `agent/skills/my_skill/SKILL.md`).
3. **Execute**: Follow the workflow or instructions defined inside the skill's instructions.

---

## 🛠 Available Skills

| Skill Folder Name | Description / Scope | Trigger Keywords | Link to Skill Instructions |
| :--- | :--- | :--- | :--- |
| `example_skill` | A placeholder demonstrating the skill structure. | `template`, `demo`, `tutorial` | [SKILL.md](file:///Users/bobhuff/ProgressiveTools/agent/skills/example_skill/SKILL.md) |
| `code_quality` | Standard code quality, syntax, and docstring coverage checker. | `lint`, `format`, `docstring`, `code review` | [SKILL.md](file:///Users/bobhuff/ProgressiveTools/agent/skills/code_quality/SKILL.md) |
| `obsidian_search` | Search Obsidian vault notes for credentials, configurations, and memory context. | `obsidian`, `vault`, `search notes`, `knowledge` | [SKILL.md](file:///Users/bobhuff/ProgressiveTools/agent/skills/obsidian_search/SKILL.md) |
| `self_edit` | Guidelines and safety check procedures for modifying ProgAgent source code. | `edit yourself`, `self-edit`, `modify source`, `upgrade` | [SKILL.md](file:///Users/bobhuff/ProgressiveTools/agent/skills/self_edit/SKILL.md) |

---

## 🆕 How to Add a New Skill

To add a new skill to the workspace:
1. Create a subfolder inside `agent/skills/` (e.g., `agent/skills/my_new_skill/`).
2. Create a `SKILL.md` file inside that subfolder.
3. Write standard instruction steps and YAML frontmatter in `SKILL.md`.
4. Add a new row to this table with the details and link to the file.
