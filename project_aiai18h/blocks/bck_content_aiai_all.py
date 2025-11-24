import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

class BStyles:
    blue = s.project.colors.blue_01
    orange = s.project.colors.orange_02
    bronze = s.project.colors.bronze_01
    red = s.project.colors.red_02
    green = s.project.colors.green_01
    huge = s.text.sizes.huge_size

    center =  s.text.alignments.center_align

    s_list = s.text.sizes.Large_size + s.reset_bold + center
    title = blue + huge
bs = BStyles

def html_block():

    html = ""     
    html += st_block(bs.center + s.text.sizes.LARGE_size + s.bold, [
        st_write(bs.title, "Session 1", label = "Session 1", toc_lvl=TOC("+1")),
            st_space(),
        st_write(bs.orange, "Training Group Discovery  (60')", toc_lvl=TOC("+2")), st_br(),
        st_write(bs.orange, "Training Presentation (15')", toc_lvl=TOC("+2")), st_br(),
        st_write(bs.orange, "Setting up NOTEBOOKS  (30')", toc_lvl=TOC("+2")), st_br(),
            st_space(),
        st_write(bs.bronze, "Break (15')", toc_lvl=TOC("+2")),
            st_space(),
        st_write(bs.orange, "Showcase (45')", toc_lvl=TOC("+2")),

        st_list(li_style = bs.s_list, block_list=[
            "Text Generation",
            "Image Recognition",
            "Image&Video Generation",
            "Music Generation"]),
        
        st_write(bs.orange, "Intuitive introduction to AI  (45')", toc_lvl=TOC("+2")),
            st_space(),
        st_write(bs.title, "Session 2", toc_lvl=TOC("+1")),
            st_space(),
        st_write(bs.orange, "Practice and understanding of deep learning basic concepts using the MNIST running example", toc_lvl=TOC("+2")),
            st_space(),
        st_write(bs.title, "Session 3", toc_lvl=TOC("+1")),
            st_space(),
        st_write(bs.orange, "Practice and understanding of deep learning basic concepts - ctnd", toc_lvl=TOC("+2")),
            st_space(),
        st_write(bs.orange, "Practice and understanding of other deep learning architectures", toc_lvl=TOC("+2")),
            st_space(),
        st_write(bs.title, "Session 4", toc_lvl=TOC("+1")),
            st_space(),
        st_write(bs.orange, f"{st_write(bs.red, 'Ethics')} & Artificial Intelligence", toc_lvl=TOC("+2")),
            st_space(),
        st_write(bs.orange, f"{st_write(bs.green, 'Society')} & Artificial Intelligence", toc_lvl=TOC("+2"))
    ])
        
    return html
