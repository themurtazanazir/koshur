from fontTools.ttLib import TTFont


def check_text_glyphs(text, font_path):
    """
    Check if all glyphs in the text are available in the font.

    Args:
        text (str): Text to check
        font_path (str): Path to the font file

    Returns:
        tuple: (bool, list) - (True if all glyphs present, list of missing characters)
    """
    # Load the font using fontTools
    tt_font = TTFont(font_path)

    # Get the character map
    cmap = tt_font.getBestCmap()

    # Check each character
    missing_chars = []
    for char in text:
        # Convert character to Unicode code point
        code_point = ord(char)

        # Check if the code point exists in the font's character map
        if code_point not in cmap:
            missing_chars.append(char)

    return len(missing_chars) == 0, missing_chars