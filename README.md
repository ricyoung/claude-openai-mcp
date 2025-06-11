# Claude-OpenAI MCP Server

A Model Context Protocol (MCP) server that bridges Claude Code with OpenAI's o3-pro model, providing advanced coding capabilities through specialized tools.

## ⚠️ Important: About o3-pro

**Pricing:** o3-pro is expensive!
- Input: $20.00 per 1M tokens
- Output: $80.00 per 1M tokens
- A single complex request could cost several dollars

**Performance:**
- Requests may take **several minutes** to complete
- o3-pro uses extensive compute for deep reasoning
- No streaming support - you'll need to wait for the full response

## 🚀 Quick Install (macOS)

```bash
curl -sSL https://raw.githubusercontent.com/ricyoung/claude-openai-mcp/main/install.sh | bash
```

This will:
1. Install the MCP server
2. **Prompt you for your OpenAI API key** (or you can add it later)
3. Configure Claude Code automatically
4. Create all necessary files

After installation, restart Claude Code and look for "claude-openai-mcp" in the MCP menu.

### Setting Your API Key

**During installation:** The installer will prompt you:
```
Enter your OpenAI API key (or press Enter to skip): 
```

**After installation:** If you skipped or need to update your key:
```bash
# Option 1: Edit the .env file
echo "OPENAI_API_KEY=your-key-here" > ~/claude-openai-mcp/.env

# Option 2: Or set it as an environment variable
export OPENAI_API_KEY="your-key-here"
```

## Features

### 🛠️ Specialized Coding Tools

1. **o3_code** - Advanced code generation with deep reasoning
2. **o3_analyze** - Comprehensive code analysis and optimization suggestions
3. **o3_debug** - Debug assistance with root cause analysis
4. **o3_refactor** - Intelligent code refactoring
5. **o3_review** - Thorough code reviews with best practices
6. **o3_safety** - Security and safety vulnerability analysis
7. **o3_reasoning** - Complex problem-solving with structured reasoning

### 🚀 Key Capabilities

- **Deep Reasoning**: Leverages o3-pro's advanced reasoning capabilities
- **Configurable Reasoning Depth**: Adjust reasoning level (low/medium/high)
- **Safety-First Approach**: Built-in security review capabilities
- **Production-Ready**: Comprehensive error handling and logging
- **Long Timeout Support**: Handles o3-pro's extended processing times

## Prerequisites

- macOS (installer is macOS-specific)
- Python 3.8 or higher
- OpenAI API key with o3-pro access
- Claude Code installed

## Manual Installation

If you prefer not to use the automatic installer:

### 1. Clone and Setup

```bash
git clone https://github.com/ricyoung/claude-openai-mcp.git
cd claude-openai-mcp
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional (defaults shown)
OPENAI_MODEL=o3-pro
TEMPERATURE=0.2
MAX_TOKENS=100000  # o3-pro supports up to 100k output tokens
TOP_P=0.95
REASONING_DEPTH=medium  # low, medium, high
SAFETY_THRESHOLD=medium  # low, medium, high
LOG_LEVEL=INFO
```

### 4. Configure Claude Code

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "claude-openai-mcp": {
      "command": "/path/to/claude-openai-mcp/venv/bin/python",
      "args": ["/path/to/claude-openai-mcp/src/server.py"]
    }
  }
}
```

Then restart Claude Code.

## Usage Examples

### Code Generation

```
Use o3_code to create a Python web scraper that extracts product information from e-commerce sites with rate limiting and error handling.
```

### Code Analysis

```
Use o3_analyze to review this JavaScript function for performance bottlenecks and suggest optimizations.
```

### Debugging

```
Use o3_debug to help me fix this TypeScript error: "Type 'string' is not assignable to type 'number'". The code is trying to parse user input.
```

### Security Review

```
Use o3_safety to review this authentication code for security vulnerabilities and OWASP compliance.
```

### Complex Reasoning

```
Use o3_reasoning to help me design a scalable microservices architecture for a real-time chat application with 1M+ concurrent users.
```

## Tool Details

### o3_code - Code Generation

Generates production-ready code with proper error handling and best practices.

**Parameters:**
- `requirements` (required): Detailed description of functionality
- `language` (required): Programming language
- `context`: Additional context or constraints
- `framework`: Specific framework to use
- `style`: Coding style preferences

### o3_analyze - Code Analysis

Performs comprehensive code analysis for quality and optimization.

**Parameters:**
- `code` (required): Code to analyze
- `language` (required): Programming language
- `focus`: Specific aspect (performance, security, maintainability)
- `context`: Additional codebase context

### o3_debug - Debug Assistance

Helps identify and fix bugs with detailed reasoning.

**Parameters:**
- `code` (required): Code with the bug
- `error` (required): Error message or behavior
- `expected` (required): Expected behavior
- `language` (required): Programming language
- `stack_trace`: Full stack trace
- `environment`: Environment details

### o3_refactor - Code Refactoring

Improves code quality while maintaining functionality.

**Parameters:**
- `code` (required): Code to refactor
- `language` (required): Programming language
- `goals`: Specific refactoring goals
- `constraints`: Requirements to maintain
- `target_patterns`: Design patterns to apply

### o3_review - Code Review

Conducts thorough code reviews with actionable feedback.

**Parameters:**
- `code` (required): Code to review
- `language` (required): Programming language
- `type`: Type of code (feature, bugfix, refactor)
- `pr_description`: Pull request context
- `standards`: Coding standards to check

### o3_safety - Security Review

Identifies security vulnerabilities and safety issues.

**Parameters:**
- `code` (required): Code to review
- `language` (required): Programming language
- `context`: Application context
- `sensitivity`: Data sensitivity level
- `compliance`: Compliance requirements

### o3_reasoning - Deep Reasoning

Applies systematic reasoning to complex problems.

**Parameters:**
- `problem` (required): Problem description
- `context`: Relevant background
- `constraints`: Specific requirements
- `options`: Potential solutions to evaluate
- `depth`: Reasoning depth (low/medium/high)

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | Model to use | o3-pro |
| `OPENAI_BASE_URL` | Custom API endpoint | https://api.openai.com |
| `TEMPERATURE` | Response creativity | 0.2 |
| `MAX_TOKENS` | Maximum response length | 100000 |
| `TOP_P` | Nucleus sampling | 0.95 |
| `REASONING_DEPTH` | Default reasoning level | medium |
| `SAFETY_THRESHOLD` | Security check sensitivity | medium |
| `LOG_LEVEL` | Logging verbosity | INFO |

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Tools

1. Create a new tool class in `src/tools/`
2. Inherit from `BaseTool`
3. Implement required methods
4. Add to `__init__.py`
5. Update server initialization

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not found"**
   - Set your API key: `echo "OPENAI_API_KEY=your-key" > ~/claude-openai-mcp/.env`
   - Or re-run the installer: `cd ~/claude-openai-mcp && ./install.sh`

2. **"Model o3-pro not available"**
   - Verify you have access to o3-pro in your OpenAI account
   - Check if you need to use a different model name

3. **"Connection refused"**
   - Restart Claude Code after installation
   - Check the path in Claude Code configuration

4. **"Request timed out"**
   - o3-pro can take several minutes - this is normal
   - For very complex tasks, consider breaking them into smaller parts

### Debug Mode

Enable debug logging:

```env
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Inspired by [claude_code-gemini-mcp](https://github.com/RaiAnsar/claude_code-gemini-mcp) and [gemini-mcp-server](https://github.com/BeehiveInnovations/gemini-mcp-server)
- Built for use with [Claude Code](https://claude.ai/code)
- Powered by OpenAI's o3_pro model