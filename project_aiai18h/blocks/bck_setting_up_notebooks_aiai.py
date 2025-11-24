import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

class BlockStyles:
    """Custom styles defined locally and used only for this block"""
    content = s.Large + s.center_txt
    lime_bold = s.text.colors.lime + s.bold
    bold_green = s.project.colors.green_01 + s.bold
    green_title = bold_green + s.huge + s.center_txt
    brown_title = s.project.colors.brown_01 + s.LARGE
    orange_emphasis = s.project.colors.orange_01 + s.bold
    pink_title = s.project.colors.pink_01 + s.LARGE + s.bold
    link_style = s.text.colors.blue + s.text.decors.underline_text
bs = BlockStyles

def html_block():
    html = ""


    html += st_block(s.center_txt, [
        st_write(bs.green_title,
                 f"Setting up the {st_write(bs.brown_title, 'NOTEBOOKS')}",
                 toc_lvl=TOC("2")),
        st_space(size=3),
    ])

    html += st_block(s.center_txt, [
        st_list(
            list_type=l.ordered,
            li_style=bs.content,
            block_list=[
                st_write(txt=f"open the {st_write(s.bold, 'COURSEPACK') + st_br()} in a new tab in your browser"),
                    
                st_write(txt=f"""Go to section: {st_write(txt='Notebooks links', link="https://docs.google.com/document/d/1eYtoLVpYgCrSpr8n75-jxqx3hrcnm1qUYYU0A4WXztY/edit?pli%3D1%23heading%3Dh.fhxl49mk9k3e")}"""),
                st_write(txt=f'click on "link" of YOUR {st_write(bs.orange_emphasis, "Notebook URL") + st_br()} {st_write(s.project.colors.brown_01 + s.bold,"(use your number printed on the paper sheet)")}'),
                st_write(txt=f"connect using {st_write(bs.lime_bold, 'YOUR gmail')} account {st_br()} (same one used in the resources access form)"),
                st_write(txt="You should see a screen close to this one:") +\
                      st_br() + st_image(uri="notebook_folder_01.png", width="1150px", height="735.34px"),
                st_write(txt=st_write(s.italic, "(optional)") + st_write(s.project.bronze_01_bold, " Discover ") + "the NOTEBOOK environment"),
                st_write(txt=st_write(
                        s.italic,"(optional)") + " Bookmark the notebook" + st_br() +\
                        "drag the " + st_image(uri="key_lock_01.png", width="60px", height="64px") +\
                        " below in the bookmarks bar") + st_br() + st_image (uri="browser_bar_01.png", width="532px", height="230px") +\
                            st_space(size=2),

                st_write(txt=f"""{st_write(s.italic,"(optional)")} Backup notebooks folder {st_br() + st_write(bs.bold_green, 'cf. section "Backup notebooks folder"') + st_br()} in the {st_write(s.bold, "COURSEPACK")}""")+\
                            st_space(size=2),

                st_write(
                    txt=f"""{st_write(s.italic,"(optional)")} Backup notebooks folder """ +\
                        st_br() + f"""{st_write(bs.bold_green, 'cf. section "Backup notebooks folder"')}""" +\
                        st_br() + f"""in the {st_write(s.bold, "COURSEPACK")}""") + st_space(size=2),


                st_write(txt="Open Notebook" + st_br() + st_write(bs.green_title, "-> ask the trainer"))+\
                            st_space(size=2),
                st_write(txt=st_write(bs.pink_title, "Duplicate the notebook")) + st_br() +\
                        st_list(
                            list_type=l.ordered,
                            l_style=s.container.lists.ordered_lowercase,
                            li_style=bs.content,
                            block_list=[
                                st_write(txt="right click + Duplicate"),
                                st_write(txt="set a smart name")
                            ]
                        )  + st_space(size=2)      
            ]
        )
    ])

    return html