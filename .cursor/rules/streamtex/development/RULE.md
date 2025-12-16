---
alwaysApply: true
---

# StreamTeX Development Guidelines

## 1. The StreamTeX Philosophy
StreamTeX is a wrapper around Streamlit with a block-based architecture. You are strictly forbidden from manually writing HTML or CSS strings within the Python code.
- **❌ BAD:** `st.markdown("<div style='color:red'>Text</div>", unsafe_allow_html=True)`
- **✅ GOOD:** `sx.st_write(s.text.colors.red, "Text")`

## 2. Source of Truth
- **Syntax Reference:** Read `documentation/streamtex_cheatsheet_en.md` before writing any block code.
- **Architecture Reference:** Inspect `project_aiai18h/` to understand how `book.py` orchestrates `blocks/`, and how to build a web book with modular blocks that may be nested and reuseable.

### Directory Structure
- Follow the standard StreamTeX project structure:
  - `book.py` (main entry point)
  - `blocks/` (content modules)
  - `custom/` (config.py, styles.py)
  - `static/images/` (static assets)
  - `streamtex_package/` (library)
  - `.streamlit/config.toml` (streamlit configuration, **critical** for static image serving)

## 3. Mandatory Imports

### A. For Block Files (`blocks/bck_*.py`)
Every block file must start with this setup:
```python
import streamlit as st

# StreamTeX Imports
from streamtex_package.src.streamtex import *
import streamtex_package.src.streamtex as sx
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

# Project Specific Imports
from [project_name].custom.styles import Styles as s
```

### B. For the Entry Point (`book.py` ONLY)
- This file MUST handle the path setup.
```python
import streamlit as st
import os, sys
# Ensure parent directory is in path for streamtex_package access
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```
- Import blocks individually, not via `import *`

## 4. Coding Standards: `sx` vs `st`

### When to use StreamTeX (`sx`)

Use `sx` functions for **ALL** layout and static content.

- **Text:** Use `sx.st_write(style, txt=...)` instead of `st.write` or `st.markdown`.
- **Images:** Use `sx.st_image(style, uri=...)` instead of `st.image`.
- **Lists:** Use `sx.st_list()` instead of manual markdown lists.
- **Layouts:** Use `sx.st_grid(rows, cols, ...)` or `sx.st_table()` instead of `st.columns`.
- **Content Encapsulation:** Use `st_block()`.
- **Spacing:** Use `sx.st_space()` or `sx.st_br()`.

#### Common Parameters
- Always specify `style=` for `st_write()`
- Use `toc_lvl=TOC('level')` for table of contents
- Use `link=` for hyperlinks
- Use `tag=` to specify HTML tag

#### Layout & Encapsulation Rules (`st_block`)

  - **Vertical Stacking (Default):** Use `sx.st_block(..., tag=t.div)` when you want elements to stack on top of each other. This is the default behavior.
  - **Horizontal Flow:** Use `sx.st_block(..., tag=t.span)` when you want elements to flow inline (side-by-side), similar to text spans.

### When to use Streamlit (`st`)

Only use standard `st` functions for:

- Interactivity (Buttons, Inputs, Sliders).
- Media players (Audio/Video) if `sx` lacks a wrapper.
- Dataframes (if `sx.st_table` is insufficient).

## 5. Block Architecture

### HTML Blocks (`html_block`)

Use this for static content. It must return a string.

```python
import streamlit as st

from streamtex_package.src.streamtex import *
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

from [project_name].custom.styles import Styles as s

class BlockStyles:
    """Local styles for this block only"""
    # Define block-specific styles
    pass
bs = BlockStyles

def html_block():
    html = ""
    html += sx.st_block(s.center_txt, [
        sx.st_write(s.title, "Hello World")
    ])
    return html
```

### Panel Blocks (`build_panel`)

Use this *only* when interactivity is required. It returns a callable or renders directly.

```python
def build_panel():
    # Use standard st elements here if necessary, mixed with sx helpers
    if st.button("Click me"):
        st.write("Clicked")
```

## 6. Project Structure

- **Filenames:** `blocks/bck_[description]_[suffix].py`. Examples: `bck_welcome_screen_aiai.py`, `bck_title_content.py`.
- **Assets:** Store images in `static/images/`. Refer to them using relative paths or filenames directly if configured in `config.py`. Use `os.path.join()` to build paths.
- **Path Configuration:** Define base paths in `config.py`. Use `Path()` for modern path manipulation. Use `os.path.join()` to build paths. Create directories automatically if needed.

## 7. Styling Guidelines

- **No Inline Strings:** Never write inline CSS strings (e.g., `"font-size: 20px"`).
- **Base Styles:** Use `s.text.*`, `s.container.*` for base styles
- **Project Styles:** Use `s.project.*` for project-specific custom styles
- **Composition:** Combine styles using the `+` operator: `s.bold + s.red + s.Large + s.center_txt`.
- **Definition:** Define styles in `BlockStyles` class within the file or `custom/styles.py`.
- **Text Font and Sizes:** 
  - **Default:** The default font is **Arial**. The default unstyled size is **16px** (approx. **12pt**).
  - **Available Sizes:** `s.text.sizes` (often aliased directly as `s.large`, `s.huge`, etc.) provides the following scale:
    - **Titles:** `GIANT` (196pt), `Giant` (128pt), `giant` (112pt), `Huge` (96pt), `huge` (80pt).
    - **Headers:** `LARGE` (64pt), `Large` (48pt), `large` (32pt).
    - **Body/Sub:** `big` (24pt), `medium` (16pt), `little` (12pt/Default), `small` (8pt), `tiny` (4pt).
  - **Usage:** Ensure title-to-body ratios are balanced.
- **Typography Details (Bold & Italic)** 
  - **Detection:** Be keenly aware of weight and emphasis.
    - **Bold:** Apply `s.bold` if the text carries visual weight or acts as a sub-header.
    - **Italic:** Apply `s.italic` for citations, emphasis, or captions.
  - **Defaults:** Remember that links (`link=...`) are underlined and blue by default. Use `no_link_decor=True` if the design shows a plain link.
- **Light vs. Dark Mode Awareness:** Do not hardcode black or white unless it is an explicit design choice (e.g., a specific "card" background). 
  - **Implicit Colors:** If text is black on a white background (or vice versa), this is usually the *default theme*, not a style. **Do NOT** explicitly style it as `color: black`. Let Streamlit handle the Light/Dark mode switch.
  - **Explicit Colors:** Only define `color` or `background-color` if it is a branding color (Red, Blue, specialized Gray) that must remain constant regardless of the theme.

### Custom Style Creation
- Inherit from `StreamTeX_Styles` in `custom/styles.py`
- Organize by categories: colors, titles, etc.
- Use `Style.create()` to combine existing styles

### Style Reusability & Naming (MANDATORY)
- **Generic Definitions:** Always define and reuse generic styles. If two texts (regardless of content) share the same properties (e.g., pink color, 18pt size), create **ONE** style with a generic name (e.g., `pink_subtitle`) and reuse it.
- **Language Agnostic:** Use **ENGLISH only** for style names. Reuse the same style instance for text in any language. Do not duplicate styles just because the text content differs.
- **Avoid Duplication:** Do not differentiate styles by ID if they have exactly the same definition.

### Visual Considerations
- **Dark Mode:** Ensure your style definitions are dark mode friendly (e.g., avoid pure black text on transparent backgrounds if the default theme is dark).
- **Alignment:** Be keenly aware of centered styles and text alignment.
- **Precision Layout:** Always insert line breaks (`st_br()` function call) to match the provided text layout exactly.  

## 8. Variable Naming Conventions

### Classes and Variables
- `BlockStyles` or `BStyles` for local styles
- `bs = BlockStyles` for the instance
- `html_block()` for HTML blocks
- `build_panel()` for panel blocks

### Custom Styles
- Use descriptive names: `title_giant_green_01`, `subtitle_blue_01`
- Suffix custom colors: `green_01`, `blue_dark_01`, `bronze_01`


## 9. Documentation and Comments

### Block Documentation
- Include docstring for `html_block()` or `build_panel()`
- Document function parameters with default values
- Add comments for complex styles

### Style Documentation
- Document custom styles in `custom/styles.py`
- Explain style hierarchy in comments
- Use descriptive variable names

## 10. Performance and Optimization

### Style Optimization
- Avoid repeated creation of identical styles
- Use predefined styles instead of inline styles
- Minimize complex style combinations

### Memory Management
- Avoid circular imports
- Use local imports when possible
- Clean up temporary resources

## 11. Development Conventions

### Code Formatting
- Use 4 spaces for indentation
- Limit lines to 100 characters
- Use snake_case for variable names
- Use PascalCase for class names

## 12. StreamTeX Specific Patterns

### Table of Contents
- Use `TOC('1')` for level 1, `TOC('+1')` for relative levels
- Always provide meaningful labels
- Use `toc_lvl` parameter in `st_write()`

### Style Combinations
- Prefer style composition over inline CSS
- Use `StyleGrid` for complex layouts
- Leverage theme system for global style changes


## 13. Best Practices

### Code Organization
- Keep blocks focused and single-purpose
- Reuse common patterns across blocks
- Maintain consistent naming throughout project

### Style Consistency
- Use project color palette consistently
- Follow typography hierarchy
- Maintain spacing and layout patterns

### Testing and Validation
- Test blocks individually
- Validate HTML output
- Check responsive behavior
- Verify accessibility features

