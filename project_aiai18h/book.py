import streamlit as st 

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import project_aiai18h.blocks
import project_aiai18h.blocks.bck_image_break_frog_orange
import project_aiai18h.blocks.bck_image_dog_02_practice
import project_aiai18h.blocks.bck_image_dog_sherlock
import project_aiai18h.blocks.bck_image_go_practice
import project_aiai18h.blocks.bck_image_two_racoons_01
import project_aiai18h.blocks.bck_image_welcome_back_giraffe_01
import project_aiai18h.blocks.bck_it_computers_ai_users
import project_aiai18h.blocks.bck_participants_round_table_aiai
import project_aiai18h.blocks.bck_practice_course_pack_access
import project_aiai18h.blocks.bck_showcase_aiai_content
import project_aiai18h.blocks.bck_showcase_glimpse_aiai
import project_aiai18h.blocks.bck_showcase_image_recognition_mnist_intro_aiai
import project_aiai18h.blocks.bck_showcase_text_generation
import project_aiai18h.blocks.bck_title_bravo
import project_aiai18h.blocks.bck_title_break
import project_aiai18h.blocks.bck_title_content
import project_aiai18h.blocks.bck_trainer_ng
import project_aiai18h.blocks.bck_training_title_aiai_dlh
import project_aiai18h.blocks.bck_welcome_screen_aiai
import project_aiai18h.blocks.bck_domains_terms_aiai
import project_aiai18h.blocks.bck_game_your_profile
import project_aiai18h.blocks.bck_content_aiai_all
import project_aiai18h.blocks.bck_session_01_course_docs
import project_aiai18h.blocks.bck_setting_up_notebooks_aiai




st.set_page_config(page_title="AIAI",
                    page_icon=None,
                    layout="centered",
                    initial_sidebar_state="expanded",
                    menu_items=None)

import streamtex_package.src.streamtex as sx
import project_aiai18h.custom.config as cfg



# Define the root path for the blocks folder
blocks_root_path = os.getcwd() + "/project_aiai18h/blocks"
path_python_folder = os.path.join(blocks_root_path, "py")
sys.path.append(path_python_folder)





st.sidebar.title("Table of Contents")


module_list = [
    project_aiai18h.blocks.bck_welcome_screen_aiai,
    project_aiai18h.blocks.bck_training_title_aiai_dlh,
    project_aiai18h.blocks.bck_showcase_glimpse_aiai,
    project_aiai18h.blocks.bck_trainer_ng,
    project_aiai18h.blocks.bck_participants_round_table_aiai,
    project_aiai18h.blocks.bck_domains_terms_aiai,
    project_aiai18h.blocks.bck_it_computers_ai_users,
    project_aiai18h.blocks.bck_title_content,
    project_aiai18h.blocks.bck_image_dog_sherlock,
    project_aiai18h.blocks.bck_content_aiai_all,
    project_aiai18h.blocks.bck_session_01_course_docs,
    project_aiai18h.blocks.bck_image_dog_02_practice,
    project_aiai18h.blocks.bck_practice_course_pack_access,
    project_aiai18h.blocks.bck_game_your_profile,
    project_aiai18h.blocks.bck_setting_up_notebooks_aiai,
    project_aiai18h.blocks.bck_image_go_practice,
    project_aiai18h.blocks.bck_title_bravo,
    project_aiai18h.blocks.bck_image_two_racoons_01,
    project_aiai18h.blocks.bck_title_break,
    project_aiai18h.blocks.bck_image_break_frog_orange,
    project_aiai18h.blocks.bck_image_welcome_back_giraffe_01,
    project_aiai18h.blocks.bck_showcase_aiai_content,
    project_aiai18h.blocks.bck_showcase_text_generation,
    project_aiai18h.blocks.bck_showcase_image_recognition_mnist_intro_aiai
]




sx.st_book(module_list)


