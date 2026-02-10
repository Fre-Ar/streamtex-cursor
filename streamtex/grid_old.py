import streamlit as st
from typing import List, Union
from contextlib import contextmanager
from .styles import Style, StyleGrid, StreamTeX_Styles
from .utils import generate_key

# Helper type definition for clean signatures
CELL_STYLES_TYPE = Union[List[List[Style]], List[Style], Style, StyleGrid]

class GridController:
    def __init__(self, rows=None, cols=None, cell_styles: CELL_STYLES_TYPE = StreamTeX_Styles.none, auto_width:bool = False, gap=None):
        self.fixed_rows = rows
        self.fixed_cols = cols
        self.cell_styles = cell_styles
        self.gap = gap
        self.auto_width = auto_width
        
        # --- State Tracking ---
        # "Global" counter: tracks how many cells have been created in total.
        # This is essential for mapping a Flat List of styles to Dynamic Rows.
        self.global_cell_counter = 0
        
        # Fixed Mode State
        self.fixed_ptr = 0         # Pointer to the next container in self.containers
        self.containers = []       # Pre-generated containers [(r, c, col), ...]
        
        # Dynamic Mode State
        self.current_row_idx = 0   # Track row index for style lookup
        self.row_cell_idx = 0      # Track cell index within the current row
        self.current_row_cols = [] # Store columns for the current active row

        # --- Pre-Generation (Fixed Mode Only) ---
        if self.fixed_rows is not None and self.fixed_cols is not None:
            for r in range(self.fixed_rows):
                # Create columns for this row immediately
                cols_list = self._create_row_cols(self.fixed_cols, self.auto_width)
                for c, col in enumerate(cols_list):
                    self.containers.append((r, c, col))
    
    def _create_row_cols(self, spec, auto_width: bool):
        """
        Helper to create Streamlit columns and optionally apply 'Auto Width' CSS.
        """
        # 1. Create native columns
        cols_list = st.columns(spec, gap=self.gap)
        
        # 2. Apply Auto-Width CSS if requested
        if auto_width:
            # Generate a unique ID for this specific row
            row_id = generate_key("row")
            
            # Inject a hidden marker into the first column so we can target the parent row
            with cols_list[0]:
                st.html(f'<span class="{row_id}" style="display:none"></span>')
            
            # Inject CSS Targeting the Row (stHorizontalBlock) containing our marker
            # flex: 0 1 auto -> Don't grow (0), allow shrink (1), size based on content (auto)
            css = f"""
            <style>
                /*
                .stHorizontalBlock:has(span.{row_id}) > div[data-testid="column"] {{
                    flex: 0 1 auto !important;
                    width: auto !important;
                    min-width: fit-content !important;
                }}*/
                .stHorizontalBlock:has(.stColumn > .stVerticalBlock > .element-container > .stHtml > span.{row_id}) {{
                    background-color: coral;
                    justify-content: space-between;
                    flex-wrap: nowrap;
                }}
                .stHorizontalBlock:has(.stColumn > .stVerticalBlock > .element-container > .stHtml > span.{row_id}) > .stColumn > .stVerticalBlock > div[data-testid="stLayoutWrapper"] > .stVerticalBlock > .element-container {{
                    background-color: cornflowerblue;
                    width: 100%;
                }}
                .stHorizontalBlock:has(.stColumn > .stVerticalBlock > .element-container > .stHtml > span.{row_id}) > .stColumn {{
                    background-color: olivedrab;
                    width: auto;
                    flex: 1 1 auto;
                }}
            </style>
            """
            st.html(css)
            
        return cols_list
   
    def _resolve_style(self, r: int, c: int) -> Style:
        """
        Determines the style for the current cell (r, c).
        Adapts the logic of flattening/matrix lookup to run Just-In-Time.
        """
        styles = self.cell_styles

        # Case 1: Single Style (Apply to all)
        if isinstance(styles, Style):
            return styles

        # Case 2: StyleGrid (Matrix Lookup with bounds check)
        elif isinstance(styles, StyleGrid):
            style_grid = styles.css_grid
            if r < len(style_grid) and c < len(style_grid[r]):
                return style_grid[r][c]
            else:
                # If the style_grid doesn't have this cell, keep the existing style (StreamTeX_Styles.none)
                return StreamTeX_Styles.none

        # Case 3: List (Flat or Matrix)
        elif isinstance(styles, list):
            if not styles:
                return StreamTeX_Styles.none

            # Check if it is a Matrix (List of Lists)
            is_matrix = all(isinstance(row, list) for row in styles)

            if is_matrix:
                # Matrix Logic: styles[row][col]
                if r < len(styles) and c < len(styles[r]):
                    return styles[r][c]
                else:
                    # If the style_grid doesn't have this cell, keep the existing style (StreamTeX_Styles.none)
                    return StreamTeX_Styles.none
            else:
                # Flat List Logic: styles[global_index]
                # We use the global counter tracking total cells rendered so far
                idx = self.global_cell_counter
                
                if idx < len(styles):
                    return styles[idx]
                else:
                    return StreamTeX_Styles.none

        # Case 4: Fallback
        return StreamTeX_Styles.none
    
    @contextmanager
    def cell(self):
        """
        Yields the next cell container in the grid sequence.
        Applies the specific style from cell_styles[row, col] if available.
        """
        target_container = None
        r, c = 0, 0

        # --- 1. Determine Target Container & Coordinates ---
        if self.containers:
            # FIXED MODE logic
            if self.fixed_ptr >= len(self.containers):
                st.warning("⚠️ Grid Overflow: More cells requested than defined.")
                yield st.container()
                return
            
            r, c, target_container = self.containers[self.fixed_ptr]
            self.fixed_ptr += 1
            
        elif self.current_row_cols:
            # DYNAMIC MODE logic
            if self.row_cell_idx >= len(self.current_row_cols):
                st.warning("⚠️ Row Overflow: More cells requested than cols in row.")
                yield st.container()
                return

            target_container = self.current_row_cols[self.row_cell_idx]
            r = self.current_row_idx
            c = self.row_cell_idx
            self.row_cell_idx += 1
            
        else:
            raise RuntimeError("Grid Error: Call `with grid.row():` before `with grid.cell():`")

        # --- 2. Resolve Style ---
        # We determine the style before entering the context
        style_to_apply = self._resolve_style(r, c)
        
        # Increment global counter for the *next* call
        self.global_cell_counter += 1

        # --- 3. Render Cell (Internalized Block Logic) ---
        with target_container:
            cell_id = generate_key("cell")
            
            # CSS: Target the stVerticalBlock wrapping the cell content
            # height: 100% ensures the background fills the Equal Height column
            css = f"""
            <style>
                /* keeps cells in a same row the same height */
                div:has(> .stVerticalBlock > .element-container > .stHtml > span.{cell_id}) {{
                    height: 100%;
                    flex-direction: row;
                }}
                div:has(> .element-container > .stHtml > span.{cell_id}) {{
                    {str(style_to_apply)}
                }}
                .element-container:has(.stHtml > span.{cell_id}) {{
                    width: auto;
                }}
            </style>
            """
            st.html(css)
            
            with st.container():
                st.html(f'<span class="{cell_id}" style="display:none"></span>')
                yield

    @contextmanager
    def row(self, cols: int):
        """
        Creates a new dynamic row with `cols` columns.
        Used only when st_grid was initialized without fixed rows/cols.
        """
        if self.containers:
            st.error("❌ Cannot add dynamic rows to a fixed grid.")
            yield
            return

        # Initialize state for this row
        self.current_row_cols = st.columns(cols, gap=self.gap)
        self.row_cell_idx = 0 # Reset cell counter for this new row
        
        yield #  Return control to the user's `with` block
        
        # Cleanup after row is done
        self.current_row_idx += 1
        self.current_row_cols = []

@contextmanager
def st_grid(
    rows: int = None, 
    cols: int = None, 
    grid_style: Style = StreamTeX_Styles.none, 
    cell_styles: CELL_STYLES_TYPE = StreamTeX_Styles.none,
    auto_width: bool = False
):
    """
    Context Manager for creating styled grids with Equal Height cells.
    
    Args:
        rows (int, optional): Fixed number of rows.
        cols (int, optional): Fixed number of columns.
        grid_style (Style): Style wrapper for the whole grid.
        cell_styles: Style(s) for cells. Can be Single, List, Matrix, or StyleGrid.
        auto_width: If True, columns will shrink to fit their content instead of expanding.
        
    ## Usage:
        (Fixed):
        ```
        with st_grid(2, 2) as g:
            with g.cell(): ...
            with g.cell(): ...
        ```
            
        (Dynamic):
        ```
        with st_grid() as g:
            with g.row(3):
                with g.cell(): ...
        ```
    """
    # 1. Generate Unique Grid ID
    grid_id = generate_key("grid")
    
# 2. Inject Scoped CSS (Wrapper Style + Equal Height Logic)
    # The 'grid_id' is placed in the wrapper, allowing us to target all internal columns
    css = f"""
    <style>
        /* A. Grid Wrapper Style */
        div[data-testid="stVerticalBlock"]:has(> .element-container .stHtml span.{grid_id}) {{
            {str(grid_style)}
        }}
        .element-container:has(.stHtml > span.{grid_id}) {{
            width: auto;
        }}
    </style>
    """
    st.html(css)
    
    # 3. Render Grid Wrapper
    with st.container():
        # Marker for the Wrapper
        st.html(f'<span class="{grid_id}" style="display:none"></span>')
        
        # 4. Initialize Controller
        controller = GridController(rows, cols, cell_styles, auto_width)
        yield controller