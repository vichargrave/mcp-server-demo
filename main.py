"""
FastMCP quickstart example.

Run from the repository root:
    uv run main.py
"""

import signal
import sys
import os

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo", json_response=True)

NOTES_FILE = "/Users/vic/src/mcp-server-demo/notes.txt"


def ensure_notes_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")


@mcp.tool()
def add_note(message: str) -> str:
    """
    Add a note to the notes file.

    :param message: The note to add
    :return: Confirmation message 
    """
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return f"Note added: {message}"
 

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    Add two numbers
    
    :param a: First number
    :param b: Second number
    :return: The sum of the two numbers
    """
    return a + b


def handle_interrupt(signum, frame):
    print("\nShutting down...", file=sys.stderr)
    sys.exit(0)


# Run with streamable HTTP transport
if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)
    mcp.run(transport="streamable-http")