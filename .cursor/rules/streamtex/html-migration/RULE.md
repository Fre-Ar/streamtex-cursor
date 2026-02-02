---
alwaysApply: false
---

# StreamTeX HTML Migration Workflow

## 0. Strict Compliance (Read First)
**CRITICAL:** This workflow guides the *analysis* of HTML inputs. The *code generation* phase MUST strictly follow `.cursor/rules/streamtex/development/RULE.md`.
- **Inherit all rules:** No raw HTML strings, use `sx` functions, strict imports.
- **Inherit Styling:** Use generic style names (English) and dark-mode friendly colors as defined in the Core Guidelines.

## 1. Context
This workflow applies when the user provides raw, cluttered HTML (e.g., Google Docs export) to convert into a StreamTeX block.

When working in this repository, **treat the `project_html_example/` folder as a canonical reference implementation** for HTML migration:
- The HTML source is `html_exports/bck_showcase_music/bck_showcase_music.html`.
- The migrated StreamTeX block lives in `project_html_example/blocks/bck_showcase_music.py`.
- Static assets for that block live in `project_html_example/static/images/`.

Before implementing a new migration, you SHOULD:
- Skim `project_html_example/book.py` to see how the block is wired into a minimal project.
- Read `project_html_example/blocks/bck_showcase_music.py` to understand:
  - How noisy Google Docs classes were consolidated into `BlockStyles`.
  - How image assets were renamed and referenced.
  - How links and repeated patterns (e.g., link rows) were factored into helper functions.

## 2. Analysis Phase (Internal Monologue)
1.  **Filter Noise:** Ignore non-descriptive classes (`c1`, `c12`). Look at the *computed* style (e.g., bold, centered, blue).
2.  **Identify Defaults:**
    - Is the text or grid backgrounds just black/white? **Do not** apply a color style (allow Light/Dark mode). 
    - Is the link underlined? That is default behavior; do not add extra decoration styles or set `no_link_decor=True` (keep it as the default `False`).
3.  **Detect Formatting:**
    - Identify **Bold** (`font-weight: 700`) and *Italic* (`font-style: italic`) usage. Map these to `s.bold` and `s.italic`.
4.  **Identify Containers:**
    - Invisible tables used for alignment -> Map to `sx.st_grid()`.
    - Actual data tables -> Map to `sx.st_table()`.
    - Manual bullet points -> Map to `sx.st_list()`.
5.  **Style Consolidation:**
    - Identify repeating patterns (e.g., "11pt Arial Black").
    - Create **ONE** generic style in `BlockStyles` (e.g., `s.text.header_standard`) instead of copying `c1`, `c2`, `c3`.

## 3. Implementation Steps

### A. Asset Handling & Naming (CRITICAL)
If the HTML contains images (`<img>` tags), you MUST rename them using the project standard:
- **Format:** `[current_block_filename_no_ext]_image_[00index].[extension]`
- **Example:** `bck_session_intro_01_image_001.png`
- **Action:** Replace the original `src` (often a Googleusercontent URL) with this local URI in `sx.st_image(uri=...)`. 
- **Destination:** If the images are provided (present inside the workspace), copy them into the project's `static/images` folder and rename them.

### B. Structure & Layout
1.  **Setup:** Create file with Mandatory Imports from `.cursor/rules/streamtex/development/RULE.md`.
2.  **Styles:** Define consolidated `BlockStyles` class.
    - *Constraint:* Do not use IDs for style differentiation if definitions are identical.
3.  **Structure:** Write `html_block()`.
    - Use `tag=t.span` for inline elements.
    - Use `tag=t.div` for stacked blocks.

**Reference pattern:** In `project_html_example/blocks/bck_showcase_music.py`, notice how:
- Raw HTML table layout became a combination of `sx.st_table` with `cell_styles` and `sx.st_block` for cell content.
- Repeated inline link sequences were abstracted into a small helper (`link_row`) that returns an `sx.st_block(..., tag=t.span)`.

### C. Content Extraction
1.  **Text:** Extract clean text. Replace `<br>` with `sx.st_br()`.
2.  **Lists:** Convert `<ul>/<ol>` or manual bullets to `sx.st_list()`.

When unsure how to represent a particular HTML construct, **first look for the closest equivalent in `bck_showcase_music.py`** before inventing a new pattern.

## 4. Migration Checklist
- [ ] Did I remove all raw HTML strings?
- [ ] Did I replace "c1/c2" classes with semantic names?
- [ ] Did I rename all image assets to `..._image_001.[ext]`?
- [ ] Did I use `sx.st_list` instead of hardcoded bullets?
- [ ] Did I use `sx.st_br()` for line breaks to match the layout?
- [ ] Did I remove hardcoded black/white colors to support Dark Mode?
- [ ] Did I correctly apply `s.bold` and `s.italic` where needed?

