"""
Deep reasoning tool using o3_pro's advanced capabilities
"""

from typing import Any, Dict
from .base import BaseTool
from ..prompts import get_prompt

class ReasoningTool(BaseTool):
    """Apply o3_pro's deep reasoning to complex programming problems"""
    
    @property
    def name(self) -> str:
        return "o3_reasoning"
    
    @property
    def description(self) -> str:
        return "Use o3_pro's advanced reasoning for complex problem-solving, architecture decisions, and technical analysis."
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "problem": {
                    "type": "string",
                    "description": "The complex problem or question to solve"
                },
                "context": {
                    "type": "string",
                    "description": "Relevant context, constraints, or background information",
                    "optional": True
                },
                "constraints": {
                    "type": "string",
                    "description": "Specific constraints or requirements",
                    "optional": True
                },
                "options": {
                    "type": "string",
                    "description": "Potential solutions or approaches to evaluate",
                    "optional": True
                },
                "depth": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Reasoning depth (default: high)",
                    "optional": True
                }
            },
            "required": ["problem"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        self._validate_arguments(arguments, ["problem"])
        
        problem = arguments["problem"]
        context = arguments.get("context", "")
        constraints = arguments.get("constraints", "")
        options = arguments.get("options", "")
        depth = arguments.get("depth", "high")
        
        user_content = f"""Solve the following problem using deep reasoning:

Problem: {problem}"""

        if context:
            user_content += f"\n\nContext:\n{context}"
        
        if constraints:
            user_content += f"\n\nConstraints:\n{constraints}"
        
        if options:
            user_content += f"\n\nPotential Approaches:\n{options}"
        
        user_content += """

Apply systematic reasoning to:
1. Analyze the problem thoroughly
2. Consider multiple approaches
3. Evaluate trade-offs
4. Recommend the best solution with justification
5. Provide implementation guidance"""
        
        system_prompt = get_prompt(self.name)
        
        # Always use complete_with_reasoning for this tool
        result = await self.client.complete_with_reasoning(
            self._build_messages(system_prompt, user_content),
            reasoning_depth=depth
        )
        
        return f"**Reasoning Process:**\n{result['reasoning']}\n\n**Recommendation:**\n{result['answer']}"