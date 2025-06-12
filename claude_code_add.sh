#!/bin/bash

# Script to add claude-openai-mcp to Claude Code

echo "Adding claude-openai-mcp to Claude Code..."

# Create a config file for Claude Code to add
cat > /tmp/claude-openai-mcp-config.json << EOF
{
  "mcpServers": {
    "claude-openai-mcp": {
      "command": "$HOME/claude-openai-mcp/venv/bin/python",
      "args": ["$HOME/claude-openai-mcp/launch_mcp.py"]
    }
  }
}
EOF

# Use Claude Code CLI to add the config
claude code config add /tmp/claude-openai-mcp-config.json

# Clean up
rm /tmp/claude-openai-mcp-config.json

echo "Done! Run 'claude mcp list' to verify."