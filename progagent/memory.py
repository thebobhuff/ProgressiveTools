"""
Obsidian Vault Memory Reader.
Recursively searches local markdown vault notes for query terms, providing JIT text snippets.
"""
import os
import re

class ObsidianMemory:
    def __init__(self, vault_path=None):
        self.vault_path = vault_path or os.environ.get("OBSIDIAN_VAULT_PATH", "./obsidian_vault")

    def search_vault(self, query: str, max_results=5) -> list:
        """
        Recursively scans the vault path for markdown files matching query terms.
        Returns a ranked list of matches with file info, scores, and matching snippet sentences.
        """
        results = []
        if not self.vault_path or not os.path.exists(self.vault_path):
            return [{"error": f"Obsidian Vault path '{self.vault_path}' does not exist."}]

        query_words = [word.lower() for word in re.findall(r'\w+', query)]
        if not query_words:
            return []

        for root, dirs, files in os.walk(self.vault_path):
            # Skip hidden system folders (e.g. .obsidian, .git)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception:
                        continue

                    filename_lower = file.lower()
                    content_lower = content.lower()
                    
                    score = 0
                    # Weight filename matches highly
                    for word in query_words:
                        if word in filename_lower:
                            score += 15
                        score += content_lower.count(word)

                    if score > 0:
                        snippets = []
                        # Extract sentences surrounding query words
                        for word in query_words:
                            # Match sentence structure containing the query word
                            sentence_pattern = rf'([^.!?\n]*?{re.escape(word)}[^.!?\n]*?[.!?\n])'
                            match = re.search(sentence_pattern, content, re.IGNORECASE)
                            if match:
                                sentence = match.group(1).strip().replace('\r', '').replace('\n', ' ')
                                if sentence not in snippets:
                                    snippets.append(sentence)
                                if len(snippets) >= 2:
                                    break
                        
                        relative_path = os.path.relpath(filepath, self.vault_path)
                        results.append({
                            "file": relative_path,
                            "score": score,
                            "snippets": " ... ".join(snippets) if snippets else content[:200].strip().replace('\n', ' ') + "..."
                        })

        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_results]
