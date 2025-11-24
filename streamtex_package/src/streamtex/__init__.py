import html as html_lib
import uuid
import streamlit as st
import os
from typing import Literal, List, Union, Optional
import importlib.resources as resources
from streamlit.components.v1 import html as htmljs
from requests.exceptions import ConnectionError, Timeout

from .styles import StreamTeX_Styles as s
from .styles import *
from .streamtex_enums import *
import time


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
"""

### Javascript code used by st_book()

zoom_js_code = r"""
function zoom_func() {
    let mainDiv = document.querySelector(".stMainBlockContainer > div > div");
    if (!mainDiv) {
        alert("main div not found.");
        return;
    }

    let parentDiv = document.querySelector(".stMainBlockContainer");
    if (!parentDiv) {
        alert("parent div not found.");
        return;
    }
        
    // Force transform origin
    mainDiv.style.transformOrigin = "top left";
    // Default to 100% scale
    mainDiv.style.transform = "scale(1)";
    mainDiv.style.display = "inline-block";

    // Find the <select> we created in st_book
    let zoomSelect = document.getElementById("zoomSelect");
    if (!zoomSelect) {
        alert("zoom select not found.");
        return;
    }

    let defaultZoom = 100;

    // Set that in the dropdown
    zoomSelect.value = String(defaultZoom);
    mainDiv.style.transform = `scale(${defaultZoom / 100})`;

    const scaledHeight = (100 / defaultZoom) *  100;
    mainDiv.style.height = scaledHeight + "vh";

    const scaledWidth = (17*72) *  (100 / defaultZoom);
    mainDiv.style.width = scaledWidth + "pt";
    mainDiv.style.maxWidth = scaledWidth + "pt";
    mainDiv.style.minWidth = scaledWidth + "pt";
    

    // Listen for changes in the dropdown
    zoomSelect.addEventListener('change', function(e) {
        let val = parseFloat(e.target.value);
        mainDiv.style.transform = `scale(${val / 100})`;

        const scaledHeight = (100/val) *  100;
        mainDiv.style.height = scaledHeight + "vh";

        const scaledWidth = (17*72) *  (100 / val);
        mainDiv.style.width = scaledWidth + "pt";
        mainDiv.style.maxWidth = scaledWidth + "pt";
        mainDiv.style.minWidth = scaledWidth + "pt";
    });

}
zoom_func();
"""

js_code = r"""
document.querySelectorAll('a[data-preview]').forEach(link => {
  // We'll track whether the mouse is in the link or the tooltip
  let mouseInLink = false;
  let mouseInTooltip = false;

  link.addEventListener('mouseenter', (e) => {
    mouseInLink = true;
    const previewHTML = link.getAttribute('data-preview');
    if (!previewHTML) return;

    // Create the tooltip div if it doesn't exist
    if (!link._tooltip) {
      const tooltip = document.createElement('div');
      tooltip.innerHTML = previewHTML;
      tooltip.className = 'hover-tooltip'; // For styling

      // Basic styling
      tooltip.style.position = 'absolute';
      tooltip.style.padding = '5px 10px';
      tooltip.style.border = '1px solid #ccc';
      tooltip.style.borderRadius = '8px';
      tooltip.style.boxShadow = '0 2px 4px rgba(0,0,0,0.15)';
      tooltip.style.backgroundColor = '#fff';
      tooltip.style.color = '#3c4043';
      tooltip.style.fontSize = '14px';
      tooltip.style.zIndex = '9999';
      tooltip.style.pointerEvents = 'auto'; // So it can handle mouseenter/leave

      // Position at bottom-left of link
      const rect = link.getBoundingClientRect();
      const leftPos = rect.left + window.pageXOffset;
      const topPos  = rect.bottom + window.pageYOffset; // below the link
      tooltip.style.left = leftPos + 'px';
      tooltip.style.top  = topPos + 'px';

      // Attach event listeners to the tooltip
      tooltip.addEventListener('mouseenter', () => {
        mouseInTooltip = true;
      });
      tooltip.addEventListener('mouseleave', () => {
        mouseInTooltip = false;
        maybeRemoveTooltip(link);
      });

      document.body.appendChild(tooltip);
      link._tooltip = tooltip;
    }
  });

  link.addEventListener('mouseleave', (e) => {
    mouseInLink = false;
    maybeRemoveTooltip(link);
  });

  function maybeRemoveTooltip(linkElem) {
    // If mouse is neither over the link nor the tooltip, remove it
    if (!mouseInLink && !mouseInTooltip && linkElem._tooltip) {
      linkElem._tooltip.remove();
      linkElem._tooltip = null;
    }
  }
});
"""


def module_hover_js():
    """
    Returns a JavaScript string that:
    - Defines one function: moduleHoverFunc()
    - Immediately calls moduleHoverFunc() at the end.
    """
    return r"""
function moduleHoverFunc() {
    let hoveredBlock = null;



    // Track the .block-container element over which the user is hovering.
    document.querySelectorAll('.block-container').forEach(block => {
      block.addEventListener('mouseenter', () => {
        hoveredBlock = block;
      });
      block.addEventListener('mouseleave', () => {
        hoveredBlock = null;
      });
    });

    // Listen for Ctrl+L
    document.addEventListener('keydown', e => {
      if (e.ctrlKey && (e.key === 'l' || e.key === 'L')) {
        if (hoveredBlock) {
          let modPath = hoveredBlock.dataset.modpath || "Unknown path";

          // Create tooltip
          const tooltip = document.createElement('div');
          tooltip.className = "module-tooltip";
          tooltip.textContent = "Module: " + modPath;

          // Basic styling
          tooltip.style.position = "absolute";
          tooltip.style.background = "#3d3d3d";
          tooltip.style.border = "1px solid #6d6d6d";
          tooltip.style.padding = "4px 8px";
          tooltip.style.zIndex = 9999;
          tooltip.style.fontSize = "14px";

          // Place it near bottom-left of the hovered block
          const rect = hoveredBlock.getBoundingClientRect();
          tooltip.style.left = (rect.left + window.pageXOffset) + "px";
          tooltip.style.top = (rect.bottom + window.pageYOffset) + "px";

          document.body.appendChild(tooltip);

          // Attempt to copy to clipboard
          navigator.clipboard.writeText(modPath).then(() => {
            console.log("Copied module path: " + modPath);
          }).catch(err => {
            console.error("Clipboard copy error:", err);
          });

          // Remove tooltip after 3 seconds
          setTimeout(() => {
            if (tooltip.parentNode) {
              tooltip.parentNode.removeChild(tooltip);
              hoveredBlock = null;
            }
          }, 3000);

          // Prevent default browser Ctrl+L
          e.preventDefault();
        }
      }
    });
}


moduleHoverFunc();
"""



def javascript(source: str) -> None:
    """
    Injects a string of javascript code into the page and executes it. It must only call one function, otherwise some buggy stuff happens where nothing happens. 
    For reference, see the zoom_js_code and how the whole code is wrapped in a single function.
    """
    div_id = uuid.uuid4()

    st.markdown(f"""
    <div style="display:none" id="{div_id}">
        <iframe src="javascript: \
            var script = document.createElement('script'); \
            script.type = 'text/javascript'; \
            script.text = {html_lib.escape(repr(source))}; \
            var div = window.parent.document.getElementById('{div_id}'); \
            div.appendChild(script); \
            div.parentElement.parentElement.parentElement.style.display = 'none'; \
        "/>
    </div>
    """, unsafe_allow_html=True)


class StreamTeX_ToC:
    def __init__(self, toc_list: list = [], numerate_title:bool = True, toc_bck_index = -1):
        # TODO: point style like google docs
        self.toc_list = toc_list
        self.numerate_title = numerate_title
        '''A boolean dictating whether to add numering in the ToC titles.'''
        self.current_level = 1
        '''The starting level of the ToC. It is used to keep track of the ToC during generation.'''
        self.numbers = []
        '''List to keep track of title numbers.'''


        self.toc_bck_index = toc_bck_index
        '''The position of the ToC in the list of blocks. 0 means at the start, -1 at the end, and None means to not include it in the web book.'''
        self.toc_title_style = s.text.titles.title
        '''A Style object dictating how the ToC main title should look.'''
        self.toc_content_style = s.text.titles.subtitle
        '''A Style object dictating how the ToC content (the listing of titles) should look.'''

    
    def add_section(self, level: str, title: str):
        """level can be '+x' or '-x' for relative TOC levels, or just 'x' for absolute TOC levels."""

        if level.startswith("+") or level.startswith("-"):
            lvl = self.current_level + int(level)
            lvl = max(lvl, 1)
        else:
            lvl = int(level)
            lvl = max(lvl, 1)
            self.current_level = lvl

         # Update section numbering
        while len(self.numbers) < lvl:
            self.numbers.append(0)  # Extend numbering hierarchy
        self.numbers = self.numbers[:lvl]  # Trim unused levels
        self.numbers[-1] += 1  # Increment the current level number

        # Reset numbering for subsequent levels when jumping back in hierarchy
        if len(self.numbers) > lvl:
            self.numbers = self.numbers[:lvl]

        # Generate numbering if numeration is enabled
        section_number = ".".join(map(str, self.numbers)) + " "

        # Add to the ToC list
        toc_entry = {
            "level": lvl,
            "title": section_number + title if self.numerate_title else title,
            "key_anchor": self.get_key_anchor(section_number + title),
        }
        self.toc_list.append(toc_entry)
        
        if not self.numerate_title:
            section_number = ""

        return toc_entry["key_anchor"], section_number
    
    def generate(self, indent_char="&nbsp;"):
        '''Generates the ToC html code.'''
        toc_string = ""
        for entry in self.toc_list:
            indentation = indent_char * 4 * (entry["level"] - 1)
            # OLD AF - st.sidebar.markdown(f'<span style="overflow: hidden; text-overflow: ellipsis; text-wrap: nowrap; word-wrap: normal;">{indentation}<a href="#{entry['key_anchor']}">{entry['title']}</a></span>', unsafe_allow_html=True)
            st.sidebar.markdown(
                f"<span style=\"overflow: hidden; text-overflow: ellipsis; text-wrap: nowrap; word-wrap: normal;\">"
                f"{indentation}<a href=\"#{entry['key_anchor']}\">{entry['title']}</a></span>",
                unsafe_allow_html=True
            )
        return toc_string
    
    @staticmethod
    def get_key_anchor(title: str):
        return title.replace('.', '-').replace(' ', '-').lower()
        

class TOC:
    """
    A class wrapper of a ToC level.
    lvl can be '+x' or '-x' for relative TOC levels, or just 'x' for absolute TOC levels."""
    def __init__(self, lvl: str):
        self.lvl = lvl
        """lvl can be '+x' or '-x' for relative TOC levels, or just 'x' for absolute TOC levels."""
    
    def tag(self, label: str) -> tuple:
        key_anchor, numbering = toc.add_section(self.lvl, label)
        return (f"<div id='{key_anchor}'>", f"</div>", numbering)


def st_show_toc(indent_char="&nbsp;&nbsp;&nbsp;"):
    '''Returns the html representing the ToC in the web book.'''
    toc_string = st_write(toc.toc_title_style,
                           "Table of Content", tag=Tags.div, toc_lvl=TOC('+1')) + st_space("v",4)
    for entry in toc.toc_list:
        indentation = indent_char * 2 * (entry["level"] - 1)
        toc_string += st_write(toc.toc_content_style, txt=f"{indentation}{entry['title']}",
                                link=f"#{entry['key_anchor']}", hover=False, no_link_decor=True) + st_br()
    return toc_string              

toc: StreamTeX_ToC = StreamTeX_ToC([], False, -1)
'''The global ToC object used by st_book when generating the ToC.'''



def st_book(module_list,  *args, **kwargs):
    """Generates a web page e-book from a list of block (html or panel) modules."""
    start_time = time.time()
    print("Starting st_book function...")

    # Load default CSS styles
    try:
        with resources.open_text('streamtex.static', 'default.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        current_dir = os.path.dirname(__file__)
        static_dir = os.path.join(current_dir, 'static')
        css_file_path = os.path.join(static_dir, 'default.css')
        # Read the CSS file
        with open(css_file_path, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # 2) Insert the Zoom <select> at the top of the sidebar
    #    This doesn't do any scaling itself, but it's an anchor for the JS to attach to.
    st.sidebar.markdown("""
    <div style="margin: 10px 0;">
      <label for="zoomSelect" style="display: block; font-weight: bold; margin-bottom: 6px;">
        Zoom Level:
      </label>
      <select id="zoomSelect" style="width: 100%; padding: 6px;">
        <option value="10">10%</option>
        <option value="25">25%</option>
        <option value="50">50%</option>
        <option value="75">75%</option>
        <option value="90">90%</option>
        <option value="100" selected>100%</option>
        <option value="125">125%</option>
        <option value="150">150%</option>
        <option value="175">175%</option>
        <option value="200">200%</option>
      </select>
    </div>
    """, unsafe_allow_html=True)

    yes_toc =  toc.toc_bck_index != None
    panel_list = []


    if yes_toc and (toc.toc_bck_index < 0 or toc.toc_bck_index >= len(module_list)):
        toc.toc_bck_index = len(module_list)


    for i in range(len(module_list)):
        block_code_module = module_list[i]

        if yes_toc and i == toc.toc_bck_index:
            panel_list.append(
                st_write(toc.toc_title_style,
                           "Table of Content", tag=Tags.div, toc_lvl=TOC('1')) + st_space("v",4))

        if block_code_module is None:
            panel_list.append(None)
            continue

        
        
        if hasattr(block_code_module, 'build_panel'):
            panel_list.append(block_code_module)  
            continue  

        if hasattr(block_code_module, 'html_block'):
            html_func = getattr(block_code_module, 'html_block')
            html = html_func(*args, **kwargs)

            absolute_path = getattr(block_code_module, '__file__', str(block_code_module))
            module_path = os.path.relpath(absolute_path, start=os.getcwd())
            html = f"<div class='block-container' data-modpath='{module_path}'>{html}</div>"
            panel_list.append(html)
            continue
    
    if toc.toc_bck_index == len(module_list):
        panel_list.append(
                st_write(toc.toc_title_style,
                           "Table of Content", tag=Tags.div, toc_lvl=TOC('1')) + st_space("v",4))
    
    for i, panel in enumerate(panel_list):
        if panel == None:
            pass

        if yes_toc and i == toc.toc_bck_index:
            indent_char="&nbsp;"
            html = panel
            for entry in toc.toc_list:
                indentation = indent_char * 6 * (entry["level"] - 1)
                html += st_write(toc.toc_content_style, txt=f"{indentation}{entry['title']}",
                                        link=f"#{entry['key_anchor']}", hover=False, no_link_decor=True) + st_br()  
            st_show(html) 
        elif type(panel) == str:
            st_show(panel)
        else:
            absolute_path = getattr(panel, '__file__', str(panel))
            module_path = os.path.relpath(absolute_path, start=os.getcwd())
            st.markdown(
                f"<div class='block-container' data-modpath='{module_path}'>",
                unsafe_allow_html=True
)
            panel = panel.build_panel(*args, **kwargs)
            panel()
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f'<div style="padding-top: 70px;"></div>', unsafe_allow_html=True)
    
    toc.generate()

    toc.toc_list = []
    toc.current_level = 1
    toc.numbers = []

    

    javascript(js_code)
    javascript(zoom_js_code)
    javascript(module_hover_js())

    end_time = time.time()
    duration = end_time - start_time
    print(f"st_book function completed in {duration:.2f} seconds.")




def __parse_html_toc(html: str, current_toc_list: list):
    """parses the html for <div class='toc{self.lvl}_{label}'> and returns a list of lists
      representing the toc, creating parent lists to accomodate jumps from 0 to.
      current_toc_list is of the form [[toc_title, ]]
      This function should return a list of all {self.lvl}_{label} pairs found in the order they appear."""

    def adjust_level(level, current_level, numbering):
        """Adjusts the numbering based on the new level."""
        if level > len(numbering):
            # Add zeros for skipped levels
            while len(numbering) < level - 1:
                numbering.append(0)
        elif level <= len(numbering):
            # Truncate numbering to the new level - 1
            numbering = numbering[:level - 1]
        return numbering

    def update_numbering(level, numbering):
        """Updates the numbering for the current level."""
        # Ensure numbering has the correct length
        while len(numbering) < level - 1:
            numbering.append(0)
        if len(numbering) == level - 1:
            numbering.append(1)
        else:
            numbering[-1] += 1
        return numbering

    # Initialize the TOC state
    toc = current_toc_list if current_toc_list else []
    numbering = []  # Keeps track of the current numbering (e.g., [1, 1, 2])
    stack = []  # Stack to manage current TOC hierarchy
    current_list = toc  # Current list to append items
    current_level = 1  # Initial level is 1

    # Regular expression to match TOC entries
    pattern = r"toc([+-]?\d+)_([\s\S]+)"

    # Find all matches for <div class='toc{lvl}_{label}'>
    matches = re.finditer(r"<div id='([^']+)'>", html)

    for match in matches:
        class_attr = match.group(1)
        toc_match = re.match(pattern, class_attr)
        if toc_match:
            lvl_str, label = toc_match.groups()
            # Determine the new level
            if lvl_str.startswith("+") or lvl_str.startswith("-"):
                new_level = current_level + int(lvl_str)
            else:
                new_level = int(lvl_str)

            # Ensure levels are valid
            if new_level < 1:
                new_level = 1

            # Adjust the numbering
            numbering = adjust_level(new_level, current_level, numbering)
            numbering = update_numbering(new_level, numbering)

            # Convert numbering to a string (e.g., '1.1.2')
            numbering_str = ".".join(map(str, numbering))

            # Add the entry to the current list
            entry = (numbering_str, label)
            current_list.append(entry)

            # Prepare for potential sub-entries
            new_sublist = []
            current_list.append(new_sublist)

            # Update the stack and state
            stack.append((current_level, numbering.copy(), current_list))
            current_level = new_level
            current_list = new_sublist

    # Handle closing div tags by popping the stack
    for tag in re.finditer(r"</div>", html):
        if stack:
            stack.pop()
            if stack:
                current_level, numbering, current_list = stack[-1]
            else:
                current_level = 1
                numbering = []
                current_list = toc

    return toc


import base64

### ------------------------------ NEW FUNCTIONS ------------------------------ ###

def __img_data(bc_file_name, folder: str):
     # Build the path to the image
     
    image_path = os.path.join(folder, bc_file_name)
    
    # Open the image file and read its contents
    with open(image_path, "rb") as file_:
        contents = file_.read()
    
    # Encode the image in base64
    return base64.b64encode(contents).decode("utf-8")

def __get_base64_encoded_image(file_path: str):
    """Converts an image to a base64 encoded string."""
    try:
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def __is_url(path: str):
    """Checks if the given path is a URL."""
    return path.startswith(("http://", "https://", "www."))

def __is_absolute_path(path: str):
    """Checks if the given path is an absolute path."""
    return os.path.isabs(path)

def __is_relative_path(path: str):
    """Checks if the given path is a relative path."""
    return path.startswith((".", "..", "/", "\\"))

def __get_mime_type(file_path: str):
    """Determine the MIME type based on the file extension."""
    extension = file_path.lower().split('.')[-1]
    if extension == "png":
        return "image/png"
    elif extension in ["jpg", "jpeg"]:
        return "image/jpeg"
    elif extension == "gif":
        return "image/gif"
    else:
        return None  # Unsupported format or no extension

import requests
from bs4 import BeautifulSoup as bs

def __get_page_preview(url: str):
    """
    Fetches the page title and favicon URL for the given link.
    If the connection is refused or times out, returns 'Could not fetch page' and None,
    preventing display of any preview.
    """
    title = url
    favicon = 'https://www.google.com/s2/favicons?domain_url=' + url
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = bs(response.content, 'html.parser')

        # Get the page title
        title = soup.title.string.strip() if soup.title else 'No title found'

        # Get the favicon
        favicon = None
        icon_link = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
        if icon_link and icon_link.get('href'):
            favicon = icon_link['href']
            if favicon.startswith('//'):
                favicon = 'http:' + favicon
            elif favicon.startswith('/'):
                from urllib.parse import urljoin
                favicon = urljoin(url, favicon)
        else:
            # Default favicon if not found
            favicon = 'https://www.google.com/s2/favicons?domain_url=' + url

        return title, favicon, True
    
    except (ConnectionError, Timeout):
        # Specifically handle connection refusal or timeout
        return title, favicon, False

    except Exception as e:
        return 'Could not fetch page', None, False

 
def st_show(html = ""):
    st.markdown(html, True)


def st_block(style: Style = StreamTeX_Styles.none, block_list: list = [], tag: Tag = Tags.div) -> str:
    """Encapsulates HTML markup (block_list) within a styled div."""
    return f'<{tag} style="{style}">{"".join(block_list)}</{tag}>' 


def st_table(rows: int = 0, cols: int = 0,
             table_style: Style = StreamTeX_Styles.none, row_styles: Union[List[Style], Style, StyleGrid] = StreamTeX_Styles.none,
             cell_styles: Union[List[List[Style]], List[Style], Style, StyleGrid] = StreamTeX_Styles.none,
             block_list: Union[List[str], List[List[str]]] = []) -> str:
    """
    Generates an HTML table with customizable styles for the table, rows, and cells.

    :param rows: Number of rows in the table. If 0, inferred from `block_list`.
    :param cols: Number of columns in the table. If 0, inferred from `block_list`.
    :param table_style: A `Style` object applied to the entire table. Defaults to `StreamTeX_Styles.none`.
    :param row_styles: Styles for rows. Can be:
        - A `StyleGrid` object.
        - A list of `Style` objects (one per row).
        - A single `Style` applied to all rows.
    :param cell_styles: Styles for individual cells. Can be:
        - A `StyleGrid` object.
        - A matrix (list of lists) of `Style` objects.
        - A flat list of `Style` objects.
        - A single `Style` applied to all cells.
    :param block_list: Content for the table cells. Can be:
        - A matrix (list of lists) if `rows` or `cols` is 0.
        - A flat list if `rows` and `cols` are provided.
    :return: A string containing the styled HTML for the table.

    Notes:
    - If `rows` and `cols` are not provided, the function treats `block_list` as a matrix and infers dimensions.
    - Missing content in `block_list`, `row_styles`, or `cell_styles` is filled with defaults (`''` for content, `StreamTeX_Styles.none` for styles).
    - Handles `StyleGrid` objects for modular, hierarchical styling.
    """

    # Check if rows or columns were specified (so we expect block_list and cell_styles to be matrices)
    if rows <= 0 or cols <= 0:
        # block_list must be a matrix (list of lists)
        rows = len(block_list)
        cols = max(len(row) for row in block_list) if block_list else 0

        # Ensure all rows in block_list have the same number of columns
        for row in block_list:
            row.extend([''] * (cols - len(row)))  # Fill shorter rows with empty strings

        # Flatten the block_list matrix
        block_list_flat = [block for block_row in block_list for block in block_row]
    else:
        # rows and cols are provided, block_list is expected to be flat
        block_list_flat = block_list

    total_cells = rows * cols

    # Process row_styles
    if isinstance(row_styles, Style):
        # Single Style applied to all rows
        row_styles_list = [row_styles] * rows

    elif isinstance(row_styles, StyleGrid):
        # Extract the css_grid from StyleGrid
        style_grid = row_styles.css_grid

        # Initialize row_styles_list with StreamTeX_Styles.none
        row_styles_list = [StreamTeX_Styles.none] * rows

        # Apply styles from the style_grid to row_styles_list
        for i in range(rows):
            if i < len(style_grid) and len(style_grid[i]) > 0:
                # Take the first style in the row
                row_styles_list[i] = style_grid[i][0]
            else:
                # Keep existing style (StreamTeX_Styles.none)
                pass

    elif isinstance(row_styles, list):
        # row_styles is a list
        row_styles_list = row_styles

        # Extend or trim row_styles_list to match rows
        if len(row_styles_list) < rows:
            row_styles_list.extend([StreamTeX_Styles.none] * (rows - len(row_styles_list)))
        else:
            row_styles_list = row_styles_list[:rows]
    else:
        # Unknown type, default to StreamTeX_Styles.none
        row_styles_list = [StreamTeX_Styles.none] * rows

    # Process cell_styles
    if isinstance(cell_styles, Style):
        # Single Style applied to all cells
        cell_styles_flat = [cell_styles] * total_cells

    elif isinstance(cell_styles, StyleGrid):
        # Extract the css_grid from StyleGrid
        style_grid = cell_styles.css_grid

        # Initialize cell_styles_flat with StreamTeX_Styles.none
        cell_styles_flat = [StreamTeX_Styles.none] * total_cells

        # Apply styles from the style_grid to cell_styles_flat
        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                if i < len(style_grid) and j < len(style_grid[i]):
                    cell_style = style_grid[i][j]
                    cell_styles_flat[index] = cell_style
                else:
                    # Keep existing style (StreamTeX_Styles.none)
                    pass

    elif isinstance(cell_styles, list):
        if all(isinstance(row, list) for row in cell_styles):
            # cell_styles is a matrix (list of lists)
            # Flatten the cell_styles matrix
            cell_styles_flat = [style for style_row in cell_styles for style in style_row]
        else:
            # cell_styles is a flat list
            cell_styles_flat = cell_styles

        # Extend or trim cell_styles_flat to match total_cells
        if len(cell_styles_flat) < total_cells:
            cell_styles_flat.extend([StreamTeX_Styles.none] * (total_cells - len(cell_styles_flat)))
        else:
            cell_styles_flat = cell_styles_flat[:total_cells]
    else:
        # Unknown type, default to StreamTeX_Styles.none
        cell_styles_flat = [StreamTeX_Styles.none] * total_cells

    # Ensure block_list_flat has length total_cells
    if len(block_list_flat) < total_cells:
        block_list_flat.extend([''] * (total_cells - len(block_list_flat)))
    else:
        block_list_flat = block_list_flat[:total_cells]

    # Begin building the table HTML
    markdown = f'<table style="{table_style.css}">'
    for y in range(rows):
        row_style = row_styles_list[y].css if y < len(row_styles_list) else ''
        markdown += f'<tr style="{row_style}">'
        for x in range(cols):
            index = y * cols + x
            cell_content = block_list_flat[index]
            cell_style = cell_styles_flat[index].css if index < len(cell_styles_flat) else ''
            markdown += f'<td style="{cell_style}">{cell_content}</td>'
        markdown += '</tr>'
    markdown += '</table>'
    return markdown


def st_grid(rows: int = 0, cols: int = 0,
            grid_style: Style = StreamTeX_Styles.none, cell_styles: Union[List[List[Style]], List[Style], Style, StyleGrid] = StreamTeX_Styles.none,
            block_list: Union[List[str], List[List[str]]] = []) -> str:
    """
    Generates an HTML grid layout with customizable styles for the grid and individual cells.

    :param rows: Number of rows in the grid. If 0, inferred from `block_list`.
    :param cols: Number of columns in the grid. If 0, inferred from `block_list`.
    :param grid_style: A `Style` object applied to the entire grid. Defaults to `StreamTeX_Styles.none`.
    :param cell_styles: Styles for individual cells. Can be:
        - A `StyleGrid` object.
        - A matrix (list of lists) of `Style` objects.
        - A flat list of `Style` objects.
        - A single `Style` applied to all cells.
    :param block_list: Content for the grid cells. Can be:
        - A matrix (list of lists) of strings if `rows` or `cols` is 0.
        - A flat list of strings if `rows` and `cols` are provided.
    :return: A string containing the styled HTML for the grid.

    Notes:
    - If `rows` and `cols` are not provided, the function treats `block_list` as a matrix and infers dimensions.
    - Missing content in `block_list` or `cell_styles` is filled with defaults (`''` for content, `StreamTeX_Styles.none` for styles).
    - Ensures compatibility with various formats for `cell_styles` and dynamically adjusts as needed.
    """

    # Determine rows and columns if not provided (block_list must be a matrix in this case)
    if rows <= 0 or cols <= 0:
        # block_list must be a matrix (list of lists)
        rows = len(block_list)
        cols = max(len(row) for row in block_list) if block_list else 0

        # Ensure all rows in block_list have the same number of columns
        for row in block_list:
            row.extend([''] * (cols - len(row)))  # Fill shorter rows with empty strings

        # Flatten the block_list matrix
        block_list_flat = [block for block_row in block_list for block in block_row]
    else:
        # rows and cols are provided, block_list is expected to be flat
        block_list_flat = block_list

    total_cells = rows * cols

    # Process cell_styles
    if isinstance(cell_styles, Style):
        # Single Style applied to all cells
        cell_styles_flat = [cell_styles] * total_cells

    elif isinstance(cell_styles, StyleGrid):
        # Extract the css_grid from StyleGrid
        style_grid = cell_styles.css_grid

        # Initialize cell_styles_flat with StreamTeX_Styles.none
        cell_styles_flat = [StreamTeX_Styles.none] * total_cells

        # Apply styles from the style_grid to cell_styles_flat
        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                if i < len(style_grid) and j < len(style_grid[i]):
                    cell_style = style_grid[i][j]
                    cell_styles_flat[index] = cell_style
                else:
                    # If the style_grid doesn't have this cell, keep the existing style (StreamTeX_Styles.none)
                    pass

    elif isinstance(cell_styles, list):
        # cell_styles is a list
        if all(isinstance(row, list) for row in cell_styles):
            # cell_styles is a matrix (list of lists)
            # Flatten the cell_styles matrix
            cell_styles_flat = [style for style_row in cell_styles for style in style_row]
        else:
            # cell_styles is a flat list
            cell_styles_flat = cell_styles

        # Extend or trim cell_styles_flat to match total_cells
        if len(cell_styles_flat) < total_cells:
            cell_styles_flat.extend([StreamTeX_Styles.none] * (total_cells - len(cell_styles_flat)))
        else:
            cell_styles_flat = cell_styles_flat[:total_cells]
    else:
        # Unknown type, default to StreamTeX_Styles.none
        cell_styles_flat = [StreamTeX_Styles.none] * total_cells

    # Ensure block_list_flat has length total_cells
    if len(block_list_flat) < total_cells:
        block_list_flat.extend([''] * (total_cells - len(block_list_flat)))
    else:
        block_list_flat = block_list_flat[:total_cells]

    # Begin building the grid HTML
    combined_grid_style = f"{grid_style.css} display: grid; grid-template-columns: repeat({cols}, 1fr); "

    markdown = f'<div style="{combined_grid_style}">'
    
    # Loop through each cell to generate HTML with individual styles
    for i in range(total_cells):
        cell_content = block_list_flat[i]
        cell_style = cell_styles_flat[i].css if isinstance(cell_styles_flat[i], Style) else ''
        markdown += f'<div style="{cell_style}">{cell_content}</div>'
    
    # Close the grid container
    markdown += '</div>'
    return markdown


def st_list(list_type: ListType = ListTypes.unordered, l_style: Style = StreamTeX_Styles.none, li_style: Style = StreamTeX_Styles.none, block_list: list = [], level=1, stickToText=True) -> str:
    """
    Generates an HTML list (ordered or unordered) with optional styles and support for nested lists.

    :param list_type: The type of list, either ordered (`<ol>`) or unordered (`<ul>`). Defaults to unordered.
    :param l_style: A `Style` object for the entire list. Supports custom list-level styles for `ListStyle`.
    :param li_style: A `Style` object for individual list items. Defaults to `StreamTeX_Styles.none`.
    :param block_list: A list of items to include in the list. Items can be strings or nested lists.
    :param level: The nesting level of the list (used for applying hierarchical styles). Defaults to 1.
    :param stickToText: If True, centers the list and aligns it inline. Defaults to True.
    :return: A string containing the styled HTML list.

    Notes:
    - Supports nested lists recursively, with the nesting level affecting the style if `l_style` is a `ListStyle`.
    - Centers the list in a container if `stickToText` is True.
    """
    
    # Start the list with the specified style
    list_style = l_style.lvl(level) + l_style if isinstance(l_style, ListStyle) else l_style

    inside_style = "list-style-position: inside; padding-left: 0;" if (stickToText and len(block_list) != 1) else ""
    list_html = f'<{list_type} style="{list_style} display: inline-block; text-align: left; {inside_style}">'

    
    # Iterate over the markdown items and wrap each in <li> tags
    for i, item in enumerate(block_list):
        if isinstance(item, list):
            # Nested list
            list_html += st_list(list_type, l_style, li_style, item, level + 1)
        else:
            list_html += f'{"" if i==0  else "</li>"}<li style="{li_style} ">{item}'
    
    # Close the list
    list_html += f'</li></{list_type}>'

    
    return list_html


def contain_link(html="", link="", no_link_decor=False, hover=True):
    """
    Wraps the given HTML content in an anchor tag, optionally adding a hover preview box.

    :param html: The HTML content to be wrapped in the anchor tag.
    :param link: The hyperlink to associate with the content. If empty, the function returns the original HTML.
    :param no_link_decor: If True, removes text decoration (like underline) from the link. Defaults to False.
    :param hover: If True, includes a hover preview box showing the page title and favicon. Defaults to True.
    :return: A string containing the original HTML wrapped in an anchor tag with optional hover content.

    Notes:
    - If `hover` is enabled, the function fetches a page preview using `get_page_preview` to display additional details.
    - If the page preview is unavailable, it falls back to displaying the link URL.
    """
    if not link:
        return html
    
    else:
        copy_link = link[:]
        if copy_link.strip().startswith("#"):
            # Internal link, no hover preview
            hover = False
            link =  "#" + StreamTeX_ToC.get_key_anchor(link.strip()[1:])
        hover_content = ''
        data_preview = ""
        if hover:
            # Fetch the page title and icon using `get_page_preview`.
            # This provides contextual information about the link on hover.
            page_title, favicon_url, success = __get_page_preview(link)

            # Check if the page preview was successfully fetched. Fallback to the link if unsuccessful.
            fallback = page_title != 'Could not fetch page' 
            preview_title = page_title if fallback else link
            preview_favicon = favicon_url or 'https://www.google.com/s2/favicons?domain_url=' + link

            hover_content = f"""
            <div class="hide-hover-box">
                <img src="{favicon_url}" alt="favicon" style="vertical-align: middle; margin-right: 8px; width: 16px; height: 16px;">
                
                {f'<embed src="{link}" style="width:300px; height: 300px;">' if success else ''}
            </div>"""

            data_preview = f"""
            <div style="display: flex; align-items: center; margin-bottom: 8px; margin-top: 8px; font-size: 16px; font-weight: bold; color: #2e6ad2; width:300px; max-height: 300px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                <img src="{preview_favicon}" style="width:24px; height:24px; margin-right:16px;">
                <span style="width: 300px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;"><a href="{link}" style="font-weight: bold; color: #2e6ad2; text-decoration: none;">{preview_title}</a></span>
            </div>
            """

            if success:
                data_preview += f'<embed src="{link}" style="width:300px; max-height: 300px;">'
            data_preview = data_preview.strip()

        link_style = "text-decoration: none;" if no_link_decor else ""
        data_preview_escaped = html_lib.escape(data_preview)
        
        # Wrap the original HTML content in an anchor tag, optionally disabling the link decorations (underline).
        # The hover box is embedded within the anchor tag.
        # OLD AF - html = f'<a style="{'text-decoration: none;' if no_link_decor else ''} position: relative;" href="{link}">{html}</a>'
        # html = f"<a style=\"{'text-decoration: none;' if no_link_decor else ''} position: relative;\" href=\"{link}\">{html}</a>"
        html = f'<a href="{link}" style="{link_style}position:relative;" data-preview="{data_preview_escaped}">{html}</a>'
    return html

def strip_html(html_string):
    """
    Remove all HTML tags from a string and return plain text.
    
    :param html_string: The string containing HTML content.
    :return: A plain text string with HTML tags removed.
    """
    # Define a regex pattern to match HTML tags
    html_tag_pattern = re.compile(r'<.*?>')
    # Use re.sub to replace HTML tags with an empty string
    plain_text = re.sub(html_tag_pattern, '', html_string)
    return plain_text

def st_write(style: Style = StreamTeX_Styles.none, txt:str='', tag: Tag = Tags.span, link="", no_link_decor=False, hover=True, toc_lvl: TOC = None, label: str = "" ) -> str:
    """
    Function to write a styled string with optional link reference and table of content entry.

    :param style: A Style object representing the CSS to apply to the text. Defaults to `StreamTeX_Styles.none`.
    :param txt: The text or HTML content to wrap in the specified tag.
    :param tag: The HTML tag to use for wrapping the content (e.g., <span>, <div>). Defaults to `Tags.span`.
    :param link: An optional hyperlink to wrap around the content. If provided, the text will be clickable.
    :param no_link_decor: If True, removes text decoration (like underline) for links. Defaults to False.
    :param hover: If True, includes hover functionality to display additional information (e.g., link previews).
    :param toc_lvl: A TOC object to include TOC-specific tags. This allows the text to be part of a hierarchical TOC.
    :param label: An optional label to use for the TOC entry. If not provided, a truncated version of `txt` is used.
    :return: A string of HTML representing the styled and linked content.

    Notes:
    - If `toc_lvl` is provided, the function wraps the content in tags to associate it with the specified TOC level.
    - Labels for TOC are automatically generated by truncating the text to a predefined length if no label is given.
    - The function uses `contain_link` to handle optional hyperlinking and link decorations.
    """
        
    if toc_lvl:
        # If no label is provided, generate a truncated label from the text. This ensures TOC entries are descriptive
        # but not overly long, avoiding clutter in the TOC.
        if not label:
            label_length = 73
            txt_no_html = strip_html(txt)  # Remove HTML tags to generate a clean label
            label = (txt_no_html[:label_length] + '..') if len(txt_no_html) > label_length else txt_no_html

        # Generate the opening and closing TOC tags for the specified level and label.
        toc_tag = toc_lvl.tag(label)
        txt = toc_tag[2] + txt # Prepend the numbering of the ToC title



    # Wrap the text in the specified tag with the given style. This ensures consistent styling.   
    txt_tag = f'<{tag} style="{style}">{txt}</{tag}>'
    # Handle optional hyperlinking and hover effects.
    txt_tag = contain_link(txt_tag, link, no_link_decor, hover)

    if toc_lvl:
        # Wrap the final output in TOC tags if a TOC level is specified. This associates the content with the TOC.
        txt_tag = toc_tag[0] + txt_tag + toc_tag[1]
    elif label:
        key_anchor = StreamTeX_ToC.get_key_anchor(label)
        txt_tag = f"<div id='{key_anchor}'>{txt_tag}</div>"

    return txt_tag


def st_image(style: Style = StreamTeX_Styles.none,  width="100%", height="100%", uri: str="", alt="", link="", hover=True):
    """
    Generates an HTML `img` tag based on the image URI, with optional styles, link wrapping, and hover effects.

    :param style: A `Style` object defining CSS styles to apply to the image. Defaults to `StreamTeX_Styles.none`.
    :param width: The width of the image. Can be a string (e.g., "50%") or an integer (e.g., 100). Defaults to "100%".
    :param height: The height of the image. Can be a string (e.g., "300px") or an integer (e.g., 300). Defaults to "100%".
    :param uri: The image URI. Can be:
        - A URL (e.g., "https://example.com/image.png").
        - An absolute path (e.g., "C:User/images/image.png").
        - A relative path (e.g., "/images/image.png". This can start with '.', '..', '/' and backslash).
        - A static path (e.g., images/image.png).
    :param alt: The alternative text for the image, used for accessibility or when the image cannot be displayed.
    :param link: An optional hyperlink to wrap around the image. Defaults to an empty string (no link).
    :param hover: If True, enables hover functionality for the image link. Defaults to True.
    :return: A string containing the HTML `img` tag, optionally wrapped in a hyperlink.

    Notes:
    - URLs are used directly as the `src` attribute.
    - Local files are base64 encoded for compatibility with browsers that don't allow local file paths in HTML.
    - If the URI cannot be resolved or is unsupported, the `src` attribute is left empty.
    - The function wraps the image tag in a link if `link` is provided, using the `contain_link` function.
    """
    # Convert integer size to pixel-based string
    if type(width) is int:
        width = str(width) + "px"
    if type(height) is int:
        height = str(height) + "px"

    width_attr = f' width="{width}"'
    height_attr = f' height="{height}"'

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

    img_tag = f'<img src="{img_src}" {width_attr} {height_attr} style="{style}" alt="{alt}"/>'
    
    
    img_tag = contain_link(img_tag, link, False, hover)
    
    return img_tag


def st_overlay(background:str, contents: List[str], positions: List[Style]):
    """Shortcut for overlaying a background block with some contents using the specified positions. 
    This encapsulates both the backgrond and contents (these becoming relative) within one absolute posiitoned div. 
    """
    positioned_contents = [st_block(positions[i] + s.container.positions.absolute, contents[i]) for i in range(min(len(contents), len(positions)))]

    return st_block(s.container.positions.relative + s.center_txt,
                    [background]+positioned_contents)


def st_space(direction: Literal["v", "h"] = "v", size="1em") -> str:
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

    # Return appropriate HTML based on orientation
    if direction == "v":
        # Vertical space with padding-top
        space_tag = f"""<div style="padding-top: {size};"></div>"""
    else:
        # Horizontal space with padding-left
        space_tag = f"""<span style="padding-left: {size};"></span>"""
    return space_tag

def st_br():
   
   return st_space("v", 0)

def st_include(block_file_module, *args, **kwargs) -> str:

    if not block_file_module:
        return f":red-background[File {block_file_module.__path__} not found]"

    if not hasattr(block_file_module, 'html_block'):
        return f":red-background[The file {block_file_module.__path__} does not contain a html_block() function.]"

        
    html_func = getattr(block_file_module, 'html_block')
    html = html_func(*args, **kwargs)

    return html

def st_iframe(url: str, width="100%", height="800px") -> str:
    
    ### TODO Check if the url is a google sheet published url or otherwise

    html_code = f"""
    <iframe src="{url}" width="{width}" height="{height}" frameborder="0"></iframe>
    """
    return html_code








import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
def st_sheet(
    google_sheet_url: str,
    service_account_file: str,
    sheet_range: Optional[str] = None,
    style_grid: Optional[StyleGrid] = None,
    fetch_styles: bool = True,
    override_styles: bool = False
) -> str:
    """
    Fetches data and styles from a Google Sheet and returns HTML markdown to display the contents.
    Allows adding or overriding styles with user-provided styles and toggling style inclusion.

    :param google_sheet_url: URL of the Google Sheet.
    :param service_account_file: Path to the service account JSON key file.
    :param sheet_range: Optional range in A1 notation (e.g., 'Sheet1!A1:E10'). If None, fetches the entire first sheet.
    :param style_grid: Optional StyleGrid to add to or override fetched styles.
    :param fetch_styles: If True, includes the fetched styles in the output. If False, no styles are  fetched. User styles may still be applied.
    :param override_styles: If True, user-defined styles override fetched styles. If False, user-defined styles are added to fetched styles.
    :return: HTML string representing the styled table.
    """
     # Extract the Spreadsheet ID from the URL
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', google_sheet_url)
    if not match:
        raise ValueError("Invalid Google Sheets URL")
    spreadsheet_id = match.group(1)

    # Set up the Sheets API
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)

    # Get the sheet names
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = sheet_metadata.get('sheets', '')
    sheet_names = [s['properties']['title'] for s in sheets]

    # Use the first sheet if no range is provided
    if not sheet_range:
        sheet_name = sheet_names[0]
        sheet_range = f"{sheet_name}"

    # Fetch the sheet data including cell formatting
    result = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        ranges=sheet_range,
        includeGridData=True
    ).execute()

    # Process the data to build the block_list and cell_styles
    block_list = []
    cell_styles = []
    max_cols = 0

    # Get the data for the specified range
    sheet_data = result['sheets'][0]['data'][0]
    rows = sheet_data.get('rowData', [])

    for row_data in rows:
        row_values = []
        row_styles = []
        values = row_data.get('values', [])
        col_index = 0
        for cell in values:
            # Get the cell value
            cell_value = cell.get('formattedValue', '')
            row_values.append(cell_value)

            # Initialize cell style
            cell_style_str = ''

            if fetch_styles:
                # Get the cell formatting
                cell_format = cell.get('effectiveFormat', {})

                # Background color
                if 'backgroundColor' in cell_format:
                    bg_color = cell_format['backgroundColor']
                    red = int(bg_color.get('red', 1) * 255)
                    green = int(bg_color.get('green', 1) * 255)
                    blue = int(bg_color.get('blue', 1) * 255)
                    alpha = bg_color.get('alpha', 1)
                    cell_style_str += f'background-color: rgba({red}, {green}, {blue}, {alpha});'

                # Text format
                text_format = cell_format.get('textFormat', {})
                if text_format.get('bold'):
                    cell_style_str += 'font-weight: bold;'
                if text_format.get('italic'):
                    cell_style_str += 'font-style: italic;'
                if text_format.get('underline'):
                    cell_style_str += 'text-decoration: underline;'
                if 'fontSize' in text_format:
                    font_size = text_format['fontSize']
                    cell_style_str += f'font-size: {font_size}px;'
                if 'foregroundColor' in text_format:
                    fg_color = text_format['foregroundColor']
                    red = int(fg_color.get('red', 0) * 255)
                    green = int(fg_color.get('green', 0) * 255)
                    blue = int(fg_color.get('blue', 0) * 255)
                    alpha = fg_color.get('alpha', 1)
                    cell_style_str += f'color: rgba({red}, {green}, {blue}, {alpha});'

                # Alignment
                horizontal_alignment = cell_format.get('horizontalAlignment', 'left').lower()
                vertical_alignment = cell_format.get('verticalAlignment', 'middle').lower()
                cell_style_str += f'text-align: {horizontal_alignment}; vertical-align: {vertical_alignment};'

                # Wrap strategy
                wrap_strategy = cell_format.get('wrapStrategy', 'OVERFLOW_CELL')
                if wrap_strategy == 'WRAP':
                    cell_style_str += 'white-space: normal;'
                else:
                    cell_style_str += 'white-space: nowrap;'

                # Borders (optional)
                # Add code here if you want to handle borders

            # Create Style object
            cell_style = Style(cell_style_str)
            row_styles.append(cell_style)
            col_index += 1

        block_list.append(row_values)
        cell_styles.append(row_styles)
        max_cols = max(max_cols, col_index)

    # Ensure all rows have the same number of columns
    for row_values, row_styles in zip(block_list, cell_styles):
        if len(row_values) < max_cols:
            row_values.extend([''] * (max_cols - len(row_values)))
            row_styles.extend([StreamTeX_Styles.none] * (max_cols - len(row_styles)))

    # Convert cell_styles to a StyleGrid
    if fetch_styles:
        fetched_style_grid = StyleGrid(css_grid=cell_styles)
    else:
        # If not fetching styles, create a StyleGrid with StreamTeX_Styles.none
        fetched_style_grid = StyleGrid(css_grid=[[StreamTeX_Styles.none for _ in row] for row in block_list])

    # Decide on the combined_style_grid based on fetch_styles and override_styles
    if style_grid:
        if override_styles:
            # Replace fetched styles with user-defined styles where provided
            combined_style_grid = fetched_style_grid * style_grid
        else:
            # Add user-defined styles to fetched styles
            combined_style_grid = fetched_style_grid + style_grid
    else:
        # No user-defined styles, use fetched styles or StreamTeX_Styles.none
        combined_style_grid = fetched_style_grid

    # Generate the HTML using st_table
    html_output = st_table(
        block_list=block_list,
        cell_styles=combined_style_grid
    )

    return html_output
