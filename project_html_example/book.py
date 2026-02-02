import streamlit as st
import os, sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import project_html_example.blocks
import project_html_example.blocks.bck_showcase_music
import project_html_example.blocks.bck_showcase_text_generation_all


st.set_page_config(
    page_title="HTML Migration Example",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items=None,
)

import streamtex_package.src.streamtex as sx
import project_html_example.custom.config as cfg


st.sidebar.title("Table of Contents")

module_list = [
    project_html_example.blocks.bck_showcase_music,
    project_html_example.blocks.bck_showcase_text_generation_all,
]


sx.st_book(module_list)

