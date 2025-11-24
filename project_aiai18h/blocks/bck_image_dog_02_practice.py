import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l
def html_block(dog_img="dog_practice.png"):

    html = ""        
    html += st_image(uri = dog_img)
        
    return html
