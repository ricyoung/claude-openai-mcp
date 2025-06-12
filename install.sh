#!/bin/bash

# Claude-OpenAI MCP Easy Installer for macOS
# This script installs and configures the Claude-OpenAI MCP server

set -e

echo "🚀 Claude-OpenAI MCP Installer for macOS"
echo "========================================"
echo

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}Error: This installer is for macOS only${NC}"
    exit 1
fi

# Check for Python 3.8+
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}Error: Python $PYTHON_VERSION is installed, but Python 3.8+ is required${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"

# Default installation directory
DEFAULT_DIR="$HOME/claude-openai-mcp"

# Check if running in a pipe/non-interactive mode
if [ -t 0 ]; then
    # Interactive mode - prompt for directory
    echo
    read -p "Installation directory [$DEFAULT_DIR]: " INSTALL_DIR
    INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_DIR}
else
    # Non-interactive mode - use default
    echo
    echo "Using default installation directory: $DEFAULT_DIR"
    INSTALL_DIR="$DEFAULT_DIR"
fi

# Create directory if it doesn't exist
mkdir -p "$(dirname "$INSTALL_DIR")"

# Clone or update repository
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Directory exists. Updating...${NC}"
    cd "$INSTALL_DIR"
    git pull origin main
else
    echo "Cloning repository..."
    git clone https://github.com/ricyoung/claude-openai-mcp.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# Create virtual environment
echo
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Get OpenAI API key
echo
echo -e "${YELLOW}⚠️  IMPORTANT: o3-pro pricing${NC}"
echo "   Input: \$20.00 per 1M tokens"
echo "   Output: \$80.00 per 1M tokens"
echo "   Requests may take several minutes to complete"
echo

if [ -t 0 ]; then
    # Interactive mode - prompt for API key
    read -p "Enter your OpenAI API key (or press Enter to skip): " OPENAI_API_KEY
else
    # Non-interactive mode - skip API key prompt
    echo "Skipping API key prompt (non-interactive mode)"
    echo "You can set your API key later in the .env file"
    OPENAI_API_KEY=""
fi

# Create .env file
if [ -n "$OPENAI_API_KEY" ]; then
    cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=$OPENAI_API_KEY
OPENAI_MODEL=o3-pro

# Model Parameters
TEMPERATURE=0.2
MAX_TOKENS=100000  # o3-pro supports up to 100k output tokens
TOP_P=0.95

# Reasoning Configuration
REASONING_DEPTH=medium  # low, medium, high

# Safety Settings
SAFETY_THRESHOLD=medium  # low, medium, high

# Logging
LOG_LEVEL=INFO
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${YELLOW}Skipping .env creation. You'll need to create it manually.${NC}"
fi

# Configure based on what's available
if command -v claude &> /dev/null; then
    # Claude CLI is available - skip desktop config
    echo
    echo "Claude Code CLI detected - configuration will be done manually"
    SKIP_CONFIG=true
else
    # Configure Claude Desktop
    echo
    echo "Configuring Claude Desktop..."
    SKIP_CONFIG=false
    CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
fi

if [ "$SKIP_CONFIG" != "true" ]; then
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${YELLOW}Claude Desktop config not found. Creating...${NC}"
        mkdir -p "$(dirname "$CONFIG_FILE")"
        echo '{"mcpServers": {}}' > "$CONFIG_FILE"
    fi

    # Create temporary config with our server
    TEMP_CONFIG=$(mktemp)
    PYTHON_PATH="$INSTALL_DIR/venv/bin/python"
    SERVER_PATH="$INSTALL_DIR/launch_mcp.py"

    # Use Python to safely merge JSON
    python3 << EOF
import json
import os

config_file = "$CONFIG_FILE"
temp_file = "$TEMP_CONFIG"
python_path = "$PYTHON_PATH"
server_path = "$SERVER_PATH"
api_key = "$OPENAI_API_KEY"

# Read existing config
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except:
    config = {}

# Ensure mcpServers exists
if 'mcpServers' not in config:
    config['mcpServers'] = {}

# Add our server
config['mcpServers']['claude-openai-mcp'] = {
    "command": python_path,
    "args": [server_path]
}

# Add env if API key provided
if api_key:
    config['mcpServers']['claude-openai-mcp']['env'] = {
        "OPENAI_API_KEY": api_key
    }

# Write config
with open(temp_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✓ Configuration updated")
EOF

    # Backup existing config and install new one
    if [ -f "$CONFIG_FILE" ]; then
        cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
        echo -e "${GREEN}✓ Backed up existing config to $CONFIG_FILE.backup${NC}"
    fi

    mv "$TEMP_CONFIG" "$CONFIG_FILE"
fi  # End of SKIP_CONFIG check

# Create convenient launcher script
cat > "$INSTALL_DIR/start-server.sh" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
source venv/bin/activate
python src/server.py
EOF
chmod +x "$INSTALL_DIR/start-server.sh"

# Final instructions
echo
echo -e "${GREEN}✅ Installation complete!${NC}"
echo

# If Claude CLI is available, provide manual instructions
if command -v claude &> /dev/null; then
    echo
    echo -e "${YELLOW}To add to Claude Code CLI, run this command:${NC}"
    echo
    echo "cat > /tmp/claude-openai-mcp.json << 'EOF'"
    echo "{"
    echo "  \"mcpServers\": {"
    echo "    \"claude-openai-mcp\": {"
    echo "      \"command\": \"$INSTALL_DIR/venv/bin/python\","
    echo "      \"args\": [\"$INSTALL_DIR/launch_mcp.py\"]"
    echo "    }"
    echo "  }"
    echo "}"
    echo "EOF"
    echo
    echo "claude code config add /tmp/claude-openai-mcp.json"
    echo "rm /tmp/claude-openai-mcp.json"
    echo
fi

echo "Next steps:"
echo "1. If using Claude Desktop app, restart it for changes to take effect"
echo "2. If using Claude Code CLI, run: claude mcp list"
echo "3. You should see 'claude-openai-mcp' in the MCP menu"
echo
echo "Available tools:"
echo "  • o3_code     - Generate production-ready code"
echo "  • o3_analyze  - Analyze code for improvements"
echo "  • o3_debug    - Debug code issues"
echo "  • o3_refactor - Refactor code"
echo "  • o3_review   - Review code quality"
echo "  • o3_safety   - Security analysis"
echo "  • o3_reasoning - Complex problem solving"
echo
echo -e "${YELLOW}⚠️  Remember: o3-pro requests can take several minutes and are expensive${NC}"
echo
echo "For manual server start: $INSTALL_DIR/start-server.sh"
echo "Configuration file: $CONFIG_FILE"
echo "Environment file: $INSTALL_DIR/.env"