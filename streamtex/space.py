import streamlit as st
from streamlit.components.v2 import component
from .styles import Style, StreamTeX_Styles
from .enums import Tag, Tags
from .utils import contain_link, generate_key, strip_html
from typing import Literal

HTML_V = """
    <div style="padding-top: 0em;"></div>
"""

JS_V = """
    export default function(component) {
        const { parentElement, data } = component;
        
        // 1. Select container
        let element = parentElement.querySelector('div');
        
        // 2. Set Size
        element.style.paddingTop = data.size;
       
    }
"""

HTML_H = """
    <span style="padding-left: 0em;"></span>
"""

JS_H = """
    export default function(component) {
        const { parentElement, data } = component;
        
        // 1. Select container
        let element = parentElement.querySelector('span');
        
        // 2. Set Size
        element.style.paddingLeft = data.size;
       
    }
"""

space_component_v = component(
    "st_space_v",
    html=HTML_V,
    js=JS_V,
    isolate_styles=False
)  

space_component_h = component(
    "st_space_h",
    html=HTML_H,
    js=JS_H,
    isolate_styles=False
) 

def st_space(direction: Literal["v", "h"] = "v", size="1em"):
    """
    Generates an HTML tag to create vertical or horizontal spacing.

    :param direction: "v" for vertical spacing, "h" for horizontal spacing. Defaults to "v".
    :param size: The size of the space (e.g., "10px" or an integer, which will be converted to "em"). Defaults to "1em".
    :return: A string containing an HTML tag for the specified spacing.

    Notes:
    - Vertical spacing is implemented using `padding-top` and horizontal spacing uses `padding-left`.
    """
    # Convert integer size to em-based string
    if type(size) is int:
        size = str(size) + "em"
    
    # Use appropriate component based on orientation
    if direction == "v":
        # Vertical space with padding-top
        result = space_component_v(
            data = {"size": size},
            key = generate_key("space_v")
        )
    else:
        # Horizontal space with padding-left
        result = space_component_h(
            data = {"size": size},
            key = generate_key("space_h")
        )
        
    return result

def st_br():
   
   return st_space("v", 0)