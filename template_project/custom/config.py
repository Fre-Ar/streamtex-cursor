import streamtex_package.src.streamtex as sx
import streamtex_package.src.streamtex.styles as sts
from template_project.custom.styles import Styles as s
from template_project.custom.themes import dark



sts.theme = dark

#
sx.toc.numerate_title = False
sx.toc.toc_bck_index = 0
sx.toc.toc_title_style = s.project.titles.title_giant_green_01 + s.center_txt
sx.toc.toc_content_style = s.large + s.text.colors.reset






