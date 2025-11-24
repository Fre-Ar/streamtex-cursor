import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

def html_block():

    html = ""
    html += st_write(s.text.alignments.center_align + s.project.titles.title_green_01,
                    "Content", t.div,
                    toc_lvl=TOC('2'))

    return html
