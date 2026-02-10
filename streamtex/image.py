import os
import streamlit as st
from .styles import Style, StreamTeX_Styles
from .utils import __is_url, __is_absolute_path, __is_relative_path, __get_mime_type, __get_base64_encoded_image

def st_image(
    style: Style = StreamTeX_Styles.none,
    width="100%", height="auto",
    uri: str="", alt:str="",
    link:str="", hover:bool=True
):
    """
    Renders an image using st.html directly.
    """
    # 1. Convert integer sizes to pixel-based strings
    if isinstance(width, int):
        width = f"{width}px"
    if isinstance(height, int):
        height = f"{height}px"
    
    # 2. Get the source (URL or Base64)
    img_src = get_image_src(uri)

    # 3. Construct the CSS style string
    # We add 'display: block' to ensure the image behaves correctly in the layout 
    # and doesn't have inline line-height gaps.
    # We allow the passed 'style' to override or add to this.
    css_style = f"{str(style)} width: {width}; height: {height};"

    # 4. Construct the HTML
    html_content = f'<img src="{img_src}" alt="{alt}" style="{css_style}">'

    # 5. Handle Link Wrapping
    if link and link != "None":
        # Wrap the image in an anchor tag if a link is provided
        # We ensure the anchor is inline-block so it wraps the image tightly
        html_content = f'<a href="{link}">{html_content}</a>'

    # 6. Render
    st.html(html_content)

def get_image_src(uri: str) -> str:
    """
    Resolves the image source from a URL, absolute path, relative path, or static file.
    """
    img_src = ""
    if __is_url(uri):
        # If it's a URL, use it directly
        img_src = uri
    elif __is_absolute_path(uri) or __is_relative_path(uri):
        # If it's an absolute or relative path, try converting the file to base64
        file_path = uri if __is_absolute_path(uri) else os.path.join(os.getcwd(), uri)
        
        # Check if file exists before trying to read it
        if os.path.exists(file_path):
            mime_type = __get_mime_type(file_path)
            encoded_image = __get_base64_encoded_image(file_path)
            if mime_type and encoded_image:
                # Use base64 encoding for local files with correct MIME type
                img_src = f"data:{mime_type};base64,{encoded_image}"
            else:
                img_src = ""  # Unsupported format or encoding failed
        else:
            img_src = "" # File not found
    else:
        # If no specific relative or absolute indicator, assume it's a static path (Legacy behavior)
        # Note: You might want to update this logic if your static handling changes
        img_src = f"app/static/images/{uri}"
        
    return img_src

