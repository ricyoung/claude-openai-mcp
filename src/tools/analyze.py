"""
Code analysis tool using o3_pro
"""

from typing import Any, Dict
from .base import BaseTool
from ..prompts import get_prompt

class AnalyzeTool(BaseTool):
    """Analyze code for quality, performance, and best practices"""
    
    @property
    def name(self) -> str:
        return "o3_analyze"
    
    @property
    def description(self) -> str:
        return "Perform comprehensive code analysis using o3_pro. Identifies issues, suggests improvements, and evaluates code quality."
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code to analyze"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language of the code"
                },
                "focus": {
                    "type": "string",
                    "description": "Specific aspect to focus on (e.g., performance, security, maintainability)",
                    "optional": True
                },
                "context": {
                    "type": "string",
                    "description": "Additional context about the codebase or requirements",
                    "optional": True
                }
            },
            "required": ["code", "language"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        self._validate_arguments(arguments, ["code", "language"])
        
        code = arguments["code"]
        language = arguments["language"]
        focus = arguments.get("focus", "")
        context = arguments.get("context", "")
        
        user_content = f"""Analyze the following {language} code:

```{language}
{code}
```

Language: {language}"""

        if focus:
            user_content += f"\nFocus Area: {focus}"
        
        if context:
            user_content += f"\n\nContext:\n{context}"
        
        user_content += "\n\nProvide a comprehensive analysis with specific recommendations."
        
        system_prompt = get_prompt(self.name)
        
        return await self._execute_with_context(
            system_prompt,
            user_content,
            temperature=0.1  # Lower temperature for analytical tasks
        )