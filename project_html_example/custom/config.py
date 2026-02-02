import streamtex_package.src.streamtex as sx
import streamtex_package.src.streamtex.styles as sts

from project_html_example.custom.styles import Styles as s
from project_html_example.custom.themes import dark


sts.theme = dark

# Table of contents styling
sx.toc.numerate_title = False
sx.toc.toc_bck_index = 0
sx.toc.toc_title_style = s.project.titles.table_of_contents
sx.toc.toc_content_style = s.large + s.text.colors.reset



