# Claude-OpenAI MCP Server

A Model Context Protocol (MCP) server that bridges Claude Code with OpenAI's o3_pro model, providing advanced coding capabilities through specialized tools.

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

- **Streaming Support**: Real-time responses for better user experience
- **Configurable Reasoning Depth**: Adjust o3_pro's reasoning level (low/medium/high)
- **Safety-First Approach**: Built-in security review capabilities
- **Production-Ready**: Comprehensive error handling and logging
- **Flexible Configuration**: Environment-based settings

## Prerequisites

- Python 3.8 or higher
- OpenAI API key with o3_pro access
- Claude Code installed

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/claude-openai-mcp.git
cd claude-openai-mcp
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
MAX_TOKENS=4096
TOP_P=0.95
REASONING_DEPTH=medium  # low, medium, high
ENABLE_STREAMING=true
SAFETY_THRESHOLD=medium  # low, medium, high
LOG_LEVEL=INFO
```

### 4. Configure Claude Code

Add the MCP server to your Claude Code configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "claude-openai-mcp": {
      "command": "python",
      "args": ["/path/to/claude-openai-mcp/src/server.py"],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key"
      }
    }
  }
}
```

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
| `OPENAI_BASE_URL` | Custom API endpoint | None |
| `TEMPERATURE` | Response creativity | 0.2 |
| `MAX_TOKENS` | Maximum response length | 4096 |
| `TOP_P` | Nucleus sampling | 0.95 |
| `REASONING_DEPTH` | Default reasoning level | medium |
| `ENABLE_STREAMING` | Enable streaming responses | true |
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
   - Ensure the API key is set in your environment or `.env` file

2. **"Model o3-pro not available"**
   - Verify you have access to o3_pro
   - Check if you need to use a different model name

3. **"Connection refused"**
   - Ensure the MCP server is running
   - Check the path in Claude Code configuration

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