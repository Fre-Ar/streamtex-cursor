import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

def html_block(trainer_name="Nicolas Guelfi"):


    html = ""
        
    html += st_list(l.unordered, s.container.lists.g_docs, s.text.sizes.large_size,
                [
                    st_write(s.project.green_01_bold + s.text.sizes.Large_size, "Software Engineering"),
                    [
                        f"Requirements engineering",
                        "Critical systems"
                    ]
                ])
        
    return html