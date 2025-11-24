import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

class BlockStyles:
    pos = s.container.positions
bs = BlockStyles

def html_block():

    html = ""
    html += st_write(toc_lvl=TOC("1"), label="_AIAI")
    html += st_image(uri = "cameleon_aiai_01.png")

    html += st_overlay(st_image(uri = "cameleon_aiai_01.png"),
                        [st_write(s.big+s.bold+s.text.colors.yellow, "AIAI")],
                        [bs.pos.bottom(16)+bs.pos.left(16)])

    html += st_write(s.large,"Go to bravo label", link="#bravo")

    return html