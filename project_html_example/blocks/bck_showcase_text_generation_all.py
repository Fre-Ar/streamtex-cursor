import streamlit as st

# StreamTeX Imports
from streamtex_package.src.streamtex import *
import streamtex_package.src.streamtex as sx
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

# Project Specific Imports
from project_html_example.custom.styles import Styles as s


class BlockStyles:
    """Local styles for the Text Generation showcase block."""

    # Title: large blue bold centered text
    title = s.project.colors.denim_blue + s.bold + s.huge + s.center_txt

    # Left column bullets: large brown/green styled bullets (use size + bold)
    left_bullet = s.Large + s.bold + s.center_txt

    # Right column primary link: big underlined blue links
    right_link = s.project.colors.denim_blue + s.text.decors.underline_text + s.Large + s.center_txt

    # Right column non-link items (Prompt Engineering, Specialized GPTs)
    right_text = s.Large + s.bold + s.center_txt

    # Section labels in tools table (left column)
    tool_label = s.Large + s.bold + s.center_txt

    # Tool link style in tools table (right column)
    tool_link = s.project.colors.denim_blue + s.text.decors.underline_text + s.Large + s.center_txt

    # Small italic annotation text for long comparison rows
    annotation = s.italic + s.bold + s.large + s.center_txt

    # Table layout & base cell styles (similar spirit to music block, simplified)
    tools_table = ns("table-layout: fixed; width: 100%; border-collapse: collapse;")
    cell = s.container.borders.solid_border + s.container.paddings.small_padding + s.center_txt

    # Alternate text colors for table rows to ease readability
    # We keep borders/padding in the base `cell` style and add colors via StyleGrid.
    # For the 1x2 concepts table
    concepts_cell_styles = (
        sg.create("A1:B1", cell)
        + sg.create("A1", s.text.colors.dark_blue)
        + sg.create("B1", s.text.colors.dark_magenta)
    )

    # For the 7x2 tools table: apply alternating row colors
    tools_cell_styles = (
        sg.create("A1:B7", cell)
        + sg.create("A1:B1,A3:B3,A5:B5,A7:B7", s.text.colors.dark_blue)
        + sg.create("A2:B2,A4:B4,A6:B6", s.text.colors.dark_magenta)
    )


bs = BlockStyles


def html_block():
    """Showcase Text Generation tools and concepts with one image and two tables."""
    html = ""

    # Title
    html += sx.st_block(
        s.center_txt,
        [
            sx.st_write(bs.title, "Text Generation", toc_lvl=TOC("1")),
        ],
    )

    # Main screenshot image
    html += sx.st_block(
        s.center_txt,
        [
            sx.st_image(
                uri="bck_showcase_text_generation_all_image_001.png",
                width="1536.00px",
                height="934.67px",
            )
        ],
    )

    # First table: high-level questions / concepts vs resources
    # Left column: Reasoning, Deep Research, Agents
    # Right column: Playground, Pricing, Prompt Engineering, Specialized GPTs

    concepts_cells = [
        # Left column
        sx.st_list(
            list_type=l.unordered,
            li_style=bs.left_bullet,
            block_list=[
                sx.st_write(txt="Reasoning / non-Reasoning ??"),
                sx.st_write(txt="Deep Research ??"),
                sx.st_write(txt="Agents ??"),
            ],
        ),
        # Right column
        sx.st_block(
            s.center_txt,
            [
                sx.st_write(
                    bs.right_link,
                    txt="Playground ??",
                    link="https://platform.openai.com/chat/edit?models=gpt-5",
                ),
                sx.st_br(),
                sx.st_write(
                    bs.right_link,
                    txt="Pricing ??",
                    link="https://platform.openai.com/docs/pricing",
                ),
                sx.st_br(),
                sx.st_write(
                    bs.right_text,
                    txt="Prompt Engineering ??",
                ),
                sx.st_br(),
                sx.st_write(
                    bs.right_text,
                    txt="Specialized GPTs ??",
                ),
            ],
        ),
    ]

    html += sx.st_table(
        1,
        2,
        table_style=bs.tools_table,
        cell_styles=bs.concepts_cell_styles,
        block_list=concepts_cells,
    )

    # Second table: concrete tools and links
    tool_rows = [
        (
            "Trainers tool",
            "https://huggingface.co/spaces/university-luxembourg/aiaiapps",
        ),
        ("OpenAI ChatGPT", "https://chatgpt.com"),
        ("DeepSeek", "https://chat.deepseek.com/"),
        ("Microsoft CoPilot", "https://copilot.microsoft.com"),
        ("perplexity.ai", "http://www.perplexity.ai"),
        ("claude.ai", "https://claude.ai/"),
    ]

    tools_cells = []
    for label, url in tool_rows:
        tools_cells.append(
            sx.st_write(
                bs.tool_label,
                txt=label,
            )
        )
        tools_cells.append(
            sx.st_write(
                bs.tool_link,
                txt="link",
                link=url,
            )
        )

    # Last two special rows: VERCEL and openrouter comparisons with annotations
    tools_cells.append(
        sx.st_block(
            s.center_txt,
            [
                sx.st_write(
                    bs.tool_label,
                    txt="VERCEL chat models comparison",
                ),
                sx.st_br(),
                sx.st_write(
                    bs.annotation,
                    txt="for demo by NG:",
                ),
                sx.st_br(),
                sx.st_write(
                    bs.annotation,
                    txt="nicolas.guelfi@ros.lu",
                ),
            ],
        )
    )
    tools_cells.append(
        sx.st_write(
            bs.tool_link,
            txt="link",
            link="https://sdk.vercel.ai/playground",
        )
    )

    tools_cells.append(
        sx.st_block(
            s.center_txt,
            [
                sx.st_write(
                    bs.tool_label,
                    txt="openrouter chat models comparison",
                ),
                sx.st_br(),
                sx.st_write(
                    bs.annotation,
                    txt="for demo by NG:",
                ),
                sx.st_br(),
                sx.st_write(
                    bs.annotation,
                    txt="nicolas.guelfi@bics.lu",
                ),
            ],
        )
    )
    tools_cells.append(
        sx.st_write(
            bs.tool_link,
            txt="link",
            link="https://openrouter.ai/chat?room=orc-1761753817-kvyfT4CtleoHHRbCdtE8",
        )
    )

    # 7 rows x 2 columns
    html += sx.st_table(
        7,
        2,
        table_style=bs.tools_table,
        cell_styles=bs.tools_cell_styles,
        block_list=tools_cells,
    )

    return html


