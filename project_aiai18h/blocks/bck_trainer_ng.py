import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l
import project_aiai18h.blocks.trainer_ng_competencies_se_html_bck


def html_block(
    trainer_name="Nicolas Guelfi",
    trainer_image="ng_black_white.png",
    trainer_link="https://drive.google.com/file/d/1FaGAxN4-zK2YUBeXsYJsxj3BWA3eJUas/view",
    logo_unilu="logo_unilu.png",
    logo_pi="logo_pi.png",
    logo_unige="logo_unige.png",
    logo_ros="logo_ros.png",
    linkedin_url="https://www.linkedin.com/in/nicolas-guelfi-phd/",
    linkedin_logo="logo_linkedin.gif"
):
    
    center = s.text.alignments.center_align
    g_lists = s.container.lists.g_docs
    large = s.text.sizes.large_size
    Large = s.text.sizes.Large_size
    bronze = s.project.bronze_01_bold


    html = ""
    html += st_block(center,
                [
                    st_write(s.project.titles.title_purple_01, "Who?"),
                        st_space("v", 2),
                    st_write(s.project.titles.title_green_01, "Trainer(s)", toc_lvl=TOC('2')),
                        st_space("v", 2),
                    st_write(s.project.titles.subtitle_blue_01, 
                             trainer_name,
                             link=trainer_link, no_link_decor=True,
                             toc_lvl=TOC('+1')),
                        st_space("v", 2),
                    st_image(uri = trainer_image, width="33%")
                ])
        
    html += st_grid(2, 2, 
            grid_style=s.project.low_pad+s.container.layouts.table_layout,
            cell_styles=s.project.low_pad,
            block_list=
            [
                st_list(l.unordered, g_lists, large,
                    [
                        st_write(bronze + Large, "Activities"),
                        [
                            "Education / Training",
                            "Research / Development"
                        ]
                    ]), 

                st_include(project_aiai18h.blocks.trainer_ng_competencies_se_html_bck), 

                st_list(l.unordered, g_lists, large,
                    [
                        st_write(bronze + Large, "Contexts"),
                        [
                            st_block(block_list=
                                [
                                    "University of Luxembourg",
                                    st_block(s.container.flex.row_flex,
                                        [
                                            st_image(uri = logo_unilu, link="https://www.uni.lu/fstm-en/people/nicolas-guelfi/"),
                                            st_image(uri = logo_pi), 
                                            st_image(uri = logo_unige)
                                        ])
                                ]),
                            st_block(s.container.flex.col_flex, 
                                [
                                    "Right-On-Skill sarl",
                                    st_image(uri = logo_ros, width="33%")
                                ])
                        ]
                    ]),

                st_list(l.unordered, g_lists, large,
                    [
                        st_write(s.project.green_01_bold + Large, "Artificial Intelligence"),
                        [
                            "Generative AI",
                            "Deep Learning",
                            "Expert Systems"
                        ]
                    ])
            ])
    
    html += st_list(l.unordered, g_lists, Large,
                [
                    st_block(s.container.flex.col_flex + center, 
                        [  
                            "More information",
                            st_image(uri = linkedin_logo, link=linkedin_url, width="250px")
                        ])
                ])


        
    return html
