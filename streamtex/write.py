from typing import Optional
import streamlit as st
from streamlit.components.v2 import component
from .styles import Style, StreamTeX_Styles
from .enums import Tag, Tags
from .utils import contain_link, generate_key, strip_html
from .toc import register_toc_entry

HTML = """
    <div style="">Text</div>
"""

JS = """
    export default function(component) {
        const { parentElement, data } = component;
        
        // 1. Select the initial container defined in HTML
        let element = parentElement.querySelector('div');
        
        // 2. Set Content and Styles
        element.innerHTML = data.txt;
        element.style.cssText = data.style;

        // 3. Handle Tag Transformation (e.g., div -> span, h1, etc.)
        if (data.tag !== 'div') {
            const newElement = document.createElement(data.tag);
            
            // Copy all child nodes (text)
            while (element.firstChild) {
                newElement.appendChild(element.firstChild);
            }
            
            // Copy all attributes (id, style, classes)
            Array.from(element.attributes).forEach(attr => {
                newElement.setAttribute(attr.name, attr.value);
            });
            
            // Replace the old div with the new tag in the DOM
            parentElement.replaceChild(newElement, element);
            element = newElement; // Update reference for the next step
        }
        
        // 4. Apply the Anchor ID if it exists
        if (data.id && data.id !== "") {
            // We set the ID on the specific element or a wrapper
            element.id = data.id; 
        }
        
        // 5. Handle Link Encapsulation
        if (data.link && data.link !== "" && data.link !== "None") {
            const anchor = document.createElement('a');
            anchor.href = data.link;
            
            // Apply link styles (e.g. text-decoration removal)
            if (data.link_style) {
                anchor.style.cssText = data.link_style;
            }

            // Wrap the element: Parent -> Anchor -> Element
            parentElement.replaceChild(anchor, element);
            anchor.appendChild(element);
        }
            
    }
"""

write_component = component(
    "st_write",
    html=HTML,
    js=JS,
    isolate_styles=False
)   


def _st_write(*args, style: Style = None, tag: Tag = Tags.span, link: str = "", no_link_decor: bool = False, hover=True, toc_lvl: Optional[str] = None, label: str = "" ):
    """
    Syntax:
        * st_write(s.header, "My Title")
        * st_write(s.header, (s.red, "R"), "ainbow ", (s.blue, "T"), "ext")
    """
    
    # --- 1. Argument Parsing ---
    container_style = StreamTeX_Styles.none
    content_args = args

    # Check if the first positional arg is a Style object (Wrapper Style)
    if len(args) > 0 and isinstance(args[0], Style):
        container_style = args[0]
        content_args = args[1:]
    elif style is not None:
        # Fallback if style was passed as a keyword arg
        container_style = style

    # --- 2. Build Inner HTML ---
    html_parts = []
    
    for item in content_args:
        if isinstance(item, tuple) and len(item) == 2:
            # It's a (Style, text) tuple -> wrap in span
            sub_style, sub_txt = item
            html_parts.append(f'<span style="{sub_style}">{sub_txt}</span>')
        else:
            # It's a string (or other object) -> append directly
            html_parts.append(str(item))
            
    final_txt = "".join(html_parts)
    
    # Determine link styling
    link_css = "position:relative;"
    if no_link_decor:
        link_css += " text-decoration: none; color: inherit;"
    
    # Handle ToC registration and element id 
    final_txt, key_anchor = _handle_toc(final_txt, toc_lvl, label)

    return write_component(
        data={
            "style": str(container_style),
            "txt": final_txt, 
            "tag": str(tag),
            "id": key_anchor,
            "link": str(link),
            "link_style": link_css
        },
        key=generate_key("write")
    )



def st_write(
    *args, style: Style = StreamTeX_Styles.none, tag: Tag = Tags.span, 
    link:str="", no_link_decor:bool=False, hover:bool=True, 
    toc_lvl: Optional[str] = None, label: str = "" ):
    """
    Function to write a styled string with optional link reference and table of content entry.
    
    :param args: The text or HTML content to wrap in the specified tag. See `Syntax` for example of usage.
    :param style: A Style object representing the CSS to apply to the text. Defaults to `StreamTeX_Styles.none`.
    :param tag: The HTML tag to use for wrapping the content (e.g., <span>, <div>). Defaults to `Tags.span`.
    :param link: An optional hyperlink to wrap around the content. If provided, the text will be clickable.
    :param no_link_decor: If True, removes text decoration (like underline) for links. Defaults to False.
    :param hover: If True, includes hover functionality to display additional information (e.g., link previews).
    :param toc_lvl: A numeric string that may start with '+' or '-' (e.g. '1', '-1' or '+1') denoting the toc level of this content. This allows the text to be part of a hierarchical TOC.
    :param label: An optional label to use for the TOC entry. If not provided, a truncated version of `txt` is used.

    Notes:
    - If `toc_lvl` is provided, the function wraps the content in tags to associate it with the specified TOC level.
    - Labels for TOC are automatically generated by truncating the text to a predefined length if no label is given.
    - The function uses `contain_link` to handle optional hyperlinking and link decorations.
    
    ## Syntax:
    - st_write(s.header, "My Title")
    - st_write(s.header, (s.red, "R"), "ainbow ", (s.blue, "T"), "ext")
    - st_write("click this ", (s.blue, "link", "https://google.com"))
    """
    
    # Parse style and txt arguments
    container_style, final_txt = _parse_args(*args, style)
    
    # Handle ToC registration and element id 
    final_txt, key_anchor = _handle_toc(final_txt, toc_lvl, label)
    elementId = f" id='{key_anchor}'" if key_anchor else ""
    
    # Wrap the text in the specified tag with the given style. This ensures consistent styling.   
    txt_tag = f'<{tag}{elementId} style="{container_style}">{final_txt}</{tag}>'
    
    # Handle optional hyperlinking and hover effects.
    txt_tag = contain_link(txt_tag, link, no_link_decor, hover)
    
    st.html(txt_tag)

def _parse_args(*args, style: Style = StreamTeX_Styles.none, hover:bool=False):
    """
    Parses arguments to distinguish between Wrapper Styles, Text, and Tuples.
    """
    container_style = StreamTeX_Styles.none
    content_args = args

    # Check if the first arg is a Wrapper Style
    if len(args) > 0 and isinstance(args[0], Style):
        container_style = args[0]
        content_args = args[1:]
    elif style is not None:
        # Fallback if style was passed as a keyword arg
        container_style = style

    # Build Inner HTML
    html_parts = []
    
    for item in content_args:
        if isinstance(item, tuple):
            # --- CASE 1: (Style, Text) ---
            if len(item) == 2:
                sub_style, sub_txt = item
                sub_link = ''
            
            # --- CASE 2: (Style, Text, Link) ---
            elif len(item) == 3:
                sub_style, sub_txt, sub_link = item
            
            span = f'<span style="{sub_style}">{sub_txt}</span>'
            span = contain_link(span, sub_link, no_link_decor=False, hover=hover)

            html_parts.append(span)

        else:
            # String or other object
            html_parts.append(str(item))
            
    final_txt = "".join(html_parts)
    
    return container_style, final_txt

def _handle_toc(final_txt: str, toc_lvl: Optional[str] = None, label: str = ""):
        # --- 3. Handle ToC Registration ---
    key_anchor = ""
    if toc_lvl:
        # If no label is provided, generate a truncated label from the text. This ensures TOC entries are descriptive
        # but not overly long, avoiding clutter in the TOC.
        if not label:
            label_length = 73
            clean_label = strip_html(final_txt)  # Remove HTML tags to generate a clean label
            label = (clean_label[:label_length] + '..') if len(clean_label) > label_length else clean_label

        # Generate the opening and closing TOC tags for the specified level and label.
        key_anchor, section_number = register_toc_entry(label, toc_lvl)
        final_txt = section_number + final_txt # Prepend the numbering of the ToC title

    return final_txt, key_anchor
