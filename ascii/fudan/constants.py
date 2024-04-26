# These are characters that are typically used in ANSI art and should be
# stripped from a BBS screen when trying to extract the plain text for
# translation, etc. Some characters like punctuation marks can be used
# for both text and art, so I'm applying some heuristics here to try to
# come up with a decent middle-ground.
DRAWING_CHARACTERS = {
    # Miscellaneous ASCII / Latin-1 punctuation marks
    *r"()+-/=\_`|~¤§¨°±·×÷",
    # Spacing Modifier Letters
    *(chr(ch) for ch in range(0x02B0, 0x0300)),
    # General Punctuation
    *(chr(ch) for ch in range(0x2000, 0x2070)),
    # Letterlike Symbols
    *(chr(ch) for ch in range(0x2100, 0x214F)),
    # Arrows
    *(chr(ch) for ch in range(0x2190, 0x2200)),
    # Mathematical Operators
    *(chr(ch) for ch in range(0x2200, 0x2300)),
    # Box Drawing
    *(chr(ch) for ch in range(0x2500, 0x2580)),
    # Block Elements
    *(chr(ch) for ch in range(0x2580, 0x25A0)),
    # Geometric Shapes
    *(chr(ch) for ch in range(0x25A0, 0x2600)),
    # Miscellaneous Symbols
    *(chr(ch) for ch in range(0x2600, 0x2700)),
    # Ideographic Description Characters
    *(chr(ch) for ch in range(0x2FF0, 0x3000)),
    # CJK Symbols and Punctuation
    *(chr(ch) for ch in range(0x3000, 0x3040)),
    # CJK Compatibility Forms
    *(chr(ch) for ch in range(0xFE30, 0xFE50)),
    # Halfwidth and Fullwidth Forms
    *(chr(ch) for ch in range(0xFF00, 0xFFF0)),
}
