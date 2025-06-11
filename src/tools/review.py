"""
Code review tool using o3_pro
"""

from typing import Any, Dict
from .base import BaseTool
from ..prompts import get_prompt

class ReviewTool(BaseTool):
    """Perform comprehensive code reviews"""
    
    @property
    def name(self) -> str:
        return "o3_review"
    
    @property
    def description(self) -> str:
        return "Conduct thorough code reviews using o3_pro. Evaluates correctness, quality, security, and adherence to best practices."
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code to review"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language"
                },
                "type": {
                    "type": "string",
                    "description": "Type of code (e.g., feature, bugfix, refactor)",
                    "optional": True
                },
                "pr_description": {
                    "type": "string",
                    "description": "Pull request description or change context",
                    "optional": True
                },
                "standards": {
                    "type": "string",
                    "description": "Specific coding standards to check against",
                    "optional": True
                }
            },
            "required": ["code", "language"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        self._validate_arguments(arguments, ["code", "language"])
        
        code = arguments["code"]
        language = arguments["language"]
        code_type = arguments.get("type", "general")
        pr_description = arguments.get("pr_description", "")
        standards = arguments.get("standards", "")
        
        user_content = f"""Review the following {language} code:

```{language}
{code}
```

Code Type: {code_type}"""

        if pr_description:
            user_content += f"\n\nPR Description:\n{pr_description}"
        
        if standards:
            user_content += f"\n\nCoding Standards:\n{standards}"
        
        user_content += """

Provide a detailed review with:
1. Issues found (with severity: critical, major, minor, suggestion)
2. Specific line references where applicable
3. Recommended fixes
4. Overall assessment"""
        
        system_prompt = get_prompt(self.name)
        
        return await self._execute_with_context(
            system_prompt,
            user_content,
            temperature=0.1
        )