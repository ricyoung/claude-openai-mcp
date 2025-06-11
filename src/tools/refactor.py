"""
Code refactoring tool using o3_pro
"""

from typing import Any, Dict
from .base import BaseTool
from ..prompts import get_prompt

class RefactorTool(BaseTool):
    """Refactor code for improved quality and maintainability"""
    
    @property
    def name(self) -> str:
        return "o3_refactor"
    
    @property
    def description(self) -> str:
        return "Refactor code using o3_pro to improve quality, readability, and maintainability while preserving functionality."
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code to refactor"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language"
                },
                "goals": {
                    "type": "string",
                    "description": "Specific refactoring goals (e.g., improve readability, reduce complexity, apply patterns)",
                    "optional": True
                },
                "constraints": {
                    "type": "string",
                    "description": "Any constraints or requirements to maintain",
                    "optional": True
                },
                "target_patterns": {
                    "type": "string",
                    "description": "Design patterns to apply (e.g., Strategy, Factory, Observer)",
                    "optional": True
                }
            },
            "required": ["code", "language"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        self._validate_arguments(arguments, ["code", "language"])
        
        code = arguments["code"]
        language = arguments["language"]
        goals = arguments.get("goals", "improve overall code quality")
        constraints = arguments.get("constraints", "")
        target_patterns = arguments.get("target_patterns", "")
        
        user_content = f"""Refactor the following {language} code:

```{language}
{code}
```

Refactoring Goals: {goals}"""

        if constraints:
            user_content += f"\nConstraints: {constraints}"
        
        if target_patterns:
            user_content += f"\nTarget Patterns: {target_patterns}"
        
        user_content += """

Provide the refactored code with explanations for significant changes.
Ensure the refactored code maintains the same functionality while improving quality."""
        
        system_prompt = get_prompt(self.name)
        
        return await self._execute_with_context(
            system_prompt,
            user_content,
            temperature=0.2
        )