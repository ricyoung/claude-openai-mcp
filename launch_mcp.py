#!/usr/bin/env python3
"""Launch the Claude-OpenAI MCP server."""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now import and run the server
from server import main

if __name__ == "__main__":
    main()