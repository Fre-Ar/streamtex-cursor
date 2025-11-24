import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

class BlockStyles:
    border = s.container.borders.color(s.text.colors.black) + s.container.borders.solid_border + s.container.borders.size("2px")
bs = BlockStyles


def html_block():

    html = ""
    html += st_block(s.text.alignments.center_align,
            [
                st_write(s.project.titles.title_green_01, "Participant(s)", toc_lvl=TOC('2')),
                st_br(),
                st_write(s.project.titles.subtitle_blue_01, "Individual presentations", toc_lvl=TOC('+1'))
            ])
    
    html += st_grid(
        grid_style= s.text.sizes.large_size,
        cell_styles= bs.border + s.container.paddings.small_padding,
        block_list=
            [
                [
                    st_list(l.unordered, block_list=
                        [
                            "First name",
                            "Main Activities",
                            f"Motivations for participating to {st_write(s.project.bronze_01_bold, 'AIAI')}"
                        ], li_style=s.text.sizes.large_size),
                    st_list(l.unordered, block_list=
                        [
                            "Experience (if any)",
                            "sciences",
                            "technologies",
                            "articifical intelligence"
                        ], li_style=s.text.sizes.large_size)
                ]
            ])

    return html
