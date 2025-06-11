"""
OpenAI API client wrapper for o3_pro model
"""

import asyncio
import logging
from typing import Any, AsyncIterator, Dict, List, Optional, Union

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

logger = logging.getLogger(__name__)

class OpenAIClient:
    """Wrapper for OpenAI API with o3_pro optimizations"""
    
    def __init__(self, config):
        self.config = config
        self.client = AsyncOpenAI(
            api_key=config.openai_api_key,
            base_url=config.openai_base_url
        )
        self.model = config.openai_model
    
    async def complete(
        self,
        messages: List[ChatCompletionMessageParam],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        stream: Optional[bool] = None,
        **kwargs
    ) -> Union[str, AsyncIterator[str]]:
        """
        Send completion request to OpenAI API
        
        Args:
            messages: List of chat messages
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            top_p: Override default top_p
            stream: Override default streaming setting
            **kwargs: Additional parameters for the API
        
        Returns:
            Completion text or async iterator for streaming
        """
        try:
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature or self.config.temperature,
                "max_tokens": max_tokens or self.config.max_tokens,
                "top_p": top_p or self.config.top_p,
                **kwargs
            }
            
            stream = stream if stream is not None else self.config.enable_streaming
            
            if stream:
                return self._stream_completion(params)
            else:
                response = await self.client.chat.completions.create(**params)
                return response.choices[0].message.content or ""
                
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _stream_completion(self, params: Dict[str, Any]) -> AsyncIterator[str]:
        """Handle streaming completion"""
        params["stream"] = True
        
        try:
            stream = await self.client.chat.completions.create(**params)
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            raise
    
    async def complete_with_reasoning(
        self,
        messages: List[ChatCompletionMessageParam],
        reasoning_depth: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Complete with explicit reasoning steps (for o3_pro)
        
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
        # This is a simplified version - you might want more sophisticated parsing
        if isinstance(response, str):
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
        else:
            # Handle streaming case
            full_response = ""
            async for chunk in response:
                full_response += chunk
            
            parts = full_response.split("\n\n")
            if len(parts) >= 2:
                return {
                    "reasoning": "\n\n".join(parts[:-1]),
                    "answer": parts[-1]
                }
            else:
                return {
                    "reasoning": "",
                    "answer": full_response
                }