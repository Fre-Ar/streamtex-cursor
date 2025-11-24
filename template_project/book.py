import streamlit as st 

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import template_project.blocks
import template_project.blocks.panel_block
import template_project.blocks.show_off





st.set_page_config(page_title="Web Book Name",
                    page_icon=None,
                    layout="centered",
                    initial_sidebar_state="expanded",
                    menu_items=None)

import streamtex_package.src.streamtex as sx
import project_aiai18h.custom.config as cfg




st.sidebar.title("Table of Contents")


module_list = [
    template_project.blocks.panel_block,
    template_project.blocks.show_off,
]




sx.st_book(module_list)


