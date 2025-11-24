import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l


class BlockStyles:
    border = s.container.borders.color(s.text.colors.black) + s.container.borders.solid_border + s.container.borders.size("2px")
bs = BlockStyles

def html_block(
    gpt_image="chat_gpt_sample_01_en.png",
    llm_symbol="llm_symbolism.png",
    bear_gif_1="bear_walking_01.gif",
    bear_gif_2="bear_walking_02.gif",
    bear_gif_3="bear_walking_03.gif",
    deep_fake_gif="showcase_deep_fake_01.gif"
    ):
    

    html = ""

    html += st_grid(3, 2, cell_styles= bs.border + s.container.paddings.little_padding + s.container.layouts.vertical_center_layout,
            block_list = [
                st_image(uri = gpt_image),
                st_image(uri = llm_symbol),
                st_grid(2, 1, block_list=
                    [
                        st_grid(1, 3, cell_styles= s.container.paddings.small_padding,
                                block_list=
                                [
                                    st_image(uri = bear_gif_1), 
                                    st_image(uri = bear_gif_2), 
                                    st_image(uri = bear_gif_3)
                                ]),
                        st_write(s.text.alignments.center_align+s.text.sizes.Large_size,
                                 f'{st_write(ns("color: #274e13;"), "prompt")} + snow + {st_write(ns("color: #660000;"), "cartoon")}',
                                   tag=t.div)
                    ]),
                st_image(uri = deep_fake_gif),
                st_image(uri = "showcase_dl_maths_01.gif"),
                st_image(s.container.sizes.height_auto, uri = "showcase_dl_maths_02.gif")
            ])
        
    return html


