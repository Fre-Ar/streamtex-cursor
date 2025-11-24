import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l


class BlockStyles:
    """Custom styles defined locally and used only for this block"""
    blue_title = s.project.colors.blue_01 + s.huge + s.center_txt + s.bold
    lime_bullet = s.text.colors.lime + s.bold
    brown_bold_title = s.project.colors.brown_01 + s.bold + s.LARGE

    red_bold_title = s.project.colors.red_01 + s.bold + s.large
    red_bold_title = s.project.colors.red_01 + s.bold + s.large

    table_cell_style = s.center_txt
    link_style = s.text.colors.blue + s.text.decors.underline_text

    side_padding = ns("padding: 10pt 36pt;")
bs = BlockStyles


def html_block():
    html = ""

    # Section Header: Text Generation
    html += st_write(bs.blue_title, "Text Generation", toc_lvl=TOC("2"), tag=t.div)
    html += st_space(size=3)

    # Image Block
    html += st_list(
        list_type=l.unordered,
        li_style=s.center_txt,
        block_list=[
            st_image(uri="gpt_text_generation_01.png", link="https://chat.openai.com"),
        ]
    )

    html += st_space(size=10)

    # Table: Chat Models and Links
    html += st_block(s.container.flex.center_align_items, [
        st_table(
            cell_styles=sg.create("A1,A3,A5", s.project.colors.orange_02) +\
                        sg.create("A2,A4", s.project.colors.red_01) +\
                        sg.create("A1:B5", s.bold + s.LARGE + bs.side_padding + s.center_txt) +\
                        sg.create("B1:B5", s.Large),
            block_list=[
                [
                    st_write(txt= "OpenAI ChatGPT"),
                    st_write(txt= "link", link="https://www.datacamp.com/blog/yolo-object-detection-explained"),
                ],
                [
                    st_write(txt= "Microsoft CoPilot"),
                    st_write(txt= "link", link="https://copilot.microsoft.com"),
                ],
                [
                    st_write(txt= "perplexity.ai"),
                    st_write(txt= "link", link="http://www.perplexity.ai"),
                ],
                [
                    st_write(txt= "claude.ai"),
                    st_write(txt= "link", link="https://claude.ai/"),
                ],
                [
                    st_write(txt="Various chat models comparison"),
                    st_write(txt= "link", link="https://sdk.vercel.ai/"),
                ]
            ]
        )
    ])

    html += st_space(size=5)

    return html