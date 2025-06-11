"""
Base tool class for all OpenAI MCP tools
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

from ..openai_client import OpenAIClient

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """Abstract base class for all tools"""
    
    def __init__(self, config):
        self.config = config
        self.client = OpenAIClient(config)
        self._name = None
        self._description = None
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name as it appears in MCP"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for MCP"""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Return JSON schema for tool parameters"""
        pass
    
    @abstractmethod
    async def execute(self, arguments: Dict[str, Any]) -> str:
        """Execute the tool with given arguments"""
        pass
    
    def _validate_arguments(self, arguments: Dict[str, Any], required: list[str]) -> None:
        """Validate required arguments are present"""
        missing = [arg for arg in required if arg not in arguments]
        if missing:
            raise ValueError(f"Missing required arguments: {', '.join(missing)}")
    
    def _build_messages(self, system_prompt: str, user_content: str) -> list[Dict[str, str]]:
        """Build messages list for OpenAI API"""
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    
    async def _execute_with_context(
        self,
        system_prompt: str,
        user_content: str,
        **kwargs
    ) -> str:
        """Common execution pattern for most tools"""
        messages = self._build_messages(system_prompt, user_content)
        
        try:
            response = await self.client.complete(messages, **kwargs)
            return response
                
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            raise