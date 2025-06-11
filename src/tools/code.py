"""
Code generation tool using o3_pro
"""

from typing import Any, Dict
from .base import BaseTool
from ..prompts import get_prompt

class CodeTool(BaseTool):
    """Generate production-ready code using o3_pro's capabilities"""
    
    @property
    def name(self) -> str:
        return "o3_code"
    
    @property
    def description(self) -> str:
        return "Generate high-quality code with o3_pro's advanced reasoning. Provide requirements, language, and any specific constraints."
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "requirements": {
                    "type": "string",
                    "description": "Detailed description of what the code should do"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language (e.g., Python, JavaScript, TypeScript, Go, Rust)"
                },
                "context": {
                    "type": "string",
                    "description": "Additional context, existing code, or constraints",
                    "optional": True
                },
                "framework": {
                    "type": "string",
                    "description": "Specific framework to use (e.g., React, Django, Express)",
                    "optional": True
                },
                "style": {
                    "type": "string",
                    "description": "Coding style preferences (e.g., functional, OOP, procedural)",
                    "optional": True
                }
            },
            "required": ["requirements", "language"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        self._validate_arguments(arguments, ["requirements", "language"])
        
        requirements = arguments["requirements"]
        language = arguments["language"]
        context = arguments.get("context", "")
        framework = arguments.get("framework", "")
        style = arguments.get("style", "")
        
        # Build comprehensive prompt
        user_content = f"""Generate {language} code for the following requirements:

Requirements: {requirements}

Language: {language}"""

        if framework:
            user_content += f"\nFramework: {framework}"
        
        if style:
            user_content += f"\nStyle: {style}"
        
        if context:
            user_content += f"\n\nAdditional Context:\n{context}"
        
        user_content += "\n\nProvide complete, production-ready code with proper error handling and best practices."
        
        system_prompt = get_prompt(self.name)
        
        # Use higher temperature for creative code generation
        return await self._execute_with_context(
            system_prompt,
            user_content,
            temperature=0.3
        )