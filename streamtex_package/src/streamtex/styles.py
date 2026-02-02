from typing import List, Tuple, Optional, Type, Union
import re


theme = {}
'''The theme style dictionary.
Example: dark = {
    "red_02" : "color: #660000;",
    "pink_01": "color: #d6fc00;"   
}'''

def add_css(str1: str, str2: str):
    '''Concatenates two css strings with a ";" in between.'''
    if str1 and str2:
        return str1 + "; " + str2
    elif str1:
        return str1
    else:
        return str2

def remove_css(str1: str, str2: str):
    '''Removes one css string (str2) from another (str1) if present.'''
    # Split CSS strings into lists of properties
    props1 = [prop.strip() for prop in str1.split(';') if prop.strip()]
    props2 = [prop.strip() for prop in str2.split(';') if prop.strip()]

    # Extract property names from props2
    import re
    prop_names2 = set()
    for prop in props2:
        match = re.match(r'^([^:]+):', prop)
        if match:
            prop_name = match.group(1).strip()
            prop_names2.add(prop_name)

    # Remove properties from props1 that are in prop_names2
    new_props1 = []
    for prop in props1:
        match = re.match(r'^([^:]+):', prop)
        if match:
            prop_name = match.group(1).strip()
            if prop_name not in prop_names2:
                new_props1.append(prop)
        else:
            # Keep properties without a colon (malformed)
            new_props1.append(prop)

    return '; '.join(new_props1)

class Style:
    """Defines a style, encapsulating a string of (maybe) multiple CSS in-line styles, with a global theme."""
    def __init__(self, css: str, style_id: str = ""):
        '''The raw CSS definition'''
        self.css = css      
        '''The ID used to look up theme overrides'''
        self.style_id = style_id  
    @classmethod
    def create(cls, style, style_id: str):
        """
        Factory method: create a new Style from an existing one, overriding the style_id.
        """
        return cls(style.css, style_id)

    def __add__(self, other):
        if isinstance(other, Style):
            # Combine the theme-based CSS from each side
            combined_css = add_css(str(self), str(other))

            # Merge the style IDs
            new_id = f"{self.style_id} {other.style_id}".strip()
            return Style(combined_css, new_id)

        elif isinstance(other, str):
            # Combine self's theme-based CSS with raw CSS string
            combined_css = add_css(str(self), other)
            clean_str_id = other.replace(" ", "").replace(";", "")
            new_id = f"{self.style_id} {clean_str_id}".strip()
            return Style(combined_css, new_id)

        return NotImplemented

    def __radd__(self, other):
        # define reserve addition
        if isinstance(other, str):
            combined_css = add_css(other, str(self))
            clean_str_id = other.replace(" ", "").replace(";", "")
            new_id = f"{clean_str_id} {self.style_id}".strip()
            return Style(combined_css, new_id)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Style):
            # Remove other's theme-based CSS from self's theme-based CSS
            new_css = remove_css(str(self), str(other))
            new_id = f"{self.style_id}-{other.style_id}".strip()
            return Style(new_css, new_id)

        elif isinstance(other, str):
            new_css = remove_css(str(self), other)
            clean_str_id = other.replace(" ", "").replace(";", "")
            new_id = f"{self.style_id}-{clean_str_id}".strip()
            return Style(new_css, new_id)

        return NotImplemented

    def __rsub__(self, other):
        # define reverse subtraction
        if isinstance(other, str):
            new_css = remove_css(other, str(self))
            clean_str_id = other.replace(" ", "").replace(";", "")
            new_id = f"{clean_str_id}-{self.style_id}".strip()
            return Style(new_css, new_id)
        return NotImplemented

    def __bool__(self):
        # Return False if the theme-based CSS is empty or whitespace
        return bool(str(self).strip())

    def __repr__(self):
        """
        If a global theme override exists for self.style_id, use that in place of self.css.
        Otherwise, fallback to self.css.
        """
        return theme.get(self.style_id, self.css)

class ListStyle(Style):
    """
    Defines a style for lists, including a style ID for theme lookups
    and custom list symbols for styling levels.
    """
    def __init__(self, css: str = "", style_id: str = "", symbols: List[str] = None):
        super().__init__(css, style_id)
        # Provide a default list of symbols if not specified
        self.symbols = symbols if symbols is not None else ["●"]

    @classmethod
    def create(cls, style, style_id: str):
        """
        Factory method: create a new ListStyle from an existing one, overriding the style_id.
        Copies over the existing symbols.
        """
        return cls(style.css, style_id, style.symbols)

    def __add__(self, other):
        if isinstance(other, Style):
            # Combine theme-based CSS from each
            combined_css = add_css(str(self), str(other))
            new_id = f"{self.style_id} {other.style_id}".strip()

            # Merge symbols if other is ListStyle
            new_symbols = list(self.symbols)
            if isinstance(other, ListStyle):
                new_symbols.extend(other.symbols)

            return ListStyle(combined_css, new_id, new_symbols)

        elif isinstance(other, str):
            combined_css = add_css(str(self), other)
            clean_str_id = other.replace(" ", "").replace(";", "")
            new_id = f"{self.style_id} {clean_str_id}".strip()

            return ListStyle(combined_css, new_id, self.symbols)

        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, str):
            combined_css = add_css(other, str(self))
            clean_str_id = other.replace(" ", "").replace(";", "")
            new_id = f"{clean_str_id} {self.style_id}".strip()

            return ListStyle(combined_css, new_id, self.symbols)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Style):
            # Remove other's theme-based CSS from self's theme-based CSS
            new_css = remove_css(str(self), str(other))
            new_id = f"{self.style_id}-{other.style_id}".strip()

            # Subtract symbols if other is also a ListStyle
            new_symbols = list(self.symbols)
            if isinstance(other, ListStyle):
                for sym in other.symbols:
                    if sym in new_symbols:
                        new_symbols.remove(sym)

            return ListStyle(new_css, new_id, new_symbols)

        elif isinstance(other, str):
            new_css = remove_css(str(self), other)
            clean_str_id = other.replace(" ", "").replace(";", "")
            new_id = f"{self.style_id}-{clean_str_id}".strip()
            return ListStyle(new_css, new_id, self.symbols)

        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, str):
            new_css = remove_css(other, str(self))
            clean_str_id = other.replace(" ", "").replace(";", "")
            new_id = f"{clean_str_id}-{self.style_id}".strip()
            return ListStyle(new_css, new_id, self.symbols)
        return NotImplemented

    def lvl(self, lvl: int = 1):
        """
        Returns the CSS needed for the list-style-type property
        based on the current nesting level. Cycles through the
        symbols if the level exceeds the number of symbols.
        """
        index = (lvl - 1) % len(self.symbols)
        return f"list-style-type: '{self.symbols[index]}';"



class StyleGrid:
    """
    Defines a grid of styles that will be applied to the rows/columns of a table or grid.
    """

    def __init__(self, css_grid: List[List[Style]] = []):
        self.css_grid = css_grid

    def __add__(self, other):
        """
        Overlapping styles are added in the order of the style grids addition.
        """
        if isinstance(other, StyleGrid):
            return self._combine_with(other, combine_styles=lambda s1, s2: s1 + s2)
        
        elif isinstance(other, list):
            return self + StyleGrid(other)
        
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, StyleGrid):
            # Reverse addition: other + self
            return other + self
        
        elif isinstance(other, list):
            return StyleGrid(other) + self
        
        return NotImplemented
    

    def __sub__(self, other):
        """
        Overlapping styles are subtracted in the order of the style grids subtraction.
        """
        if isinstance(other, StyleGrid):
            return self._combine_with(other, combine_styles=lambda s1, s2: s1 - s2)
        elif isinstance(other, list):
            return self - StyleGrid(other)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, StyleGrid):
            # Reverse subtraction: other - self
            return other - self
        elif isinstance(other, list):
            return StyleGrid(other) - self
        return NotImplemented

    def __mul__(self, other):
        """
        Multiplication works like addition but styles at the same cell are replaced.
        """
        if isinstance(other, StyleGrid):
            return self._combine_with(other, combine_styles=lambda s1, s2: s2 if s2 else s1)
        elif isinstance(other, list):
            return self * StyleGrid(other)
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, StyleGrid):
            # Reverse multiplication: other * self
            return other * self    
        elif isinstance(other, list):
            return StyleGrid(other) * self
        return NotImplemented

    def _combine_with(self, other, combine_styles):
        """
        Combines two StyleGrids using the provided combine_styles function for overlapping cells.
        """
        self_rows, self_cols = self._get_dimensions()
        other_rows, other_cols = other._get_dimensions()

        max_rows = max(self_rows, other_rows)
        max_cols = max(self_cols, other_cols)

        # Initialize new grid with Styles.none
        new_grid = [[StreamTeX_Styles.none for _ in range(max_cols)] for _ in range(max_rows)]

        # Fill in styles from self
        for i in range(self_rows):
            for j in range(len(self.css_grid[i])):
                new_grid[i][j] = self.css_grid[i][j]

        # Combine styles from other
        for i in range(other_rows):
            for j in range(len(other.css_grid[i])):
                if i < max_rows and j < max_cols:
                    new_grid[i][j] = combine_styles(new_grid[i][j], other.css_grid[i][j])

        return StyleGrid(new_grid)

    def _get_dimensions(self) -> Tuple[int, int]:
        if not self.css_grid:
            return 0, 0
        num_rows = len(self.css_grid)
        num_cols = max(len(row) for row in self.css_grid) if self.css_grid else 0
        return num_rows, num_cols

    @staticmethod
    def create(cells: str, style: Style, num_rows: Optional[int] = None, num_cols: Optional[int] = None):
        """
        Creates a StyleGrid with the specified cells filled with the given style.
        Cells are specified in Excel-like notation (e.g., "A1:C3,B5").
        Other cells are filled with Styles.none.
        """
        # Parse the cells string to get the list of cell indices
        cells_list = StyleGrid._parse_cells(cells)

        # Determine the required grid size
        max_row_index = max((row for row, _ in cells_list), default=0)
        max_col_index = max((col for _, col in cells_list), default=0)

        # Adjust grid size based on provided num_rows and num_cols
        grid_rows = max(num_rows if num_rows is not None else 0, max_row_index + 1)
        grid_cols = max(num_cols if num_cols is not None else 0, max_col_index + 1)

        # Initialize the grid with Styles.none
        grid = [[StreamTeX_Styles.none for _ in range(grid_cols)] for _ in range(grid_rows)]

        # Fill in the specified cells with the given style
        for row, col in cells_list:
            if row < grid_rows and col < grid_cols:
                grid[row][col] = style

        return StyleGrid(grid)

    @staticmethod
    def _parse_cells(cells_str: str) -> List[Tuple[int, int]]:
        """
        Parses a string of cell ranges in Excel-like notation and returns a list of cell indices.
        """
        cells = []
        ranges = cells_str.split(',')
        for cell_range in ranges:
            cell_range = cell_range.strip()
            if ':' in cell_range:
                start_cell, end_cell = cell_range.split(':')
                start_row, start_col = StyleGrid._cell_to_indices(start_cell.strip())
                end_row, end_col = StyleGrid._cell_to_indices(end_cell.strip())

                # Swap if start is after end
                if start_row > end_row:
                    start_row, end_row = end_row, start_row
                if start_col > end_col:
                    start_col, end_col = end_col, start_col

                for row in range(start_row, end_row + 1):
                    for col in range(start_col, end_col + 1):
                        cells.append((row, col))
            else:
                row, col = StyleGrid._cell_to_indices(cell_range)
                cells.append((row, col))
        return cells

    @staticmethod
    def _cell_to_indices(cell: str) -> Tuple[int, int]:
        """
        Converts a cell reference (e.g., "A1") to zero-based (row, col) indices.
        """
        match = re.match(r'^([A-Za-z]+)([0-9]+)$', cell)
        if not match:
            raise ValueError(f"Invalid cell reference: {cell}")
        col_str, row_str = match.groups()
        col_index = StyleGrid._column_letter_to_index(col_str)
        row_index = int(row_str) - 1  # Convert to zero-based index
        return row_index, col_index

    @staticmethod
    def _column_letter_to_index(col_str: str) -> int:
        """
        Converts column letters to a zero-based column index.
        """
        col_str = col_str.upper()
        col_index = 0
        for char in col_str:
            if 'A' <= char <= 'Z':
                col_index = col_index * 26 + (ord(char) - ord('A') + 1)
            else:
                raise ValueError(f"Invalid column letter: {char}")
        return col_index - 1  # Convert to zero-based index


class Decors:
    # Font decoration
    italic_text        = Style("font-style: italic;",     "italic_text")
    underline_text     = Style("text-decoration: underline;", "underline_text")
    decor_none_text    = Style("text-decoration: none;",  "decor_none_text")
    strike_text        = Style("text-decoration: line-through;", "strike_text")

class Weights:
    # Font weights
    bold_weight        = Style("font-weight: bold;",   "bold_weight") # font-weight: 700
    light_weight       = Style("font-weight: 300;",    "light_weight")
    normal_weight      = Style("font-weight: normal;", "normal_weight")

class Alignments:
    # Text alignment (multiline alignment, not element positioning)
    center_align       = Style("text-align: center;",  "center_align")
    right_align        = Style("text-align: right;",   "right_align")
    left_align         = Style("text-align: left;",    "left_align")
    justify_align      = Style("text-align: justify;", "justify_align")

class Colors:
    # Basic color styles
    reset              = Style("color: initial;",   "reset")
    alice_blue         = Style("color: AliceBlue;", "alice_blue")
    antique_white      = Style("color: AntiqueWhite;", "antique_white")
    aqua               = Style("color: Aqua;", "aqua")
    aquamarine         = Style("color: Aquamarine;", "aquamarine")
    azure              = Style("color: Azure;", "azure")
    beige              = Style("color: Beige;", "beige")
    bisque             = Style("color: Bisque;", "bisque")
    black              = Style("color: Black;", "black")
    blanched_almond    = Style("color: BlanchedAlmond;", "blanched_almond")
    blue               = Style("color: Blue;", "blue")
    blue_violet        = Style("color: BlueViolet;", "blue_violet")
    brown              = Style("color: Brown;", "brown")
    burly_wood         = Style("color: BurlyWood;", "burly_wood")
    cadet_blue         = Style("color: CadetBlue;", "cadet_blue")
    chartreuse         = Style("color: Chartreuse;", "chartreuse")
    chocolate          = Style("color: Chocolate;", "chocolate")
    coral              = Style("color: Coral;", "coral")
    cornflower_blue    = Style("color: CornflowerBlue;", "cornflower_blue")
    cornsilk           = Style("color: Cornsilk;", "cornsilk")
    crimson            = Style("color: Crimson;", "crimson")
    cyan               = Style("color: Cyan;", "cyan")
    dark_blue          = Style("color: DarkBlue;", "dark_blue")
    dark_cyan          = Style("color: DarkCyan;", "dark_cyan")
    dark_golden_rod    = Style("color: DarkGoldenRod;", "dark_golden_rod")
    dark_gray          = Style("color: DarkGray;", "dark_gray")
    dark_grey          = Style("color: DarkGrey;", "dark_grey")
    dark_green         = Style("color: DarkGreen;", "dark_green")
    dark_khaki         = Style("color: DarkKhaki;", "dark_khaki")
    dark_magenta       = Style("color: DarkMagenta;", "dark_magenta")
    dark_olive_green   = Style("color: DarkOliveGreen;", "dark_olive_green")
    dark_orange        = Style("color: DarkOrange;", "dark_orange")
    dark_orchid        = Style("color: DarkOrchid;", "dark_orchid")
    dark_red           = Style("color: DarkRed;", "dark_red")
    dark_salmon        = Style("color: DarkSalmon;", "dark_salmon")
    dark_sea_green     = Style("color: DarkSeaGreen;", "dark_sea_green")
    dark_slate_blue    = Style("color: DarkSlateBlue;", "dark_slate_blue")
    dark_slate_gray    = Style("color: DarkSlateGray;", "dark_slate_gray")
    dark_slate_grey    = Style("color: DarkSlateGrey;", "dark_slate_grey")
    dark_turquoise     = Style("color: DarkTurquoise;", "dark_turquoise")
    dark_violet        = Style("color: DarkViolet;", "dark_violet")
    deep_pink          = Style("color: DeepPink;", "deep_pink")
    deep_sky_blue      = Style("color: DeepSkyBlue;", "deep_sky_blue")
    dim_gray           = Style("color: DimGray;", "dim_gray")
    dim_grey           = Style("color: DimGrey;", "dim_grey")
    dodger_blue        = Style("color: DodgerBlue;", "dodger_blue")
    fire_brick         = Style("color: FireBrick;", "fire_brick")
    floral_white       = Style("color: FloralWhite;", "floral_white")
    forest_green       = Style("color: ForestGreen;", "forest_green")
    fuchsia            = Style("color: Fuchsia;", "fuchsia")
    gainsboro          = Style("color: Gainsboro;", "gainsboro")
    ghost_white        = Style("color: GhostWhite;", "ghost_white")
    gold               = Style("color: Gold;", "gold")
    golden_rod         = Style("color: GoldenRod;", "golden_rod")
    gray               = Style("color: Gray;", "gray")
    grey               = Style("color: Grey;", "grey")
    green              = Style("color: Green;", "green")
    green_yellow       = Style("color: GreenYellow;", "green_yellow")
    honey_dew          = Style("color: HoneyDew;", "honey_dew")
    hot_pink           = Style("color: HotPink;", "hot_pink")
    indian_red         = Style("color: IndianRed;", "indian_red")
    indigo             = Style("color: Indigo;", "indigo")
    ivory              = Style("color: Ivory;", "ivory")
    khaki              = Style("color: Khaki;", "khaki")
    lavender           = Style("color: Lavender;", "lavender")
    lavender_blush     = Style("color: LavenderBlush;", "lavender_blush")
    lawn_green         = Style("color: LawnGreen;", "lawn_green")
    lemon_chiffon      = Style("color: LemonChiffon;", "lemon_chiffon")
    light_blue         = Style("color: LightBlue;", "light_blue")
    light_coral        = Style("color: LightCoral;", "light_coral")
    light_cyan         = Style("color: LightCyan;", "light_cyan")
    light_golden_rod_yellow = Style("color: LightGoldenRodYellow;", "light_golden_rod_yellow")
    light_gray         = Style("color: LightGray;", "light_gray")
    light_grey         = Style("color: LightGrey;", "light_grey")
    light_green        = Style("color: LightGreen;", "light_green")
    light_pink         = Style("color: LightPink;", "light_pink")
    light_salmon       = Style("color: LightSalmon;", "light_salmon")
    light_sea_green    = Style("color: LightSeaGreen;", "light_sea_green")
    light_sky_blue     = Style("color: LightSkyBlue;", "light_sky_blue")
    light_slate_gray   = Style("color: LightSlateGray;", "light_slate_gray")
    light_slate_grey   = Style("color: LightSlateGrey;", "light_slate_grey")
    light_steel_blue   = Style("color: LightSteelBlue;", "light_steel_blue")
    light_yellow       = Style("color: LightYellow;", "light_yellow")
    lime               = Style("color: Lime;", "lime")
    lime_green         = Style("color: LimeGreen;", "lime_green")
    linen              = Style("color: Linen;", "linen")
    magenta            = Style("color: Magenta;", "magenta")
    maroon             = Style("color: Maroon;", "maroon")
    medium_aqua_marine = Style("color: MediumAquaMarine;", "medium_aqua_marine")
    medium_blue        = Style("color: MediumBlue;", "medium_blue")
    medium_orchid      = Style("color: MediumOrchid;", "medium_orchid")
    medium_purple      = Style("color: MediumPurple;", "medium_purple")
    medium_sea_green   = Style("color: MediumSeaGreen;", "medium_sea_green")
    medium_slate_blue  = Style("color: MediumSlateBlue;", "medium_slate_blue")
    medium_spring_green= Style("color: MediumSpringGreen;", "medium_spring_green")
    medium_turquoise   = Style("color: MediumTurquoise;", "medium_turquoise")
    medium_violet_red  = Style("color: MediumVioletRed;", "medium_violet_red")
    midnight_blue      = Style("color: MidnightBlue;", "midnight_blue")
    mint_cream         = Style("color: MintCream;", "mint_cream")
    misty_rose         = Style("color: MistyRose;", "misty_rose")
    moccasin           = Style("color: Moccasin;", "moccasin")
    navajo_white       = Style("color: NavajoWhite;", "navajo_white")
    navy               = Style("color: Navy;", "navy")
    old_lace           = Style("color: OldLace;", "old_lace")
    olive              = Style("color: Olive;", "olive")
    olive_drab         = Style("color: OliveDrab;", "olive_drab")
    orange             = Style("color: Orange;", "orange")
    orange_red         = Style("color: OrangeRed;", "orange_red")
    orchid             = Style("color: Orchid;", "orchid")
    pale_golden_rod    = Style("color: PaleGoldenRod;", "pale_golden_rod")
    pale_green         = Style("color: PaleGreen;", "pale_green")
    pale_turquoise     = Style("color: PaleTurquoise;", "pale_turquoise")
    pale_violet_red    = Style("color: PaleVioletRed;", "pale_violet_red")
    papaya_whip        = Style("color: PapayaWhip;", "papaya_whip")
    peach_puff         = Style("color: PeachPuff;", "peach_puff")
    peru               = Style("color: Peru;", "peru")
    pink               = Style("color: Pink;", "pink")
    plum               = Style("color: Plum;", "plum")
    powder_blue        = Style("color: PowderBlue;", "powder_blue")
    purple             = Style("color: Purple;", "purple")
    rebecca_purple     = Style("color: RebeccaPurple;", "rebecca_purple")
    red                = Style("color: Red;", "red")
    rosy_brown         = Style("color: RosyBrown;", "rosy_brown")
    royal_blue         = Style("color: RoyalBlue;", "royal_blue")
    saddle_brown       = Style("color: SaddleBrown;", "saddle_brown")
    salmon             = Style("color: Salmon;", "salmon")
    sandy_brown        = Style("color: SandyBrown;", "sandy_brown")
    sea_green          = Style("color: SeaGreen;", "sea_green")
    sea_shell          = Style("color: SeaShell;", "sea_shell")
    sienna             = Style("color: Sienna;", "sienna")
    silver             = Style("color: Silver;", "silver")
    sky_blue           = Style("color: SkyBlue;", "sky_blue")
    slate_blue         = Style("color: SlateBlue;", "slate_blue")
    slate_gray         = Style("color: SlateGray;", "slate_gray")
    slate_grey         = Style("color: SlateGrey;", "slate_grey")
    snow               = Style("color: Snow;", "snow")
    spring_green       = Style("color: SpringGreen;", "spring_green")
    steel_blue         = Style("color: SteelBlue;", "steel_blue")
    tan                = Style("color: Tan;", "tan")
    teal               = Style("color: Teal;", "teal")
    thistle            = Style("color: Thistle;", "thistle")
    tomato             = Style("color: Tomato;", "tomato")
    turquoise          = Style("color: Turquoise;", "turquoise")
    violet             = Style("color: Violet;", "violet")
    wheat              = Style("color: Wheat;", "wheat")
    white              = Style("color: White;", "white")
    white_smoke        = Style("color: WhiteSmoke;", "white_smoke")
    yellow             = Style("color: Yellow;", "yellow")
    yellow_green       = Style("color: YellowGreen;", "yellow_green")



class Sizes:
    @staticmethod
    def size(size: Union[str, int] = 16, style_id: Optional[str] = None):
        """
        Creates a text Style with the specified font size, default unit is 'pt' if size is an integer.
        An optional style_id can be provided for theme lookups.

        :param size: The size for the font. If int, it becomes '{size}pt'.
        :param style_id: An optional identifier for the global theme dictionary.
        :return: A Style object representing the specified font size.
        """
        if isinstance(size, int):
            size = f"{size}pt"
        # Derive a default style_id if none provided
        if not style_id:
            style_id = f"size_{size.replace(' ', '').replace(';', '').replace(':','')}"
        return Style(f"font-size: {size};", style_id)

    Giant_em_size   = Style("font-size: 8em;",   "Giant_em_size")
    """8em"""
    giant_em_size   = Style("font-size: 7em;",   "giant_em_size")
    """7em"""
    Huge_em_size    = Style("font-size: 6em;",   "Huge_em_size")
    """6em"""
    huge_em_size    = Style("font-size: 5em;",   "huge_em_size")
    """5em"""
    LARGE_em_size   = Style("font-size: 4em;",   "LARGE_em_size")
    """4em"""
    Large_em_size   = Style("font-size: 3em;",   "Large_em_size")
    """3em"""
    large_em_size   = Style("font-size: 2em;",   "large_em_size")
    """2em"""
    big_em_size     = Style("font-size: 1.5em;", "big_em_size")
    """1.5em"""
    medium_em_size  = Style("font-size: 1em;",   "medium_em_size")
    """1em"""
    little_em_size  = Style("font-size: 0.75em;","little_em_size")
    """0.75em"""
    small_em_size   = Style("font-size: 0.5em;", "small_em_size")
    """0.5em"""
    tiny_em_size    = Style("font-size: 0.25em;","tiny_em_size")
    """0.25em"""
            
    Giant_px_size   = Style("font-size: 128px;", "Giant_px_size")
    """128px"""
    giant_px_size   = Style("font-size: 112px;", "giant_px_size")
    """112px"""
    Huge_px_size    = Style("font-size: 96px;",  "Huge_px_size")
    """96px"""
    huge_px_size    = Style("font-size: 80px;",  "huge_px_size")
    """80px"""
    LARGE_px_size   = Style("font-size: 64px;",  "LARGE_px_size")
    """64px"""
    Large_px_size   = Style("font-size: 48px;",  "Large_px_size")
    """48px"""
    large_px_size   = Style("font-size: 32px;",  "large_px_size")
    """32px"""
    big_px_size     = Style("font-size: 24px;",  "big_px_size")
    """24px"""
    medium_px_size  = Style("font-size: 16px;",  "medium_px_size")
    """16px"""
    little_px_size  = Style("font-size: 12px;",  "little_px_size")
    """12px"""
    small_px_size   = Style("font-size: 8px;",   "small_px_size")
    """8px"""
    tiny_px_size    = Style("font-size: 4px;",   "tiny_px_size")
    """4px"""

    GIANT_size      = Style("font-size: 196pt;", "GIANT_size")
    """196pt"""
    Giant_size      = Style("font-size: 128pt;", "Giant_size")
    """128pt"""
    giant_size      = Style("font-size: 112pt;", "giant_size")
    """112pt"""
    Huge_size       = Style("font-size: 96pt;",  "Huge_size")
    """96pt"""
    huge_size       = Style("font-size: 80pt;",  "huge_size")
    """80pt"""
    LARGE_size      = Style("font-size: 64pt;",  "LARGE_size")
    """64pt"""
    Large_size      = Style("font-size: 48pt;",  "Large_size")
    """48pt"""
    large_size      = Style("font-size: 32pt;",  "large_size")
    """32pt"""
    big_size        = Style("font-size: 24pt;",  "big_size")
    """24pt"""
    medium_size     = Style("font-size: 16pt;",  "medium_size")
    """16pt"""
    little_size     = Style("font-size: 12pt;",  "little_size")
    """12pt"""
    small_size      = Style("font-size: 8pt;",   "small_size")
    """8pt"""
    tiny_size       = Style("font-size: 4pt;",   "tiny_size")
    """4pt"""

class Fonts:
    # Sans-serif fonts
    font_arial         = Style("font-family: Arial; font-style: normal;",         "font_arial")
    font_helvetica     = Style("font-family: Helvetica; font-style: normal;",     "font_helvetica")
    font_verdana       = Style("font-family: Verdana; font-style: normal;",       "font_verdana")
    font_tahoma        = Style("font-family: Tahoma; font-style: normal;",        "font_tahoma")
    font_trebuchet_ms  = Style("font-family: 'Trebuchet MS'; font-style: normal;","font_trebuchet_ms")
    font_gill_sans     = Style("font-family: 'Gill Sans'; font-style: normal;",   "font_gill_sans")

    # Serif fonts
    font_times_new_roman = Style("font-family: 'Times New Roman'; font-style: normal;", "font_times_new_roman")
    font_georgia         = Style("font-family: Georgia; font-style: normal;",           "font_georgia")
    font_garamond        = Style("font-family: Garamond; font-style: normal;",          "font_garamond")
    font_baskerville     = Style("font-family: Baskerville; font-style: normal;",       "font_baskerville")
    font_caslon          = Style("font-family: Caslon; font-style: normal;",            "font_caslon")
    font_book_antiqua    = Style("font-family: 'Book Antiqua'; font-style: normal;",    "font_book_antiqua")
    
    # Monospace fonts
    font_courier_new   = Style("font-family: 'Courier New'; font-style: normal;",  "font_courier_new")
    font_lucida_console= Style("font-family: 'Lucida Console'; font-style: normal;","font_lucida_console")
    font_monaco        = Style("font-family: Monaco; font-style: normal;",         "font_monaco")
    font_consolas      = Style("font-family: Consolas; font-style: normal;",       "font_consolas")

    # Cursive fonts
    font_comic_sans_ms   = Style("font-family: 'Comic Sans MS'; font-style: normal;",   "font_comic_sans_ms")
    font_brush_script_mt = Style("font-family: 'Brush Script MT'; font-style: normal;", "font_brush_script_mt")

    # Fantasy fonts
    font_impact     = Style("font-family: Impact; font-style: normal;",    "font_impact")
    font_luminari   = Style("font-family: Luminari; font-style: normal;",  "font_luminari")
    font_chalkduster= Style("font-family: Chalkduster; font-style: normal;","font_chalkduster")

    # System UI fonts
    font_system_ui   = Style("font-family: system-ui; font-style: normal;",  "font_system_ui")
    font_segoe_ui    = Style("font-family: 'Segoe UI'; font-style: normal;", "font_segoe_ui")
    font_apple_system= Style("font-family: -apple-system; font-style: normal;", "font_apple_system")
    font_sans_serif  = Style("font-family: sans-serif; font-style: normal;", "font_sans_serif")
    font_serif       = Style("font-family: serif; font-style: normal;",     "font_serif")
    font_monospace   = Style("font-family: monospace; font-style: normal;", "font_monospace")


class BackgroundColors:
    reset_bg              = Style("background-color: initial;",           "reset_bg")
    alice_blue_bg         = Style("background-color: AliceBlue;",         "alice_blue_bg")
    antique_white_bg      = Style("background-color: AntiqueWhite;",      "antique_white_bg")
    aqua_bg               = Style("background-color: Aqua;",              "aqua_bg")
    aquamarine_bg         = Style("background-color: Aquamarine;",        "aquamarine_bg")
    azure_bg              = Style("background-color: Azure;",             "azure_bg")
    beige_bg              = Style("background-color: Beige;",             "beige_bg")
    bisque_bg             = Style("background-color: Bisque;",            "bisque_bg")
    black_bg              = Style("background-color: Black;",             "black_bg")
    blanched_almond_bg    = Style("background-color: BlanchedAlmond;",    "blanched_almond_bg")
    blue_bg               = Style("background-color: Blue;",              "blue_bg")
    blue_violet_bg        = Style("background-color: BlueViolet;",        "blue_violet_bg")
    brown_bg              = Style("background-color: Brown;",             "brown_bg")
    burly_wood_bg         = Style("background-color: BurlyWood;",         "burly_wood_bg")
    cadet_blue_bg         = Style("background-color: CadetBlue;",         "cadet_blue_bg")
    chartreuse_bg         = Style("background-color: Chartreuse;",        "chartreuse_bg")
    chocolate_bg          = Style("background-color: Chocolate;",         "chocolate_bg")
    coral_bg              = Style("background-color: Coral;",             "coral_bg")
    cornflower_blue_bg    = Style("background-color: CornflowerBlue;",    "cornflower_blue_bg")
    cornsilk_bg           = Style("background-color: Cornsilk;",          "cornsilk_bg")
    crimson_bg            = Style("background-color: Crimson;",           "crimson_bg")
    cyan_bg               = Style("background-color: Cyan;",              "cyan_bg")
    dark_blue_bg          = Style("background-color: DarkBlue;",          "dark_blue_bg")
    dark_cyan_bg          = Style("background-color: DarkCyan;",          "dark_cyan_bg")
    dark_golden_rod_bg    = Style("background-color: DarkGoldenRod;",     "dark_golden_rod_bg")
    dark_gray_bg          = Style("background-color: DarkGray;",          "dark_gray_bg")
    dark_grey_bg          = Style("background-color: DarkGrey;",          "dark_grey_bg")
    dark_green_bg         = Style("background-color: DarkGreen;",         "dark_green_bg")
    dark_khaki_bg         = Style("background-color: DarkKhaki;",         "dark_khaki_bg")
    dark_magenta_bg       = Style("background-color: DarkMagenta;",       "dark_magenta_bg")
    dark_olive_green_bg   = Style("background-color: DarkOliveGreen;",    "dark_olive_green_bg")
    dark_orange_bg        = Style("background-color: DarkOrange;",        "dark_orange_bg")
    dark_orchid_bg        = Style("background-color: DarkOrchid;",        "dark_orchid_bg")
    dark_red_bg           = Style("background-color: DarkRed;",           "dark_red_bg")
    dark_salmon_bg        = Style("background-color: DarkSalmon;",        "dark_salmon_bg")
    dark_sea_green_bg     = Style("background-color: DarkSeaGreen;",      "dark_sea_green_bg")
    dark_slate_blue_bg    = Style("background-color: DarkSlateBlue;",     "dark_slate_blue_bg")
    dark_slate_gray_bg    = Style("background-color: DarkSlateGray;",     "dark_slate_gray_bg")
    dark_slate_grey_bg    = Style("background-color: DarkSlateGrey;",     "dark_slate_grey_bg")
    dark_turquoise_bg     = Style("background-color: DarkTurquoise;",     "dark_turquoise_bg")
    dark_violet_bg        = Style("background-color: DarkViolet;",        "dark_violet_bg")
    deep_pink_bg          = Style("background-color: DeepPink;",          "deep_pink_bg")
    deep_sky_blue_bg      = Style("background-color: DeepSkyBlue;",       "deep_sky_blue_bg")
    dim_gray_bg           = Style("background-color: DimGray;",           "dim_gray_bg")
    dim_grey_bg           = Style("background-color: DimGrey;",           "dim_grey_bg")
    dodger_blue_bg        = Style("background-color: DodgerBlue;",        "dodger_blue_bg")
    fire_brick_bg         = Style("background-color: FireBrick;",         "fire_brick_bg")
    floral_white_bg       = Style("background-color: FloralWhite;",       "floral_white_bg")
    forest_green_bg       = Style("background-color: ForestGreen;",       "forest_green_bg")
    fuchsia_bg            = Style("background-color: Fuchsia;",           "fuchsia_bg")
    gainsboro_bg          = Style("background-color: Gainsboro;",         "gainsboro_bg")
    ghost_white_bg        = Style("background-color: GhostWhite;",        "ghost_white_bg")
    gold_bg               = Style("background-color: Gold;",              "gold_bg")
    golden_rod_bg         = Style("background-color: GoldenRod;",         "golden_rod_bg")
    gray_bg               = Style("background-color: Gray;",              "gray_bg")
    grey_bg               = Style("background-color: Grey;",              "grey_bg")
    green_bg              = Style("background-color: Green;",             "green_bg")
    green_yellow_bg       = Style("background-color: GreenYellow;",       "green_yellow_bg")
    honey_dew_bg          = Style("background-color: HoneyDew;",          "honey_dew_bg")
    hot_pink_bg           = Style("background-color: HotPink;",           "hot_pink_bg")
    indian_red_bg         = Style("background-color: IndianRed;",         "indian_red_bg")
    indigo_bg             = Style("background-color: Indigo;",            "indigo_bg")
    ivory_bg              = Style("background-color: Ivory;",             "ivory_bg")
    khaki_bg              = Style("background-color: Khaki;",             "khaki_bg")
    lavender_bg           = Style("background-color: Lavender;",          "lavender_bg")
    lavender_blush_bg     = Style("background-color: LavenderBlush;",     "lavender_blush_bg")
    lawn_green_bg         = Style("background-color: LawnGreen;",         "lawn_green_bg")
    lemon_chiffon_bg      = Style("background-color: LemonChiffon;",      "lemon_chiffon_bg")
    light_blue_bg         = Style("background-color: LightBlue;",         "light_blue_bg")
    light_coral_bg        = Style("background-color: LightCoral;",        "light_coral_bg")
    light_cyan_bg         = Style("background-color: LightCyan;",         "light_cyan_bg")
    light_golden_rod_yellow_bg = Style("background-color: LightGoldenRodYellow;", "light_golden_rod_yellow_bg")
    light_gray_bg         = Style("background-color: LightGray;",         "light_gray_bg")
    light_grey_bg         = Style("background-color: LightGrey;",         "light_grey_bg")
    light_green_bg        = Style("background-color: LightGreen;",        "light_green_bg")
    light_pink_bg         = Style("background-color: LightPink;",         "light_pink_bg")
    light_salmon_bg       = Style("background-color: LightSalmon;",       "light_salmon_bg")
    light_sea_green_bg    = Style("background-color: LightSeaGreen;",     "light_sea_green_bg")
    light_sky_blue_bg     = Style("background-color: LightSkyBlue;",      "light_sky_blue_bg")
    light_slate_gray_bg   = Style("background-color: LightSlateGray;",    "light_slate_gray_bg")
    light_slate_grey_bg   = Style("background-color: LightSlateGrey;",    "light_slate_grey_bg")
    light_steel_blue_bg   = Style("background-color: LightSteelBlue;",    "light_steel_blue_bg")
    light_yellow_bg       = Style("background-color: LightYellow;",       "light_yellow_bg")
    lime_bg               = Style("background-color: Lime;",              "lime_bg")
    lime_green_bg         = Style("background-color: LimeGreen;",         "lime_green_bg")
    linen_bg              = Style("background-color: Linen;",             "linen_bg")
    magenta_bg            = Style("background-color: Magenta;",           "magenta_bg")
    maroon_bg             = Style("background-color: Maroon;",            "maroon_bg")
    medium_aqua_marine_bg = Style("background-color: MediumAquaMarine;",  "medium_aqua_marine_bg")
    medium_blue_bg        = Style("background-color: MediumBlue;",        "medium_blue_bg")
    medium_orchid_bg      = Style("background-color: MediumOrchid;",      "medium_orchid_bg")
    medium_purple_bg      = Style("background-color: MediumPurple;",      "medium_purple_bg")
    medium_sea_green_bg   = Style("background-color: MediumSeaGreen;",    "medium_sea_green_bg")
    medium_slate_blue_bg  = Style("background-color: MediumSlateBlue;",   "medium_slate_blue_bg")
    medium_spring_green_bg= Style("background-color: MediumSpringGreen;", "medium_spring_green_bg")
    medium_turquoise_bg   = Style("background-color: MediumTurquoise;",   "medium_turquoise_bg")
    medium_violet_red_bg  = Style("background-color: MediumVioletRed;",   "medium_violet_red_bg")
    midnight_blue_bg      = Style("background-color: MidnightBlue;",      "midnight_blue_bg")
    mint_cream_bg         = Style("background-color: MintCream;",         "mint_cream_bg")
    misty_rose_bg         = Style("background-color: MistyRose;",         "misty_rose_bg")
    moccasin_bg           = Style("background-color: Moccasin;",          "moccasin_bg")
    navajo_white_bg       = Style("background-color: NavajoWhite;",       "navajo_white_bg")
    navy_bg               = Style("background-color: Navy;",              "navy_bg")
    old_lace_bg           = Style("background-color: OldLace;",           "old_lace_bg")
    olive_bg              = Style("background-color: Olive;",             "olive_bg")
    olive_drab_bg         = Style("background-color: OliveDrab;",         "olive_drab_bg")
    orange_bg             = Style("background-color: Orange;",            "orange_bg")
    orange_red_bg         = Style("background-color: OrangeRed;",         "orange_red_bg")
    orchid_bg             = Style("background-color: Orchid;",            "orchid_bg")
    pale_golden_rod_bg    = Style("background-color: PaleGoldenRod;",     "pale_golden_rod_bg")
    pale_green_bg         = Style("background-color: PaleGreen;",         "pale_green_bg")
    pale_turquoise_bg     = Style("background-color: PaleTurquoise;",     "pale_turquoise_bg")
    pale_violet_red_bg    = Style("background-color: PaleVioletRed;",     "pale_violet_red_bg")
    papaya_whip_bg        = Style("background-color: PapayaWhip;",        "papaya_whip_bg")
    peach_puff_bg         = Style("background-color: PeachPuff;",         "peach_puff_bg")
    peru_bg               = Style("background-color: Peru;",              "peru_bg")
    pink_bg               = Style("background-color: Pink;",              "pink_bg")
    plum_bg               = Style("background-color: Plum;",              "plum_bg")
    powder_blue_bg        = Style("background-color: PowderBlue;",        "powder_blue_bg")
    purple_bg             = Style("background-color: Purple;",            "purple_bg")
    rebecca_purple_bg     = Style("background-color: RebeccaPurple;",     "rebecca_purple_bg")
    red_bg                = Style("background-color: Red;",               "red_bg")
    rosy_brown_bg         = Style("background-color: RosyBrown;",         "rosy_brown_bg")
    royal_blue_bg         = Style("background-color: RoyalBlue;",         "royal_blue_bg")
    saddle_brown_bg       = Style("background-color: SaddleBrown;",       "saddle_brown_bg")
    salmon_bg             = Style("background-color: Salmon;",            "salmon_bg")
    sandy_brown_bg        = Style("background-color: SandyBrown;",        "sandy_brown_bg")
    sea_green_bg          = Style("background-color: SeaGreen;",          "sea_green_bg")
    sea_shell_bg          = Style("background-color: SeaShell;",          "sea_shell_bg")
    sienna_bg             = Style("background-color: Sienna;",            "sienna_bg")
    silver_bg             = Style("background-color: Silver;",            "silver_bg")
    sky_blue_bg           = Style("background-color: SkyBlue;",           "sky_blue_bg")
    slate_blue_bg         = Style("background-color: SlateBlue;",         "slate_blue_bg")
    slate_gray_bg         = Style("background-color: SlateGray;",         "slate_gray_bg")
    slate_grey_bg         = Style("background-color: SlateGrey;",         "slate_grey_bg")
    snow_bg               = Style("background-color: Snow;",              "snow_bg")
    spring_green_bg       = Style("background-color: SpringGreen;",       "spring_green_bg")
    steel_blue_bg         = Style("background-color: SteelBlue;",         "steel_blue_bg")
    tan_bg                = Style("background-color: Tan;",               "tan_bg")
    teal_bg               = Style("background-color: Teal;",              "teal_bg")
    thistle_bg            = Style("background-color: Thistle;",           "thistle_bg")
    tomato_bg             = Style("background-color: Tomato;",            "tomato_bg")
    turquoise_bg          = Style("background-color: Turquoise;",         "turquoise_bg")
    violet_bg             = Style("background-color: Violet;",            "violet_bg")
    wheat_bg              = Style("background-color: Wheat;",             "wheat_bg")
    white_bg              = Style("background-color: White;",             "white_bg")
    white_smoke_bg        = Style("background-color: WhiteSmoke;",        "white_smoke_bg")
    yellow_bg             = Style("background-color: Yellow;",            "yellow_bg")
    yellow_green_bg       = Style("background-color: YellowGreen;",       "yellow_green_bg")


class Paddings:

    @staticmethod
    def size(*sizes: Union[str, int], style_id: Optional[str] = None):
        """
        Creates a padding style with specified sizes, supporting 1-4 values as per CSS convention:
        - 1 value: Applies to all sides.
        - 2 values: top-bottom | left-right.
        - 3 values: top | left-right | bottom.
        - 4 values: top | right | bottom | left.

        :param sizes: Up to 4 values representing padding sizes (int value defaults to em)
        :param style_id: An optional identifier for global theme lookups.
        :return: Style object with the appropriate padding CSS property.
        """
        # Convert integers to em-based strings
        converted_sizes = []
        for size in sizes[:4]:
            if isinstance(size, int):
                size = f"{size}pt"
            converted_sizes.append(str(size))

        padding_value = " ".join(converted_sizes)

        # Derive a default style_id if none is provided
        if not style_id:
            style_id = f"padding_{padding_value.replace(' ', '_')}"

        return Style(f"padding: {padding_value};", style_id)
    
    # Padding (pt)
    Giant_padding   = Style("padding: 96pt;",  "Giant_padding")
    """96pt"""
    giant_padding   = Style("padding: 84pt;",  "giant_padding")
    """84pt"""
    Huge_padding    = Style("padding: 72pt;",  "Huge_padding")
    """72pt"""
    huge_padding    = Style("padding: 60pt;",  "huge_padding")
    """60pt"""
    LARGE_padding   = Style("padding: 48pt;",  "LARGE_padding")
    """48pt"""
    Large_padding   = Style("padding: 36pt;",  "Large_padding")
    """36pt"""
    large_padding   = Style("padding: 24pt;",  "large_padding")
    """24pt"""
    big_padding     = Style("padding: 18pt;",  "big_padding")
    """18pt"""
    medium_padding  = Style("padding: 12pt;",  "medium_padding")
    """12pt"""
    little_padding  = Style("padding: 9pt;",   "little_padding")
    """9pt"""
    small_padding   = Style("padding: 6pt;",   "small_padding")
    """6pt"""
    tiny_padding    = Style("padding: 3pt;",   "tiny_padding")
    """3pt"""
    none_padding    = Style("padding: 0pt;",   "none_padding")
    """0pt"""

    # Padding (em)
    Giant_em_padding   = Style("padding: 8em;",   "Giant_em_padding")
    """8em"""
    giant_em_padding   = Style("padding: 7em;",   "giant_em_padding")
    """7em"""
    Huge_em_padding    = Style("padding: 6em;",   "Huge_em_padding")
    """6em"""
    huge_em_padding    = Style("padding: 5em;",   "huge_em_padding")
    """5em"""
    LARGE_em_padding   = Style("padding: 4em;",   "LARGE_em_padding")
    """4em"""
    Large_em_padding   = Style("padding: 3em;",   "Large_em_padding")
    """3em"""
    large_em_padding   = Style("padding: 2em;",   "large_em_padding")
    """2em"""
    big_em_padding     = Style("padding: 1.5em;", "big_em_padding")
    """1.5em"""
    medium_em_padding  = Style("padding: 1em;",   "medium_em_padding")
    """1em"""
    little_em_padding  = Style("padding: 0.75em;","little_em_padding")
    """0.75em"""
    small_em_padding   = Style("padding: 0.5em;", "small_em_padding")
    """0.5em"""
    tiny_em_padding    = Style("padding: 0.25em;","tiny_em_padding")
    """0.25em"""
    none_em_padding    = Style("padding: 0em;",   "none_em_padding")
    """0em"""
    
class Margins:

    @staticmethod
    def size(*sizes: Union[str, int], style_id: Optional[str] = None):
        """
        Creates a margin style with specified sizes, supporting 1-4 values as per CSS convention:
        - 1 value: Applies to all sides.
        - 2 values: top-bottom | left-right.
        - 3 values: top | left-right | bottom.
        - 4 values: top | right | bottom | left.

        :param sizes: Up to 4 values representing margin sizes (int value defaults to em)
        :param style_id: An optional identifier for global theme lookups.
        :return: Style object with the appropriate margin CSS property.
        """
        # Convert integers to em-based strings
        converted_sizes = []
        for size in sizes[:4]:
            if isinstance(size, int):
                size = f"{size}pt"
            converted_sizes.append(str(size))

        margin_value = " ".join(converted_sizes)

        # Derive a default style_id if none is provided
        if not style_id:
            style_id = f"margin_{margin_value.replace(' ', '_')}"

        return Style(f"margin: {margin_value};", style_id)

    # Margin (pt)
    Giant_margin    = Style("margin: 96pt;",  "Giant_margin")
    """96pt"""
    giant_margin    = Style("margin: 84pt;",  "giant_margin")
    """84pt"""
    Huge_margin     = Style("margin: 72pt;",  "Huge_margin")
    """72pt"""
    huge_margin     = Style("margin: 60pt;",  "huge_margin")
    """60pt"""
    LARGE_margin    = Style("margin: 48pt;",  "LARGE_margin")
    """48pt"""
    Large_margin    = Style("margin: 36pt;",  "Large_margin")
    """36pt"""
    large_margin    = Style("margin: 24pt;",  "large_margin")
    """24pt"""
    big_margin      = Style("margin: 18pt;",  "big_margin")
    """18pt"""
    medium_margin   = Style("margin: 12pt;",  "medium_margin")
    """12pt"""
    little_margin   = Style("margin: 9pt;",   "little_margin")
    """9pt"""
    small_margin    = Style("margin: 6pt;",   "small_margin")
    """6pt"""
    tiny_margin     = Style("margin: 3pt;",   "tiny_margin")
    """3pt"""
    none_margin     = Style("margin: 0pt;",   "none_margin")
    """0pt"""
    
    # Special Margin
    auto_margin     = Style("margin: auto;",  "auto_margin")
    
    # Margin (em)
    Giant_em_margin    = Style("margin: 8em;",   "Giant_em_margin")
    """8em"""
    giant_em_margin    = Style("margin: 7em;",   "giant_em_margin")
    """7em"""
    Huge_em_margin     = Style("margin: 6em;",   "Huge_em_margin")
    """6em"""
    huge_em_margin     = Style("margin: 5em;",   "huge_em_margin")
    """5em"""
    LARGE_em_margin    = Style("margin: 4em;",   "LARGE_em_margin")
    """4em"""
    Large_em_margin    = Style("margin: 3em;",   "Large_em_margin")
    """3em"""
    large_em_margin    = Style("margin: 2em;",   "large_em_margin")
    """2em"""
    big_em_margin      = Style("margin: 1.5em;","big_em_margin")
    """1.5em"""
    medium_em_margin   = Style("margin: 1em;",   "medium_em_margin")
    """1em"""
    little_em_margin   = Style("margin: 0.75em;","little_em_margin")
    """0.75em"""
    small_em_margin    = Style("margin: 0.5em;", "small_em_margin")
    """0.5em"""
    tiny_em_margin     = Style("margin: 0.25em;","tiny_em_margin")
    """0.25em"""
    none_em_margin     = Style("margin: 0em;",   "none_em_margin")
    """0em"""



class Layouts:
    # Layout styles
    fix_ratio             = Style("display: block;",               "fix_ratio")
    inline                = Style("display: inline-block;",        "inline")
    col_layout            = Style("display: flex; flex-direction: column;", "col_layout")
    row_layout            = Style("display: flex; flex-direction: row;",    "row_layout")
    vertical_center_layout= Style("display: flex; align-items: center; justify-content: center;", "vertical_center_layout")
    table_layout          = Style("table-layout: fixed; width: 100%;",      "table_layout")


class ContainerSizes:
    # Width and height
    width_full = Style("width: 100%;", "width_full")
    width_half = Style("width: 50%;",  "width_half")
    width_auto = Style("width: auto;", "width_auto")

    height_full = Style("height: 100%;", "height_full")
    height_half = Style("height: 50%;",  "height_half")
    height_auto = Style("height: auto;", "height_auto")


class Borders:

    @staticmethod
    def size(*sizes: Union[str, int], style_id: Optional[str] = None):
        """
        Creates a border width style with specified sizes, supporting 1-4 values:
        - 1 value: Applies to all sides.
        - 2 values: top-bottom | left-right.
        - 3 values: top | left-right | bottom.
        - 4 values: top | right | bottom | left.
        
        If style_id is provided, it will be used for global theme lookups.
        Otherwise, one is auto-generated.
        """
        # Convert integer sizes to em-based strings
        converted_sizes = []
        for size in sizes[:4]:
            if isinstance(size, int):
                size = f"{size}pt"
            converted_sizes.append(str(size))

        border_width_value = " ".join(converted_sizes)
        if not style_id:
            clean_id = border_width_value.replace(" ", "_")
            style_id = f"border_size_{clean_id}"

        return Style(f"border-width: {border_width_value};", style_id)

    # Border widths
    thin_border   = Style("border-width: thin;",   "thin_border")
    medium_border = Style("border-width: medium;", "medium_border")
    thick_border  = Style("border-width: thick;",  "thick_border")

    # Border style
    solid_border  = Style("border-style: solid;",  "solid_border")
    dotted_border = Style("border-style: dotted;", "dotted_border")
    dashed_border = Style("border-style: dashed;", "dashed_border")
    double_border = Style("border-style: double;", "double_border")
    groove_border = Style("border-style: groove;", "groove_border")
    ridge_border  = Style("border-style: ridge;",  "ridge_border")
    inset_border  = Style("border-style: inset;",  "inset_border")
    outset_border = Style("border-style: outset;", "outset_border")
    none_border   = Style("border-style: none;",   "none_border")
    hidden_border = Style("border-style: hidden;", "hidden_border")

    @staticmethod
    def color(color: Union[Style, str], style_id: Optional[str] = None):
        """
        Converts a text color Style object or string into a border color Style.
        If the input is a Style object with 'color:' in it, the color is extracted.
        
        An optional style_id can be provided for the global theme dictionary. 
        Otherwise, one is auto-generated.
        """
        if isinstance(color, Style):
            color_str = str(color)  # theme-based CSS
            if "color:" in color_str:
                # Extract color name/value from 'color: ...;'
                color = color_str.split("color:")[1].split(";")[0].strip()

        if not style_id:
            # Replace disallowed chars in color
            clean_id = str(color).replace(" ", "_").replace(":", "").replace(";", "")
            style_id = f"border_color_{clean_id}"

        return Style(f"border-color: {color};", style_id)

    table_border = Style("""
        border: 1px solid rgba(0, 0, 0, 1);
        border-collapse: collapse;
        opacity: 1;
    """.strip(), "table_border")


class Flex:
    # Flexbox layouts
    flex               = Style("display: flex;", "flex")
    row_flex           = Style("display: flex; flex-direction: row;",    "row_flex")
    col_flex           = Style("display: flex; flex-direction: column;", "col_flex")
    wrap_flex          = Style("display: flex; flex-wrap: wrap;",        "wrap_flex")

    space_between_justify = Style("justify-content: space-between;", "space_between_justify")
    center_justify        = Style("justify-content: center;",        "center_justify")
    center_align_items    = Style("align-items: center;",            "center_align_items")

    # Instead of center_flex = flex + center_align_items, use Style.create(...)
    # to give it a distinct style_id: "center_flex"
    center_flex = Style.create(flex + center_align_items, "center_flex")


class Visibility:
    # Display and visibility
    hidden = Style("display: none;",    "hidden")
    """block doesn't take up space in page"""

    visible = Style("visibility: visible;", "visible")

    invisible = Style("visibility: hidden;", "invisible")
    """block takes up space in page"""


class ListStyles:
    # Example: we have a ListStyle with special symbols. Provide a style ID if needed.
    g_docs = ListStyle(symbols=["❖", "➢", "◼", "●", "◆", "➢", "◼", "●", "◆", "◆", "◆", "◆", "◆", "◆", "◆", "◆"])
    # For an enumerated style like 'ordered_lowercase', just add an ID
    ordered_lowercase = Style("list-style-type: lower-alpha;", "ordered_lowercase")

class Titles:
    # Titles and Subtitles
    title = Style.create(
        Weights.bold_weight + Sizes.LARGE_size + Alignments.center_align,
        "title"
    )
    subtitle = Style.create(
        Weights.bold_weight + Sizes.large_size + Alignments.center_align,
        "subtitle"
    )

class Text:
    decors = Decors
    weights = Weights
    alignments = Alignments
    colors = Colors
    bg_colors = BackgroundColors
    sizes = Sizes
    fonts = Fonts
    titles = Titles

class Positions:
    # CSS position properties
    initial  = Style("position: initial;",  "initial")
    static   = Style("position: static;",   "static")
    relative = Style("position: relative;", "relative")
    absolute = Style("position: absolute;", "absolute")
    fixed    = Style("position: fixed;",    "fixed")
    sticky   = Style("position: sticky;",   "sticky")

    @staticmethod
    def top(offset: Union[str, int], style_id: Optional[str] = None):
        """
        Returns a Style with 'top: <offset>;', defaulting to px if offset is an int.
        If style_id is None, auto-generates one.
        """
        if isinstance(offset, int):
            offset = f"{offset}px"
        if not style_id:
            style_id = f"top_{offset}"
        return Style(f"top: {offset};", style_id)

    @staticmethod
    def bottom(offset: Union[str, int], style_id: Optional[str] = None):
        """
        Returns a Style with 'bottom: <offset>;', defaulting to px if offset is an int.
        If style_id is None, auto-generates one.
        """
        if isinstance(offset, int):
            offset = f"{offset}px"
        if not style_id:
            style_id = f"bottom_{offset}"
        return Style(f"bottom: {offset};", style_id)

    @staticmethod
    def left(offset: Union[str, int], style_id: Optional[str] = None):
        """
        Returns a Style with 'left: <offset>;', defaulting to px if offset is an int.
        If style_id is None, auto-generates one.
        """
        if isinstance(offset, int):
            offset = f"{offset}px"
        if not style_id:
            style_id = f"left_{offset}"
        return Style(f"left: {offset};", style_id)

    @staticmethod
    def right(offset: Union[str, int], style_id: Optional[str] = None):
        """
        Returns a Style with 'right: <offset>;', defaulting to px if offset is an int.
        If style_id is None, auto-generates one.
        """
        if isinstance(offset, int):
            offset = f"{offset}px"
        if not style_id:
            style_id = f"right_{offset}"
        return Style(f"right: {offset};", style_id)


class Container:
    sizes = ContainerSizes
    bg_colors = BackgroundColors
    borders = Borders
    paddings = Paddings
    margins = Margins
    layouts = Layouts
    flex = Flex
    lists = ListStyles
    positions = Positions
           

text = Text  
container = Container
visibility = Visibility  



class StreamTeX_Styles:

    ### Enums #####
    none = Style("", "none")    
    text = Text
    container = Container
    visibility = Visibility

    bold = text.weights.bold_weight
    reset_bold = text.weights.normal_weight
    italic = text.decors.italic_text
    center_txt = text.alignments.center_align


    GIANT = text.sizes.GIANT_size
    """196pt"""
    Giant = text.sizes.Giant_size
    """128pt"""
    giant = text.sizes.giant_size
    """112pt"""
    Huge = text.sizes.Huge_size
    """96pt"""
    huge = text.sizes.huge_size
    """80pt"""
    LARGE = text.sizes.LARGE_size
    """64pt"""
    Large = text.sizes.Large_size
    """48pt"""
    large = text.sizes.large_size
    """32pt"""
    big = text.sizes.big_size
    """24pt"""
    medium = text.sizes.medium_size
    """16pt"""
    little = text.sizes.little_size
    """12pt"""
    small = text.sizes.small_size
    """8pt"""
    tiny = text.sizes.tiny_size
    """4pt"""
        