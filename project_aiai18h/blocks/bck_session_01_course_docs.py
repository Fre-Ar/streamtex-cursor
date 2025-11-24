import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

class BStyles:
    blue = s.project.colors.blue_01
    orange = s.project.colors.orange_02
    red = s.project.colors.red_02
    green = s.project.colors.green_01
    purple = s.project.colors.purple_01


    Huge = s.text.sizes.Huge_size
    huge = s.text.sizes.huge_size

    center =  s.text.alignments.center_align

    s_list = s.reset_bold + center + s.text.sizes.Large_size 
bs = BStyles

def html_block():

    html = ""     
    html += st_block(bs.center + s.text.sizes.Large_size + s.bold, [
        st_write(bs.purple + bs.Huge, "Session 1", toc_lvl=TOC("1")),
            st_space(size=2),
        st_write(bs.green + bs.huge, "Course documentation", toc_lvl=TOC("+1")), st_br(),
        st_write(bs.red, "©  DO NOT DISTRIBUTE"), st_br(),
        st_write(bs.blue + bs.huge, "Main Documents & Usage", toc_lvl=TOC("+1")), st_br(),
            st_space(size=2),

        st_list(li_style = bs.orange + s.text.sizes.LARGE_size + s.bold, block_list=[st_write(txt="Course Pack Document", toc_lvl=TOC("+1"))]),
        st_list(li_style = bs.s_list, block_list=[
            "all material for self study",
            "access to online board",
            "access to surveys",
            "access to notebooks"]),
        st_write(bs.blue, "_", link="https://docs.google.com/document/d/1kXSRZ6Woi3gCVcOdjtluk-JcGZ-0gYj6RwGk_49gOIc/edit")
    ])
        
    return html
