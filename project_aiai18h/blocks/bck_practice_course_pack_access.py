import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

class BlockStyles:
    """Custom styles defined locally and used only for this block"""
    center_txt = s.text.alignments.center_align
    content = s.Large + center_txt
    green = s.project.colors.green_01
    pink = s.project.colors.pink_01
    gold = s.project.colors.bronze_01
    huge_green_title = green + s.huge
    large_italic_text = s.text.decors.italic_text + s.text.sizes.large_size
    blue = s.project.colors.blue_01
    link_style = s.project.titles.subtitle_blue_01
    red_emphasis = s.project.colors.red_01 + s.bold + s.LARGE
    purple_subtitle = s.project.colors.purple_02 + content + s.bold
bs = BlockStyles

def html_block():
    html = ""

    temp_text_01 = f"USE {st_write(bs.gold, 'YOUR')} VALUES(S) PRINTED ON PAPER"
    temp_text_02 = {st_write(s.bold, f"{st_write(s.LARGE, 'YOUR')} {st_write(bs.green, 'gmail email address')} {st_write(bs.pink, temp_text_01)}")}

    html += st_block(bs.center_txt, [
        st_write(bs.huge_green_title + bs.center_txt + s.bold,
                 "Practice - CoursePack Access",
                 toc_lvl=TOC('2')),
        st_space(size=5),

        st_write(bs.center_txt + bs.blue + s.bold + s.huge, "Process", toc_lvl=TOC('+1')),
        st_space(size=5),

        st_write(bs.purple_subtitle, "Please proceed to the following process:"),
        st_space(size=3),
        st_list(
            list_type=l.ordered,
            li_style= bs.content,
            block_list=[
                st_write(txt="Start your computer (if not started)"),
                st_write(txt="Open a session using the institution identification information (if not already opened)"),
                st_write(txt="Launch firefox application"),
                st_write(txt=f"Go to {st_write(bs.link_style, 'aiai.ros.lu', link='https://aiai.ros.lu')}"),
               #  st_write(txt=f'Click on {st_write(bs.red_emphasis, '"Go"')}'),
                st_write(txt=f"""Click on {st_write(bs.red_emphasis, '"Go"')}"""),
                # st_write(txt=f"Fill the form with {st_write(s.bold, f"{st_write(s.LARGE, 'YOUR')} {st_write(bs.green, 'gmail email address')} {st_write(bs.pink, f"USE {st_write(bs.gold, "YOUR")} VALUES(S) PRINTED ON PAPER")}")}"),
                st_write(txt=f"Fill the form with {temp_text_02}"),
                st_write(txt=f"Check your email at {st_write(bs.link_style, 'mail.google.com', link='https://mail.google.com')}"),
                st_write(txt=f"Click on the {st_write(bs.gold + s.LARGE + s.bold, 'COURSEPACK')} link")
            ]
        )
    ])

    return html


