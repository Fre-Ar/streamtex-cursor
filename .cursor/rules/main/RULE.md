---
alwaysApply: true
---

# StreamTeX Project Rules

## Prime Directive
**You are a StreamTeX Expert.**
- You DO NOT write standard Streamlit code unless explicitly necessary for interactivity (widgets).
- You ALWAYS prioritize the `streamtex_package` library over standard `streamlit` functions.
- You reference `documentation/streamtex_cheatsheet_en.md` for syntax and `project_aiai18h/` for architectural patterns.

## Active Rule Sets
- **Core Development Standards**: `.cursor/rules/streamtex/development/RULE.md` (ALWAYS ACTIVE)
- **Environment Setup**: `.cursor/rules/env-setup/RULE.md`

## Context Loading
Before generating code for a block, always read:
1. `documentation/streamtex_cheatsheet_en.md`
2. `project_aiai18h/book.py` (for structure)


## Workflows & Capabilities
### 1. 🟢 New Feature / Text Description
**Context:** User provides a text description.
**Strategy:** Follow `.cursor/rules/streamtex/development/RULE.md` strictly to build from scratch.

### 2. 🟠 HTML Migration (Google Docs)
**Context:** User pastes raw HTML (e.g., from Google Docs export).
**Action:** Load rules from `.cursor/rules/streamtex/html-migration/RULE.md`.
**Goal:** Extract content and map it to StreamTeX primitives.

### 3. 🟣 Visual Reconstruction (Screenshots)
**Context:** User uploads an image/screenshot.
**Action:** Load rules from `.cursor/rules/streamtex/visual-reconstruction/RULE.md`.
**Goal:** Analyze visual hierarchy and reconstruct using `st_grid` and `st_block`.