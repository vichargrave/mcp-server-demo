# mcp-server-demo

A minimal [Model Context Protocol](https://modelcontextprotocol.io) server built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk). It exposes a single `add` tool over streamable HTTP and is wired up for use with Claude Code via `.mcp.json`.

## Project structure

```
mcp-server-demo/
├── main.py            # FastMCP server + tool definitions
├── pyproject.toml     # Project metadata and dependencies
├── uv.lock            # Locked dependency versions (managed by uv)
├── .python-version    # Pinned Python version (3.14)
├── .mcp.json          # Claude Code MCP server registration
└── CLAUDE.md          # Guidance for Claude Code sessions
```

`main.py` is the whole server:

- Creates a `FastMCP("Demo", json_response=True)` instance.
- Registers tools with the `@mcp.tool()` decorator — function signatures and docstrings become the tool's MCP schema automatically.
- Runs over the `streamable-http` transport, which listens on `127.0.0.1:8000` and serves the MCP endpoint at `/mcp/`.
- Installs SIGINT/SIGTERM handlers so the server shuts down cleanly.

## Requirements

- Python **3.14+**
- [`uv`](https://docs.astral.sh/uv/) for dependency management

## Setup

```bash
uv sync
```

This creates `.venv` and installs the locked dependencies (`mcp[cli]`).

## Running the server

```bash
uv run main.py
```

The server listens on `http://127.0.0.1:8000/mcp/`. Stop it with `Ctrl+C`.

## Using it with Claude Code

`.mcp.json` already registers this project's server with Claude Code as an HTTP MCP server:

```json
{
  "mcpServers": {
    "demo": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp/"
    }
  }
}
```

Start the server first (`uv run main.py`), then launch Claude Code from this directory. The `add` tool will be available as `mcp__demo__add`.

## Adding a new tool

Define a typed function in `main.py` and decorate it with `@mcp.tool()`:

```python
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b
```

Restart the server to pick up changes.
