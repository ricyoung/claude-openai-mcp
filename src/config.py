"""
Configuration management for Claude-OpenAI MCP
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the MCP server"""
    
    def __init__(self):
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.openai_model: str = os.getenv("OPENAI_MODEL", "o3-pro")
        self.openai_base_url: Optional[str] = os.getenv("OPENAI_BASE_URL")
        
        # Model parameters
        self.temperature: float = float(os.getenv("TEMPERATURE", "0.2"))
        self.max_tokens: int = int(os.getenv("MAX_TOKENS", "100000"))  # o3-pro supports up to 100k
        self.top_p: float = float(os.getenv("TOP_P", "0.95"))
        
        # Reasoning depth levels
        self.reasoning_depth: str = os.getenv("REASONING_DEPTH", "medium")  # low, medium, high
        
        # Safety
        self.safety_threshold: str = os.getenv("SAFETY_THRESHOLD", "medium")  # low, medium, high
        
        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # Validate configuration
        self._validate()
    
    def _validate(self):
        """Validate required configuration"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        if self.reasoning_depth not in ["low", "medium", "high"]:
            raise ValueError("REASONING_DEPTH must be 'low', 'medium', or 'high'")
        
        if self.safety_threshold not in ["low", "medium", "high"]:
            raise ValueError("SAFETY_THRESHOLD must be 'low', 'medium', or 'high'")