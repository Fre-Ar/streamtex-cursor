from streamtex.styles import Style, Text, Container, StreamTeX_Styles

class ColorsCustom:
    """Custom colors defined multiple times."""
    denim_blue = Style("color: #1155cc;", "denim_blue")
    lilac = Style("color: #8b5cf6;", "lilac")


class TitleStyles:
    """Title styl4es"""
    table_of_contents = Style.create(
        ColorsCustom.lilac + Text.weights.bold_weight + Text.sizes.large_size + Text.alignments.center_align,
        "callout_title"
    )

class ProjectStyles:
    """Aggregated access point for StreamTeX."""
    colors = ColorsCustom
    titles = TitleStyles


class Styles(StreamTeX_Styles):
    project = ProjectStyles

