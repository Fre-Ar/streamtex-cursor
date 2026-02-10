import os
from typing import Optional
import streamlit as st
from streamlit.components.v2 import component
from .styles import Style, StreamTeX_Styles
from .enums import Tag, Tags
from .utils import contain_link, generate_key, __is_url, __is_absolute_path, __is_relative_path, __get_mime_type, __get_base64_encoded_image
from .toc import register_toc_entry

HTML = """
    <img/>
"""

JS = """
    export default function(component) {
        const { parentElement, data } = component;
        
        // 1. Select the initial container defined in HTML
        let element = parentElement.querySelector('img');
        
        // 2. Set Content and Styles
        element.src = data.src;
        element.style.cssText = data.style;
        if (data.alt)
            element.alt = data.alt;
    
        // 3. Handle Link Encapsulation
        if (data.link && data.link !== "" && data.link !== "None") {
            const anchor = document.createElement('a');
            anchor.href = data.link;
            console.log("Wrapping image whose parent is:", parentElement);

            // Wrap the element: Parent -> Anchor -> Element
            element.parentNode.replaceChild(anchor, element);
            anchor.appendChild(element);
        }
            
    }
"""

image_component = component(
    "st_image",
    html=HTML,
    js=JS,
    isolate_styles=False
)   

def st_image(
    style: Style = StreamTeX_Styles.none,
    width="100%", height="100%",
    uri: str="", alt:str="",
    link:str="", hover:bool=True
):
    # Convert integer size to pixel-based string
    if type(width) is int:
        width = str(width) + "px"
    if type(height) is int:
        height = str(height) + "px"
    
    img_src = get_image_src(uri)
    #img_tag = contain_link(img_tag, link, False, hover)

    result = image_component(
        data = {
            "style": f"{style} width: {width}; height: {height};",
            "src": img_src,
            "alt": alt,
            "link": str(link),
        },
        key=generate_key("image")
    )
    return result

def get_image_src(uri: str) -> str:
    img_src = ""
    if __is_url(uri):
        # If it's a URL, use it directly
        img_src = uri
    elif __is_absolute_path(uri) or __is_relative_path(uri):
        # If it's an absolute or relative path, try converting the file to base64
        file_path = uri if __is_absolute_path(uri) else os.path.join(os.getcwd(), uri)
        mime_type = __get_mime_type(file_path)
        encoded_image = __get_base64_encoded_image(file_path)
        if mime_type and encoded_image:
            # Use base64 encoding for local files with correct MIME type
            img_src = f"data:{mime_type};base64,{encoded_image}"
        else:
            img_src = ""  # Missing image or unsupported format
    else:
        # If no specific relative or absolute indicator, assume it's a static path
        img_src = f"app/static/images/{uri}"
    return img_src
    