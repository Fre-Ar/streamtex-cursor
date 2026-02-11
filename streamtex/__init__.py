import streamlit as st
from streamlit.delta_generator import DeltaGenerator as Delta
import time
import os

from .styles import Style
from .write import st_write
from .image import st_image
from .container import st_block, st_span
from .space import st_space, st_br
from .grid import st_grid
from .list import st_list
from .overlay import st_overlay
from .toc import reset_toc_registry, toc_entries, TOCConfig
from .enums import Tags
from .utils import inject_link_preview_scaffold

import importlib.resources as resources

streamtex_zoom = "streamtex_zoom"

def st_book(module_list, toc_config: TOCConfig = None, *args, **kwargs):
    """Generates a web page e-book from a list of block modules."""
    start_time = time.time()
    print("Starting st_book function...")

    # Load default CSS styles
    load_css("default.css")
    
    # Ensure the hover card is ready before any content is rendered.
    inject_link_preview_scaffold()
    
    # Add zoom options to sidebar
    add_zoom_options()
    
    # Clear previous run's headers
    reset_toc_registry(toc_config)
    
    # Extract ToC config and create ToC placeholders
    use_toc_sidebar = toc_config is not None 
    use_toc_block = use_toc_sidebar and toc_config.toc_position is not None
    if use_toc_sidebar:
        toc_sidebar = build_ToC_sidebar_placeholder()
        toc_block = None
        toc_content_style = None
    if use_toc_block:  
        # Determine ToC insertion position
        toc_pos = toc_config.toc_position
        if toc_pos < 0 or toc_pos >= len(module_list):
            toc_pos = len(module_list)
        toc_title_style = toc_config.title_style
        toc_content_style = toc_config.content_style

    # Run the blocks (potentially populating the ToC registry)
    for i, module in enumerate(module_list):
        
        # Generate Toc at appropriate position
        if use_toc_block and i == toc_pos:
            toc_block = st_toc(toc_title_style)
        
        # TODO: Wrap block in a way to trace it back to module name
        st_include(module, *args, **kwargs)
        st_space("v","70px")
    
    # Generate Toc at appropriate position
    if use_toc_block and toc_pos == len(module_list):
        toc_block = st_toc(toc_title_style)
    
    # Fill the ToC placeholder
    if use_toc_sidebar:
        populate_toc(toc_sidebar, toc_block, toc_content_style)
        
    end_time = time.time()
    duration = end_time - start_time
    print(f"st_book function completed in {duration:.2f} seconds.")


def load_css(file_name: str):
    """Loads a CSS file and injects it into the StreamTeX app."""
    try:
        with resources.open_text('streamtex.static', file_name) as f:
            st.html(f'<style>{f.read()}</style>')
    except:
        current_dir = os.path.dirname(__file__)
        static_dir = os.path.join(current_dir, 'static')
        css_file_path = os.path.join(static_dir, file_name)
        # Read the CSS file
        with open(css_file_path, 'r') as f:
            st.html(f'<style>{f.read()}</style>')

def add_zoom_options():
    """Adds a generic 'View Options' menu to the sidebar using a popover."""
    
    # 1. Initialize State
    if streamtex_zoom not in st.session_state:
        st.session_state[streamtex_zoom] = "Fit"

    # 2. Define Options
    zoom_levels = ["Fit", 50, 75, 90, 100, 110, 125, 150, 175, 200]
    
    # 3. Create the Menu (Popover)
    with st.sidebar:
        option = st.selectbox(
            "**Zoom Level**",
            options=zoom_levels,
            format_func=lambda x: x if x == "Fit" else f"{x}%",
            index=zoom_levels.index(st.session_state[streamtex_zoom]) 
                      if st.session_state[streamtex_zoom] in zoom_levels else 0,
            key="streamtex_zoom_list"
        )
        
        # Update state if changed
        if option != st.session_state[streamtex_zoom]:
            st.session_state[streamtex_zoom] = option
            st.rerun() # Force rerun to apply CSS immediately
    
    # 4. Apply the styles
    inject_zoom_logic(st.session_state.streamtex_zoom)

# streamtex/__init__.py

def inject_zoom_logic(zoom_setting):
    """
    Applies the fixed page layout and handles 'Fit' vs 'Fixed' scaling.
    """
    
    # Constants defined by user
    # 17 inches * 72 pt/inch = 1224 pt
    PAGE_WIDTH = "1224pt" 
    # 0.5 inches * 72 pt/inch = 36 pt
    PAGE_PADDING = "36pt" 

    # Logic decision
    if zoom_setting == "Fit":
        # JS mode: Calculate scale based on viewport width
        # We target .stMain (the scrollable area) minus some buffer
        scale_val = "var(--streamtex-fit-scale, 1)"
        js_logic = """
        <script>
            function updateScale() {
                const main = document.querySelector('.stMain');
                const page = document.querySelector('.block-container');
                
                if (main && page) {
                    // Convert 1224pt to approx pixels for calculation (1pt ~= 1.33px)
                    // Or better: get the rendered offsetWidth of the fixed page
                    const pageWidthPx = page.scrollWidth; 
                    const availableWidth = main.clientWidth - 40; // 40px buffer for scrollbars
                    
                    const scale = availableWidth / pageWidthPx;
                    document.documentElement.style.setProperty('--streamtex-fit-scale', scale);
                }
            }
            
            // Run on load and resize
            updateScale();
            window.addEventListener('resize', updateScale);
            
            // Streamlit sometimes re-renders DOM, so we observe it
            new MutationObserver(updateScale).observe(document.body, {childList: true, subtree: true});
        </script>
        """


def inject_zoom_logic(zoom_setting):
    """
    Applies page layout and calculates negative margins to remove whitespace.
    """
    
    # Constants
    # 17 inches * 72 pt/inch = 1224 pt
    PAGE_WIDTH = "1224pt" 
    # 0.5 inches * 72 pt/inch = 36 pt
    PAGE_PADDING = "36pt" 

    # 1. Determine Scale Strategy
    if zoom_setting == "Fit":
        # Calculate scale based on viewport
        scale_val = "var(--streamtex-fit-scale, 1)"
        
        # Logic to determine the Fit Ratio
        fit_logic_js = """
            const main = document.querySelector('.stMain');
            if (main && page) {
                const pageWidthPx = page.scrollWidth; 
                // 40px buffer for scrollbars
                const availableWidth = main.clientWidth - 40; // 40px buffer for scrollbars
                const scale = availableWidth / pageWidthPx;
                document.documentElement.style.setProperty('--streamtex-fit-scale', scale);
            }
        """
    else:
        # Fixed mode
        scale_val = zoom_setting / 100.0
        fit_logic_js = "" # No calculation needed

    # 2. Fix the Whitespace
    # This calculates: Layout Gap = Original Height - (Original Height * Scale)
    # And applies it as a negative margin.
    js_logic = f"""
    <script>
        function updateLayout() {{
            const page = document.querySelector('.block-container');
            if (!page) return;
            
            // 1. Run Fit Logic if needed
            {fit_logic_js}

            // 2. Read the active scale (Fit or Fixed)
            const rootStyle = getComputedStyle(document.documentElement);
            const scale = parseFloat(rootStyle.getPropertyValue('--streamtex-scale')) || 
                          parseFloat(rootStyle.getPropertyValue('--streamtex-fit-scale')) || 1;
            
            
            // 3. Calculate 'Ghost Space'
            // offsetHeight is the Unscaled Layout Height
            const origHeight = page.offsetHeight;
            const visualHeight = origHeight * scale;
            const ghostSpace = origHeight - visualHeight;
            
            // 4. Apply Negative Margin to collapse the gap
            // We leave a small 50px buffer so it's not too tight
            page.style.marginBottom = `-${{ghostSpace - 50}}px`;
        }}
        
        // Triggers
        window.addEventListener('resize', updateLayout);
        
        // Observer: Streamlit changes DOM content (height) frequently
        new MutationObserver(updateLayout).observe(document.body, {{
            childList: true, subtree: true, attributes: true
        }});
        
        // Run immediately
        setTimeout(updateLayout, 100);
    </script>
    """

    css = f"""
    <style>
        :root {{
            --streamtex-scale: {scale_val};
        }}
        
        .stMain .block-container {{
            /* Dimensions */
            width: {PAGE_WIDTH} !important;
            min-width: {PAGE_WIDTH} !important;
            max-width: {PAGE_WIDTH} !important;
            
            /* Padding */
            padding-left: {PAGE_PADDING} !important;
            padding-right: {PAGE_PADDING} !important;
            
            /* Scaling */
            transform: scale(var(--streamtex-scale));
            transform-origin: top center;
        }}
    </style>
    """
    
    st.html(css)
    st.html(js_logic, unsafe_allow_javascript=True)
       
def build_ToC_sidebar_placeholder():
    with st.sidebar:
        st.header("Table of Contents")
        toc_sidebar = st.empty()
    
    return toc_sidebar

def populate_toc(toc_sidebar: Delta, toc_block: Delta=None, toc_content_style: Style =None):
    toc_entry_list = toc_entries()
    indent_char="&nbsp;"
        
    with toc_sidebar.container():
        for entry in toc_entry_list:
            # Indentation based on level
            indent = indent_char * (entry['level'] - 1) * 4
            
            # Native Streamlit Link to ID
            st.html(
                f"<span style=\"overflow: hidden; text-overflow: ellipsis; text-wrap: nowrap; word-wrap: normal;\">"
                f"{indent}<a href=\"#{entry['key_anchor']}\">{entry['title']}</a></span>"
            )
    if toc_block is not None:
        with toc_block.container():
            for entry in toc_entry_list:
                indent = indent_char * (entry['level'] - 1) * 2
                st_write(toc_content_style, f"{indent}{entry['title']}",
                                link=f"#{entry['key_anchor']}", hover=False, no_link_decor=True)
                st_br()
                
                
            
            
def st_toc(toc_title_style):
    st_write(toc_title_style, "Table of Contents", tag=Tags.div, toc_lvl='1')
    st_space("v",4)
    toc_block = st.empty()
    st_space("v","70px")
    return toc_block

def st_include(block_file_module, *args, **kwargs):
    if not block_file_module:
        st.markdown(f":red-background[File {block_file_module.__path__} not found]")
        return

    if not hasattr(block_file_module, 'build'):
        st.markdown(f":red-background[The file {block_file_module.__path__} does not contain a build() function.]")
        return 
    
    block_file_module.build(*args, **kwargs)