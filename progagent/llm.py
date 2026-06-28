"""
Ollama Local LLM Client and Tool Call Parser.
Supports structured tool-calling formatting and zero-dependency HTTP communication.
"""
import json
import re
import urllib.error
import urllib.request

class OllamaClient:
    def __init__(self, model="hermes3", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate_chat(self, messages, system_prompt=None) -> str:
        """
        Sends chat history to local Ollama instance and returns the model response.
        """
        url = f"{self.base_url}/api/chat"
        
        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        payload_messages.extend(messages)

        data = {
            "model": self.model,
            "messages": payload_messages,
            "stream": False,
            "options": {
                "temperature": 0.1  # Low temperature for precise code execution and tool-calling
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as res:
                response = json.loads(res.read().decode('utf-8'))
                return response.get("message", {}).get("content", "")
        except urllib.error.URLError as e:
            return (
                f"[ERROR: Could not connect to local Ollama instance at {self.base_url}. "
                f"Please ensure Ollama is running and the model '{self.model}' is pulled.\n"
                f"Details: {e}]"
            )

    def parse_tool_calls(self, content: str) -> list:
        """
        Parses custom XML-like tool call tags from the model output.
        Format: <tool_call>{"name": "tool_name", "arguments": {...}}</tool_call>
        """
        tool_calls = []
        pattern = re.compile(r'<tool_call>(.*?)</tool_call>', re.DOTALL)
        matches = pattern.findall(content)
        
        for match in matches:
            try:
                call_data = json.loads(match.strip())
                if "name" in call_data:
                    tool_calls.append({
                        "name": call_data["name"],
                        "arguments": call_data.get("arguments", {})
                    })
            except json.JSONDecodeError:
                # Fallback: attempt to extract JSON using a regex if there's syntax fluff
                json_match = re.search(r'\{.*\}', match, re.DOTALL)
                if json_match:
                    try:
                        call_data = json.loads(json_match.group(0))
                        if "name" in call_data:
                            tool_calls.append({
                                "name": call_data["name"],
                                "arguments": call_data.get("arguments", {})
                            })
                    except json.JSONDecodeError:
                        pass
        return tool_calls

    def get_tool_call_instructions(self) -> str:
        """
        Returns system instructions teaching the model how to make tool calls.
        """
        return (
            "You are equipped with custom workspace tools. When you need to call a tool, "
            "you MUST output your request in XML-like tags matching the following structure:\n"
            "<tool_call>{\"name\": \"tool_name\", \"arguments\": {\"arg1\": \"value1\"}}</tool_call>\n"
            "Only output the tool call tag when a tool is actually required. Do not print markdown surrounding the tool call."
        )
