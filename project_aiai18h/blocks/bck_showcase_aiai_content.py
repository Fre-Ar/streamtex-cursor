import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l


class BlockStyles:
    """Custom styles defined locally and used only for this block"""
    green_huge_title = s.project.colors.green_01 + s.huge + s.text.alignments.center_align + s.bold
    lime_bullet = s.text.colors.lime + s.bold
    debriefing_style = s.project.colors.brown_01 + s.LARGE + s.bold
bs = BlockStyles


def html_block():

    html = ""

    html += st_write(bs.green_huge_title, "Showcase", toc_lvl=TOC("2"), tag=t.div)
    html += st_space(size=5)


    html += st_list(
            list_type=l.unordered,
            li_style=s.Large + s.center_txt,
            block_list=[
                st_write(txt="Text Generation"),
                st_write(txt="Image Recognition"),
                st_write(txt="Image Generation"),
                st_write(txt="Music Generation"),
                st_write(bs.debriefing_style, "Debriefing"),
            ]
        )
        
    return html


