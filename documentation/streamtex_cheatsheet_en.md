# 📚 Streamtex Complete Cheatsheet

## 📥 Essential Imports

```python
from streamtex_package.src.streamtex import *
from streamtex_package.src.streamtex.styles import Style as ns, StyleGrid as sg
from streamtex_package.src.streamtex.streamtex_enums import Tags as t, ListTypes as l
```

## 🎨 Style Organization

### Custom Style Class

```python
class BlockStyles:
    """Custom styles defined locally and used only for this block"""
    # Composed styles
    content = s.Large + s.center_txt
    lime_bold = s.text.colors.lime + s.bold
    bold_green = s.project.colors.green_01 + s.bold
    
    # Styles with alignment
    green_title = bold_green + s.huge + s.center_txt
    
    # Styles with borders
    border = s.container.borders.color(s.text.colors.black) + \
             s.container.borders.solid_border + \
             s.container.borders.size("2px")
    
    # Styles with padding
    side_padding = ns("padding: 10pt 36pt;")
bs = BlockStyles
```

## 📝 Basic Elements

### Blocks and Text

```python
# Simple block with style
html += st_block(s.center_txt, [
    st_write(bs.green_title, "My Title"),
    st_space(size=3)
])

# Block with list
html += st_block(s.center_txt, [
    st_list(
        list_type=l.ordered,
        li_style=bs.content,
        block_list=[
            st_write(txt="First item"),
            st_write(txt="Second item")
        ]
    )
])
```

### Images and Media

```python
# Simple image
st_image(uri="image.png")

# Image with dimensions
st_image(uri="image.png", width="1150px", height="735.34px")

# Image with link
st_image(uri="image.png", link="https://example.com")

# Image with auto-height style
st_image(s.container.sizes.height_auto, uri="image.png")
```

### Grids and Tables

```python
# 3x2 grid
html += st_grid(3, 2, 
    cell_styles=bs.border + s.container.paddings.little_padding,
    block_list=[
        st_image(uri="image1.png"),
        st_image(uri="image2.png"),
        st_image(uri="image3.png")
    ]
)

# Table with custom styles
html += st_table(
    cell_styles=sg.create("A1,A3", s.project.colors.orange_02) +
                sg.create("A2", s.project.colors.red_01) +
                sg.create("A1:B3", s.bold + s.LARGE),
    block_list=[
        ["Title", "Link"],
        ["Item 1", "link1"],
        ["Item 2", "link2"]
    ]
)
```

## 🔗 Links and Navigation

### Links

```python
# Simple link
st_write(txt="Click here", link="https://example.com")

# Styled link
link_style = s.text.colors.blue + s.text.decors.underline_text
st_write(link_style, txt="Styled link", link="https://example.com", no_link_decor=True)
```

### Table of Contents

```python
# Top level
st_write(style, "Section", toc_lvl=TOC("1"))

# Sub-level
st_write(style, "Subsection", toc_lvl=TOC("+1"))
```

## 🎯 Predefined Styles

### Colors

```python
# Project colors
s.project.colors.blue_01
s.project.colors.green_01
s.project.colors.orange_01
s.project.colors.red_01
s.project.colors.brown_01

# Text colors
s.text.colors.lime
s.text.colors.black
```

### Text Sizes

```python
s.huge          # Very large
s.LARGE         # Larger
s.Large         # Large
s.large         # Normal
```

### Alignment and Layout

```python
s.center_txt
s.container.flex.center_align_items
s.container.layouts.vertical_center_layout
```

### Decorations

```python
s.bold
s.italic
s.text.decors.underline_text
```

## 🔧 Utilities

### Spacing

```python
# Vertical space
st_space(size=3)
st_space("v", size=2)

# Horizontal space
st_space("h", size=1)

# Line break
st_br()
```

### Containers

```python
# Padding
s.container.paddings.little_padding
s.container.paddings.small_padding

# Borders
s.container.borders.solid_border
s.container.borders.size("2px")
```

## 💡 Complete Examples

### Docs Page

```python
def html_block():
    html = ""
    html += st_block(bs.center_txt, [
        st_write(bs.green_title, "Documentation"),
        st_space(size=3),
        st_list(l.ordered, bs.content, [
            "First point",
            "Second point"
        ])
    ])
    return html
```

### Showcase with Grid

```python
def html_block():
    html = ""
    ### 3 rows, 2 columns grid
    html += st_grid(3, 2, 
        cell_styles=bs.border,
        block_list=[
            st_image(uri="image1.png"),
            st_image(uri="image2.png"),
            st_write(bs.content, "Description")
        ]
    )
    return html
```

### Full Page Example

```python
def html_block():
    html = ""

    # Header with title
    html += st_block(s.center_txt + s.LARGE + s.bold, [
        st_write(s.project.colors.blue_01 + s.huge, "Main Title", toc_lvl=TOC("1")),
        st_space(size=2),
        st_write(s.project.colors.orange_01, "Subtitle", toc_lvl=TOC("+1")),
        st_space(size=3)
    ])

    # Main content
    html += st_block(s.center_txt, [
        st_list(
            list_type=l.ordered,
            li_style=bs.content,
            block_list=[
                st_write(txt="Section 1"),
                st_write(txt="Section 2"),
                st_write(txt="Section 3")
            ]
        )
    ])

    # Image grid
    html += st_grid(2, 2,
        cell_styles=bs.border + s.container.paddings.little_padding,
        block_list=[
            st_image(uri="image1.png"),
            st_image(uri="image2.png"),
            st_write(bs.content, "Description 1"),
            st_write(bs.content, "Description 2")
        ]
    )

    # Links and references
    html += st_block(s.center_txt + s.Large, [
        st_write(bs.link_style, txt="Link 1", link="https://example1.com"),
        st_space(size=1),
        st_write(bs.link_style, txt="Link 2", link="https://example2.com")
    ])

    return html
```

## 📌 Important Notes

1. Always initialize HTML with `html = ""`
2. Use style classes to organize code
3. Combine styles with the `+` operator
4. Use `st_space()` to manage spacing
5. Keep a proper heading hierarchy for the table of contents

## 🔍 Tips and Best Practices

1. Group common styles in a `BlockStyles` class
2. Use variables for reusable styles
3. Comment complex sections
4. Structure code into logical sections
5. Use vertical spacing to improve readability
