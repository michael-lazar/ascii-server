from ascii.core.sauce import get_sauce_data
from ascii.core.utils import get_project_file
from ascii.textmode.choices import AspectRatio, DataType, FileType, LetterSpacing
from ascii.textmode.sauce import Sauce


def test_build_sauce():
    sauce = Sauce(
        {
            "Id": "SAUCE",
            "Version": 0,
            "Title": "fire #40 members",
            "Author": "nail",
            "Group": "fire",
            "Date": 20240707,
            "Filesize": 16851,
            "Datatype": 1,
            "Filetype": 1,
            "Tinfo1": 80,
            "Tinfo2": 149,
            "Tinfo3": 0,
            "Tinfo4": 0,
            "Tflags": 20,
            "Tinfos": "IBM VGA",
            "Comments": "",
            "ansiflags": {
                "blink": 0,
                "ls": 2,
                "ar": 2,
            },
        }
    )

    assert sauce.title == "fire #40 members"
    assert sauce.author == "nail"
    assert sauce.group == "fire"
    assert sauce.comments == ""
    assert sauce.date.isoformat() == "2024-07-07"
    assert sauce.datatype == DataType.CHARACTER
    assert sauce.filetype == FileType.ANSI
    assert sauce.pixel_width is None
    assert sauce.pixel_height is None
    assert sauce.pixel_depth is None
    assert sauce.sample_rate is None
    assert sauce.character_width == 80
    assert sauce.number_of_lines == 149
    assert sauce.font_name == "IBM VGA"
    assert sauce.filesize == 16851
    assert sauce.ice_colors is False
    assert sauce.letter_spacing == LetterSpacing.NINE
    assert sauce.aspect_ratio == AspectRatio.SQUARE


def test_sauce_from_file():
    """Test that sauce data from get_sauce_data() is compatible with Sauce() class."""
    with open(get_project_file("core/tests/data/clouds.xb"), "rb") as fp:
        file_bytes = fp.read()

    sauce_data = get_sauce_data(file_bytes)
    assert sauce_data is not None

    sauce = Sauce(sauce_data)

    assert sauce.title == "clouds"
    assert sauce.author == "mozz"
    assert sauce.group == "mistigris"
    assert sauce.date.isoformat() == "2026-01-18"
    assert sauce.comments == "blah\nblah\nblah"
    assert sauce.datatype == DataType.XBIN
    assert sauce.filetype == FileType.XBIN
    assert sauce.font_name == ""
