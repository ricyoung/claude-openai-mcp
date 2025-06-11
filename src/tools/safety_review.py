"""
Safety and security review tool using o3_pro
"""

from typing import Any, Dict
from .base import BaseTool
from ..prompts import get_prompt

class SafetyReviewTool(BaseTool):
    """Perform security and safety analysis of code"""
    
    @property
    def name(self) -> str:
        return "o3_safety"
    
    @property
    def description(self) -> str:
        return "Conduct security and safety reviews using o3_pro. Identifies vulnerabilities, security risks, and potential safety issues."
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code to review for safety and security"
                },
                "language": {
                    "type": "string",
                    "description": "Programming language"
                },
                "context": {
                    "type": "string",
                    "description": "Application context (e.g., web app, API, library)",
                    "optional": True
                },
                "sensitivity": {
                    "type": "string",
                    "description": "Data sensitivity level (e.g., public, internal, confidential)",
                    "optional": True
                },
                "compliance": {
                    "type": "string",
                    "description": "Compliance requirements (e.g., OWASP, PCI-DSS, HIPAA)",
                    "optional": True
                }
            },
            "required": ["code", "language"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> str:
        self._validate_arguments(arguments, ["code", "language"])
        
        code = arguments["code"]
        language = arguments["language"]
        context = arguments.get("context", "general application")
        sensitivity = arguments.get("sensitivity", "")
        compliance = arguments.get("compliance", "")
        
        user_content = f"""Perform a security and safety review of the following {language} code:

```{language}
{code}
```

Application Context: {context}"""

        if sensitivity:
            user_content += f"\nData Sensitivity: {sensitivity}"
        
        if compliance:
            user_content += f"\nCompliance Requirements: {compliance}"
        
        user_content += """

Provide a comprehensive security analysis including:
1. Vulnerabilities found (with severity: critical, high, medium, low)
2. Specific security risks and attack vectors
3. Remediation recommendations with code examples
4. Best practices to prevent similar issues
5. Overall security posture assessment"""
        
        system_prompt = get_prompt(self.name)
        
        # Use high reasoning depth for security analysis
        result = await self.client.complete_with_reasoning(
            self._build_messages(system_prompt, user_content),
            reasoning_depth="high"
        )
        
        return f"**Security Analysis:**\n{result['reasoning']}\n\n**Findings and Recommendations:**\n{result['answer']}"