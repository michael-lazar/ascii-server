def center_pad_ascii_art(
    artwork: str,
    min_width: int = 35,
    min_height: int = 10,
    padding_vertical: int = 1,
    padding_horizontal: int = 5,
):
    # Split the artwork into lines
    lines = artwork.split("\n")

    # Remove trailing white space from each line
    lines = [line.rstrip() for line in lines]

    leading_whitespace = 100
    for line in lines:
        leading_whitespace = min(leading_whitespace, len(line) - len(line.lstrip(" ")))

    lines = [line[leading_whitespace:] for line in lines]

    # Determine the current width and height of the artwork
    current_width = max(len(line) for line in lines)
    current_height = len(lines)

    # Add the horizontal padding to each line of the artwork
    padded_lines = [" " * padding_horizontal + line + " " * padding_horizontal for line in lines]

    # Recalculate the current width after horizontal padding
    current_width = current_width + 2 * padding_horizontal

    # Calculate the additional width and height needed to meet the minimum dimensions
    additional_width = max(0, min_width - current_width)
    additional_height = max(0, min_height - current_height - 2 * padding_vertical)

    # Add the additional width padding to each line of the artwork
    padded_lines = [
        " " * (additional_width // 2) + line + " " * (additional_width // 2)
        for line in padded_lines
    ]

    # Create lines to add above and below the artwork to meet the minimum height
    empty_line = " " * (current_width + additional_width)
    lines_above = [empty_line] * (additional_height // 2 + padding_vertical)
    lines_below = [empty_line] * (additional_height // 2 + padding_vertical)

    # Combine all the lines into the final padded artwork
    padded_artwork = "\n".join(lines_above + padded_lines + lines_below)

    return padded_artwork
