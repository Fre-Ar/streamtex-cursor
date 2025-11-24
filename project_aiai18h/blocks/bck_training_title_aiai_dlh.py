import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

def html_block():
    
    lime = s.text.colors.lime
    bold = s.text.weights.bold_weight

    html = ""
    html += st_image(uri = "logo_ros.png", width="287px",  height="248px")
    html += st_block(s.project.titles.subtitle_intro_bronze_01 + s.text.alignments.center_align,
            [
                  st_space("v", 4),
                st_write(s.project.titles.title_intro_green_lime_01, "AI AI", tag=t.h2),
                  st_space(size= "2em"),
                st_write(bold, f'{st_write(lime,"A")}rtificial {st_write(lime, "I")}ntelligence'),
                  st_space("v", 0),
                st_write(bold, f'- {st_write(lime,"A")}pplied {st_write(lime, "I")}ntroduction:'),
                  st_space(),
                st_write(s.text.decors.italic_text, f'Concepts, Applications and Challenges')
            ],tag=t.div)

    return html