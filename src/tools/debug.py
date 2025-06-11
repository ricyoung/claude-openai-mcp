"""
Debug assistance tool using o3_pro
"""

from typing import Any, Dict
from .base import BaseTool
from ..prompts import get_prompt

class DebugTool(BaseTool):
    """Help debug code issues with o3_pro's reasoning capabilities"""
    
    @property
    def name(self) -> str:
        return "o3_debug"
    
    @property
    def description(self) -> str:
        return "Debug code issues using o3_pro's analytical reasoning. Provide code, error messages, and expected behavior."
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code with the bug"
                },
                "error": {
                    "type": "string",
                    "description": "Error message or unexpected behavior description"
                },
                "expected": {
                    "type": "string",
                    "description": "Expected behavior or output"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language"
                },
                "stack_trace": {
                    "type": "string",
                    "description": "Full stack trace if available",
                    "optional": True
                },
                "environment": {
                    "type": "string",
                    "description": "Environment details (OS, versions, etc.)",
                    "optional": True
                }
            },
            "required": ["code", "error", "expected", "language"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        self._validate_arguments(arguments, ["code", "error", "expected", "language"])
        
        code = arguments["code"]
        error = arguments["error"]
        expected = arguments["expected"]
        language = arguments["language"]
        stack_trace = arguments.get("stack_trace", "")
        environment = arguments.get("environment", "")
        
        user_content = f"""Debug the following {language} code:

```{language}
{code}
```

Error/Issue: {error}

Expected Behavior: {expected}"""

        if stack_trace:
            user_content += f"\n\nStack Trace:\n```\n{stack_trace}\n```"
        
        if environment:
            user_content += f"\n\nEnvironment: {environment}"
        
        user_content += "\n\nIdentify the root cause and provide a solution with corrected code."
        
        system_prompt = get_prompt(self.name)
        
        # Use reasoning mode for debugging
        result = await self.client.complete_with_reasoning(
            self._build_messages(system_prompt, user_content),
            reasoning_depth="high"
        )
        
        return f"{result['reasoning']}\n\n**Solution:**\n{result['answer']}"