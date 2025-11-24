import streamlit as st
import template_project.blocks
from streamtex_package.src.streamtex import *
from template_project.custom.styles import Styles as s
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l


"""
List of st_* functions implemented in the StreamTeX library:

- function()    # parameters

- st_book()     # module_list
- st_write()    # style, txt, link, hover, no_link_decor, tag, toc_lvl, label
- st_image()    # style, width, height, uri, alt, link, hover
- st_space()    # direction, size
- st_br()       #
- st_include()  # module
- st_block()    # style, block_list, tag
- st_list()     # list_type, l_style, li_style, block_list, level, stickToText
- st_grid()     # rows, cols, grid_style, cell_styles, block_list
- st_table()    # rows, cols, table_style, row_styles, cell_styles, block_list
- st_sheet()    # rows, cols, grid_style, cell_styles, block_list
- st_iframe()   # url, width, height

-----------------------------------

Hierarchy of Styles:


Styles:
- `none`: base style
- `text`: Text Styles enum
- `container`: Container (divs) styles enum
- `visibility`: Element visibility enum (hidden, visible or invisible)
- `project`: User defined styles enum

text
- `decors`: Italic, underline, and no-decoration styles.  
- `weights`: Bold, light, and normal text weights.  
- `alignments`: Text alignment styles (left, center, right).  
- `colors`: Foreground color styles.  
- `bg_colors`: Background color styles.  
- `sizes`: Font size styles (em, px, and pt units).  
- `fonts`: Font families for various types (sans-serif, serif, monospace, etc.).

container
- `sizes`: Container width and height.  
- `bg_colors`: Background color styles.  
- `borders`: Border styles.  
- `paddings`: Padding styles.  
- `margins`: Margin styles.  
- `layouts`: Layout options (e.g., flexbox, table).  
- `flex`: Flexbox-specific layout properties.  
- `lists`: List-specific styles (e.g., Google Docs style).

project
- `colors`: User-defined colors.  
- `titles`: Custom title and subtitle styles. 

"""

class BlockStyles:
    """Custom styles for this block."""
    header_style = s.Giant + s.text.colors.blue
    grid_cell_style = ns("border: 1px solid gray;") + s.container.paddings.little_padding + s.center_txt
    list_item_style = s.text.colors.green + s.bold
    table_style = ns("border: 2px solid black; width: 100%;")
bs = BlockStyles


def html_block():

    html = ""     

    # st_write example
    html += st_write(bs.header_style, "Dynamic HTML Generator Example", t.h1)

        # st_space example (horizontal)
    html += st_space("h", "20px")  # Horizontal space for layout adjustment

    # st_write example (with all parameters)
    html += st_write(style=s.none,
                     txt='example_link',
                     tag=t.div,
                     link="https://example.com/",
                     no_link_decor=True,
                     hover=False,
                     toc_lvl=TOC("1"), label="Example ToC Label")
    # st_space example (vertical)
    html += st_space("v", "2em")  # Vertical space

    # st_list example
    html += st_list(list_type=l.unordered,
                    l_style=s.none,
                    li_style=bs.list_item_style,
                    block_list=["List Item 1", "List Item 2", ["Nested Item 1", "Nested Item 2"]])

    # st_image example
    html += st_image(
        style=s.none,
        width="1000px",
        height="100%",
        uri="placeholder.png",
        alt="Placeholder Image",
        link="https://example.com",
        hover=True)

    # st_br example
    html += st_br()  # Line break

    # st_grid example
    html += st_grid(rows=2,
                    cols=3,
                    cell_styles=bs.grid_cell_style,
                    block_list=[
                        "Cell 1", "Cell 2", "Cell 3",
                        "Cell 4", "Cell 5", "Cell 6",
                    ])

    # st_table example
    html += st_table(
        rows=2,
        cols=2,
        table_style=bs.table_style,
        cell_styles=bs.grid_cell_style,
        block_list=[
            ["Row 1, Col 1", "Row 1, Col 2"],
            ["Row 2, Col 1", "Row 2, Col 2"],
        ])

    # both st_grid and st_table benefit from row and column auto-detection,
    # as well as the use stylegrids (multiplication replaces, addition adds)

    html += st_grid(
        cell_styles = sg.create("A1:B3", s.large) * sg.create("A1:B1, B3", s.text.colors.white + s.container.bg_colors.red_bg),
        block_list=[
            ["A1", "B1"],
            ["A2", "B2"],
            ["A3", "B3"],
        ])
    
    html += st_block(style=s.center_txt + s.big,
                     block_list=[
                         st_write("This is inside a div. Normally, st_yrite defaults to a span tag. The block styles cascade.")
                     ])
        
    return html


