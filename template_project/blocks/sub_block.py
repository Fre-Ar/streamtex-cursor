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
    html += st_write("This text is in a different block, but is being included in another block using st_include().")
        
    return html


