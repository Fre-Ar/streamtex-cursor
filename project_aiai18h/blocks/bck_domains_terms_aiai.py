import streamlit as st
from streamtex_package.src.streamtex import *
from project_aiai18h.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l

def html_block():

    class BStyles:
        Giant = s.text.sizes.Giant_size
        LARGE = s.text.sizes.LARGE_size
        large = s.text.sizes.large_size

        bold = s.text.weights.bold_weight
        green = s.project.colors.green_01

        center_txt = s.text.alignments.center_align

        blue = s.project.colors.blue_dark_01
        bronze =  s.project.colors.bronze_01 
        
        bronze_under = bronze + s.text.decors.underline_text + Giant 
        green_title = s.project.titles.title_giant_green_01
        red_title = s.project.titles.title_red_01 
        blue_bold = blue + bold
        blue_sub = s.project.titles.subtitle_blue_01

    bs = BStyles

    html = ""     
    html += st_block(bs.center_txt + bs.LARGE, 
                     [
                        st_write(bs.green_title + bs.center_txt, "Domains", toc_lvl=TOC('1')),
                        st_space("v", 3),
                        st_write(bs.red_title, f"""{st_write(bs.bronze_under, "A")}rtificial {st_write(bs.bronze_under, 'I')}ntelligence""",
                                 toc_lvl=TOC('+3')),
                        st_space("v", 3),
                        st_write(s.project.colors.orange_01 + bs.Giant, "..."),        
                        st_space("v", 3),
                        st_image(uri="monkey_01.jpg"),
                        st_space("v", 3),
                        st_write(bs.red_title, f"{st_write(bs.bronze, 'A')}rticifical", toc_lvl=TOC('+3')),
                        st_br(),
                        st_list(l.unordered, li_style = bs.LARGE + bs.center_txt, block_list=[
                            "man-made?",
                            "non-natural?"
                        ]),
                        st_space("v", 3),
                        st_write(bs.red_title, f"{st_write(bs.bronze, 'I')}ntelligence", toc_lvl=TOC('+3')),

                        st_list(l.unordered, li_style= bs.LARGE + bs.center_txt, block_list=[
                            "not stupid?",
                            "ability to acquire and apply knowledge and skills?",
                            "adaptation capabilities?"  
                        ]),

                        
                        st_space("v", 3),
                        st_write(bs.bronze, f"""\"Faculty of understanding, conceiving, knowing, and in particular the ability to discern or 
                                 {st_write(bs.blue_bold, "establish relationships between facts, ideas or forms to achieve knowledge.")}
                                    <br/><br/> Aptitude to 
                                    {st_write(bs.blue_bold, "adapt a behavior to a new situation")}, 
                                    a skill that is shown in a given situation, skill demonstrated by the choice of means that are used to achieve a specific result.\" """
                            ),
                        st_br(),
                        st_write(bs.blue_sub, "_", link="https://www.dictionnaire-academie.fr/article/A9I1608"),
                        st_space("v", 6),
                        st_write(bs.green + bs.bold + s.text.sizes.Large_size,
                                f"""\"Viewed narrowly, there seems to be almost 
                                    {st_write(bs.bronze, "as many definitions")} of intelligence
                                    {st_write(bs.bronze, "as")} there were {st_write(bs.bronze, "experts")} asked to define it.\" """),
                            st_space("v", 1),
                        st_write(s.text.decors.italic_text + bs.large, f"Sternberg R. (2004). intelligence. </br> In The Oxford Companion to the Mind. : Oxford University Press."),
                            st_br(),
                        st_write(bs.blue_sub, "_", link="https://arxiv.org/pdf/0706.3639.pdf") + st_space("h") +
                          st_write(bs.blue_sub, "_", link="https://www.arxiv-vanity.com/papers/0712.3329/"),
                        st_space("v", 3), 
                        st_write(s.project.titles.subtitle_purple_01, "Going Deeper: ", toc_lvl=TOC('+4')),
                        st_list(l.ordered, li_style = bs.large + bs.center_txt, block_list=
                                [
                                    """Legg, S., & Hutter, M. (2007). A collection of definitions of intelligence. 
                                                Frontiers in Artificial Intelligence and applications, 157, 17.""" +
                                                st_space() + 
                                                st_write(bs.blue_sub, "_", link="https://arxiv.org/pdf/0706.3639.pdf"),
                                    """Legg, S., & Hutter, M. (2007). Universal intelligence: A definition of machine
                                                 intelligence. Minds and machines, 17, 391-444. """ +
                                                st_space() + 
                                                st_write(bs.blue_sub, "_", link="https://www.arxiv-vanity.com/papers/0712.3329/"),
                                ])
                     ])
    

        
    return html