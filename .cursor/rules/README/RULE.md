---
alwaysApply: false
---

# Cursor Rules Organization

This directory contains the rules that guide the Cursor AI agent.

## Structure
- **streamtex/streamtex-development.mdc**: The core logic for writing StreamTeX code. Defines imports, block structures, and styling rules.
- **env-setup.mdc**: Instructions on how to run the project (Conda, Streamlit commands).
- **file-extension-standards.mdc**: (Optional) Meta-rules about naming files.

## Adding New Rules
1. Create a `RULE.md` file in the appropriate subdirectory.
2. Reference it in the main `.cursorrules` file in the project root if it should be active.