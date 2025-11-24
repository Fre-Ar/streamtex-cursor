import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

class BlockStyles:
    """Custom styles defined locally and used only for this block"""
    blue = s.project.colors.blue_01 + s.text.decors.underline_text
bs = BlockStyles


def html_block():
    html = ""

    html += st_block(s.center_txt + s.LARGE + s.bold, [
            st_write(s.project.colors.blue_01 + s.huge, "Image Recognition", toc_lvl=TOC("2")),
                st_space(size=1),
            st_write(s.project.colors.orange_01, "Handwritten Digits", toc_lvl=TOC("+1")),
                st_space(size=1),
            st_write(s.project.colors.red_01, "Demo", toc_lvl=TOC("+2")),
                st_space(size=2)
        ]
    )


    html += st_image(uri="digit_recognition_mnist_01.png", width="1541px", height="914px")
    html += st_space(size=3)


    html += st_block(s.center_txt + s.Large + s.bold, [
        st_write(bs.blue, txt= "2DANN", link="https://adamharley.com/nn_vis/mlp/2d.html", no_link_decor=True) +
            st_space("h", size=1) +
        st_write(bs.blue, txt= "2DCNN", link="https://adamharley.com/nn_vis/cnn/2d.html", no_link_decor=True) + st_br(),
        st_write(bs.blue, txt= "3DANN", link="https://adamharley.com/nn_vis/mlp/3d.html", no_link_decor=True) + st_space("h", size=1) +
        st_write(bs.blue, txt= "3DCNN", link="https://adamharley.com/nn_vis/cnn/3d.html", no_link_decor=True)
    ])

    html += st_space(size=5)

    return html