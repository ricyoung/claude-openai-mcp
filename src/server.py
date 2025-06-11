#!/usr/bin/env python3
"""
Claude-OpenAI MCP Server
Main entry point for the Model Context Protocol server that bridges Claude Code with OpenAI o3_pro
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.types as types

from tools import (
    CodeTool, AnalyzeTool, DebugTool, RefactorTool,
    ReviewTool, SafetyReviewTool, ReasoningTool
)
from config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenAIMCPServer:
    def __init__(self):
        self.server = Server("claude-openai-mcp")
        self.config = Config()
        self.tools = {}
        self._initialize_tools()
        self._setup_handlers()
    
    def _initialize_tools(self):
        """Initialize all available tools"""
        tool_classes = [
            CodeTool,
            AnalyzeTool,
            DebugTool,
            RefactorTool,
            ReviewTool,
            SafetyReviewTool,
            ReasoningTool
        ]
        
        for tool_class in tool_classes:
            tool = tool_class(self.config)
            self.tools[tool.name] = tool
            logger.info(f"Initialized tool: {tool.name}")
    
    def _setup_handlers(self):
        """Set up MCP protocol handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """Return list of available tools"""
            tools = []
            for tool in self.tools.values():
                tools.append(types.Tool(
                    name=tool.name,
                    description=tool.description,
                    inputSchema=tool.get_schema()
                ))
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str,
            arguments: Optional[Dict[str, Any]] = None
        ) -> list[types.TextContent]:
            """Handle tool execution requests"""
            if name not in self.tools:
                raise ValueError(f"Unknown tool: {name}")
            
            tool = self.tools[name]
            try:
                result = await tool.execute(arguments or {})
                return [types.TextContent(
                    type="text",
                    text=result
                )]
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [types.TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
    
    async def run(self):
        """Run the MCP server"""
        async with self.server.run_stdio():
            await self.server._stopped.wait()

def main():
    """Main entry point"""
    server = OpenAIMCPServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()