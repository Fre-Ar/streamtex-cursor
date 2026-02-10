import streamlit as st
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from .styles import Style, StreamTeX_Styles as s, ListStyle
from .container import st_block
from .enums import ListType, ListTypes

# Global context variable to track nesting level
_current_list_level = ContextVar("list_level", default=0)

class ListController:
    def __init__(self, li_style: Style, bullet_content: str):
        self.li_style = li_style
        self.bullet_content = bullet_content

    @contextmanager
    def item(self, style: Style = None):
        """
        Creates a list item.
        """
        # 1. Determine Style
        final_style = self.li_style
        if style:
            final_style = final_style + style

        # 2. Generate ID
        item_id = f"li-{uuid.uuid4().hex}"

        # 3. Inject CSS
        # We use the bullet_content passed from the parent list (calculated based on level)
        css = f"""
        <style>
            /* Container: acts as the LI wrapper */
            div[data-testid="stVerticalBlock"]:has(> .element-container .stHtml span.{item_id}) {{
                padding-left: 3.5rem;
                position: relative;
                overflow: visible !important;
                counter-increment: streamtex-counter;
            }}
            
            /* Bullet Point: acts as the marker */
            div[data-testid="stVerticalBlock"]:has(> .element-container .stHtml span.{item_id})::before {{
                content: {self.bullet_content};
                position: absolute;
                left: 0rem;
                width: 1.2rem;
                text-align: right;
                color: inherit;
                pointer-events: none;
            }}
        </style>
        """
        st.html(css)

        # 4. Render
        with st_block(style=final_style):
            st.html(f'<span class="{item_id}" style="display:none"></span>')
            yield


@contextmanager
def st_list(
    list_type: ListType = ListTypes.unordered, 
    l_style: Style = s.none, 
    li_style: Style = s.none
):
    """
    Context Manager for Lists.
    Supports custom ListStyle symbols based on nesting level.
    """
    
    # 1. Automatic Level Detection
    current_level = _current_list_level.get()
    next_level = current_level + 1
    token = _current_list_level.set(next_level) 

    try:
        # 2. Resolve List Style (CSS)
        # If l_style is a ListStyle, we assume its main CSS (font, etc) applies to the wrapper
        applied_list_style = l_style
        
        # 3. Resolve Bullet Symbol
        # We calculate the string to be used in 'content: ...' CSS property
        bullet_content = "'•'" # Default fallback

        if list_type == ListTypes.ordered:
            # Ordered lists use CSS counters regardless of ListStyle symbols
            bullet_content = "counter(streamtex-counter) '.'"
        
        elif isinstance(l_style, ListStyle) and l_style.symbols:
            # --- CUSTOM SYMBOL LOGIC ---
            # Use the logic from your class: index = (lvl - 1) % len(symbols)
            # We access the .symbols attribute directly
            idx = (next_level - 1) % len(l_style.symbols)
            symbol_char = l_style.symbols[idx]
            
            # Escape quotes if necessary for CSS string
            bullet_content = f"'{symbol_char}'"
        
        else:
            # Default fallback for simple Styles (Disc -> Circle -> Square)
            if next_level == 2: bullet_content = "'○'"
            elif next_level >= 3: bullet_content = "'■'"

        # 4. Generate ID & CSS for the Wrapper
        list_id = f"ul-{uuid.uuid4().hex}"
        
        css = f"""
        <style>
            div[data-testid="stVerticalBlock"]:has(> .element-container .stHtml span.{list_id}) {{
                counter-reset: streamtex-counter;
                gap: 0.2rem;
                width: 100%; /* Ensure it takes width unless restricted */
            }}
        </style>
        """
        st.html(css)

        # 5. Render Container
        with st_block(style=applied_list_style):
            st.html(f'<span class="{list_id}" style="display:none"></span>')
            
            # We pass the pre-calculated bullet_content to the controller
            yield ListController(li_style=li_style, bullet_content=bullet_content)
            
    finally:
        _current_list_level.reset(token)