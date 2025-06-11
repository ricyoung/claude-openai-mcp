"""
OpenAI API client wrapper for o3_pro model
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
import aiohttp
import json

logger = logging.getLogger(__name__)

class OpenAIClient:
    """Wrapper for OpenAI API with o3_pro optimizations using Responses API"""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.openai_api_key
        self.base_url = config.openai_base_url or "https://api.openai.com"
        self.model = config.openai_model
        
    async def complete(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Send completion request to OpenAI Responses API (v1/responses)
        Note: o3-pro doesn't support streaming and may take several minutes
        
        Args:
            messages: List of chat messages
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            top_p: Override default top_p
            **kwargs: Additional parameters for the API
        
        Returns:
            Completion text
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # o3-pro uses the Responses API endpoint
        url = f"{self.base_url}/v1/responses"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
            "top_p": top_p or self.config.top_p,
            **kwargs
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Set a long timeout for o3-pro as it can take several minutes
                timeout = aiohttp.ClientTimeout(total=600)  # 10 minutes
                
                async with session.post(
                    url, 
                    headers=headers, 
                    json=payload,
                    timeout=timeout
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Extract response from the Responses API format
                        if "choices" in data and data["choices"]:
                            return data["choices"][0]["message"]["content"] or ""
                        else:
                            logger.error(f"Unexpected response format: {data}")
                            return "Error: Unexpected response format"
                    else:
                        error_text = await response.text()
                        logger.error(f"OpenAI API error: {response.status} - {error_text}")
                        raise Exception(f"API Error: {response.status} - {error_text}")
                        
        except asyncio.TimeoutError:
            logger.error("Request timed out. o3-pro can take several minutes for complex requests.")
            raise Exception("Request timed out. Try using background mode for long-running requests.")
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def complete_with_reasoning(
        self,
        messages: List[Dict[str, str]],
        reasoning_depth: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Complete with explicit reasoning steps (for o3_pro)
        o3-pro naturally provides reasoning in its responses
        
        Returns dict with 'reasoning' and 'answer' keys
        """
        depth = reasoning_depth or self.config.reasoning_depth
        
        # Add reasoning instruction based on depth
        reasoning_prompts = {
            "low": "Think step by step.",
            "medium": "Think through this carefully, showing your reasoning process.",
            "high": "Provide detailed reasoning, exploring multiple approaches and trade-offs before arriving at your answer."
        }
        
        # Modify the last user message to include reasoning instruction
        messages_copy = messages.copy()
        if messages_copy and messages_copy[-1]["role"] == "user":
            messages_copy[-1]["content"] = f"{messages_copy[-1]['content']}\n\n{reasoning_prompts[depth]}"
        
        response = await self.complete(messages_copy, **kwargs)
        
        # Parse reasoning and answer
        # o3-pro typically includes reasoning in its responses
        parts = response.split("\n\n")
        if len(parts) >= 2:
            return {
                "reasoning": "\n\n".join(parts[:-1]),
                "answer": parts[-1]
            }
        else:
            return {
                "reasoning": "",
                "answer": response
            }