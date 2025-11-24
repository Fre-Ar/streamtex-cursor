import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

class BlockStyles:
    pass
bs = BlockStyles


def build_panel():

    html = ""     
    html += st_write("This was written using StreamTeX's st_* functions but is being displayed from a st.markdown call inside a build_panel() block.")

    st.markdown(html, unsafe_allow_html=True)

    st.image("https://picsum.photos/200/300")
   


