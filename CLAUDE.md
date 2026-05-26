# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Dependency management and execution use `uv` (Python 3.14+).

- Install/sync dependencies: `uv sync`
- Run the server: `uv run main.py`
- Add a dependency: `uv add <package>`

There is no test suite, linter, or build step configured.

## Architecture

This is a single-file MCP (Model Context Protocol) server built on `FastMCP` (from the `mcp[cli]` package).

- `main.py` instantiates `FastMCP("Demo", json_response=True)` and registers tools via the `@mcp.tool()` decorator. New tools are added by writing a typed Python function and decorating it — FastMCP introspects the signature and docstring to build the MCP tool schema automatically.
- Transport is **streamable HTTP** (`mcp.run(transport="streamable-http")`), which binds to `127.0.0.1:8000` and exposes the MCP endpoint at `/mcp/`. SIGINT/SIGTERM are handled explicitly so the server shuts down cleanly when stopped.
- `.mcp.json` registers this server with Claude Code as an HTTP MCP server pointing at `http://127.0.0.1:8000/mcp/`. For Claude Code to use the tools, the server must already be running locally.

## Git Workflow

Work must be committed to Git regularly and pushed to GitHub to ensure no loss of progress or status. Follow these practices:

**Commit Frequency:**
- Commit after completing each logical unit of work (feature, bug fix, documentation update)
- Do not accumulate multiple changes before committing
- Aim for frequent, incremental commits rather than large batches

**Commit Messages:**
- Use clear, descriptive commit messages that explain what changed and why
- Format: Start with a present-tense imperative verb (e.g., "Add feature", "Fix bug", "Update docs")
- Include context about the change when relevant
- Example: "Add keyboard shortcut for find/replace" or "Fix win detection edge case in tic tac toe"

**Pushing:**
- Push commits to GitHub regularly (after each commit or at the end of each work session)
- This ensures changes are backed up and accessible remotely
- Never leave uncommitted work in progress without a clear reason

**Session-end safety net:**
- A `SessionEnd` hook in `.claude/settings.local.json` runs on every Claude Code session exit. If the working tree is dirty, it stages all changes (`git add -A`), commits them with the message `"Auto-commit on Claude Code session end"`, and pushes if an upstream is configured (otherwise it prints `(no upstream — not pushing)` and exits cleanly).
- The hook bypasses pre-commit and pre-push hooks (`--no-verify` on both `git commit` and `git push`) so the auto-commit can never be rejected by a local hook. This is the catch-all safety net — run lint/test checks during the session, not at session end.
- The hook is a backstop, not a substitute for the commit-frequently / push-regularly discipline above. Prefer creating meaningful, scoped commits during the session over relying on the catch-all auto-commit.
