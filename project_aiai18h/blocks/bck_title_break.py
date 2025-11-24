import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l


class BlockStyles:
    pass
bs = BlockStyles


def html_block():

    html = ""     
    html += st_write(s.project.titles.title_green_01 + s.center_txt, "Break", toc_lvl=TOC('2'), tag=t.div)
        
    return html


