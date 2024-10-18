import os
import struct

from django.core.management.base import BaseCommand, CommandError
from PIL import Image


class Command(BaseCommand):
    help = "Parse font data from an XBIN file and save it in VGA format."

    def add_arguments(self, parser):
        parser.add_argument("input_file", type=str, help="Path to the input XBIN file")

    def handle(self, *args, **options):
        input_file = options["input_file"]
        if not os.path.exists(input_file):
            raise CommandError(f"File '{input_file}' does not exist.")

        try:
            self.read_xbin_font(input_file)
        except ValueError as e:
            raise CommandError(str(e)) from e

    def read_xbin_font(self, input_file):
        with open(input_file, "rb") as file:
            # Read header (11 bytes)
            header = file.read(11)
            if len(header) < 11:
                raise ValueError("Invalid XBIN file: Header is too short.")

            # Parse header fields
            id_str, eof_char, width, height, font_size, flags = struct.unpack("<4sBHHBB", header)

            if id_str != b"XBIN":
                raise ValueError("Not an XBIN file.")

            # Check if font is present in flags (bit 1 in flags)
            has_palette = flags & 0b00000001
            has_font = flags & 0b00000010
            has_512_chars = flags & 0b00010000

            if not has_font:
                self.stdout.write(self.style.WARNING("No font data in this XBIN file."))
                return

            if has_palette:
                file.read(48)

            # Set character count based on 512Chars flag
            char_count = 512 if has_512_chars else 256

            # Read font data
            font_data_size = font_size * char_count
            font_data = file.read(font_data_size)
            if len(font_data) < font_data_size:
                raise ValueError("Incomplete font data in XBIN file.")

            # Determine output file name based on input basename and font size
            output_file = f"{os.path.splitext(input_file)[0]}.F{font_size}"

            # Save font data to output file
            with open(output_file, "wb") as out:
                out.write(font_data)

            self.stdout.write(
                self.style.SUCCESS(f"Font data saved to {output_file} in VGA format.")
            )

            # Create PNG image for the font
            chars_per_row = 16
            img_width = chars_per_row * 8
            img_height = (char_count // chars_per_row) * font_size

            # Create a new image
            image = Image.new("1", (img_width, img_height))

            # Draw each character into the image
            for i in range(char_count):
                char_x = (i % chars_per_row) * 8
                char_y = (i // chars_per_row) * font_size

                for y in range(font_size):
                    row_data = font_data[i * font_size + y]
                    for x in range(8):  # Each row is 8 pixels wide
                        pixel_on = (row_data >> (7 - x)) & 1
                        image.putpixel((char_x + x, char_y + y), 1 if pixel_on else 0)

            # Save the image as a PNG file
            png_output_file = f"{os.path.splitext(input_file)[0]}.png"
            image.save(png_output_file, "PNG")
            self.stdout.write(self.style.SUCCESS(f"Font image saved as {png_output_file}."))
