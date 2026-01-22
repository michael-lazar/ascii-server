"""Tests for SAUCE encoder/decoder."""

from ascii.core.sauce import get_sauce_data, write_sauce_data
from ascii.core.utils import get_project_file


def test_get_sauce_data_from_file():
    """Test parsing existing SAUCE metadata from clouds.xb file."""
    with open(get_project_file("core/tests/data/clouds.xb"), "rb") as fp:
        file_bytes = fp.read()

    sauce = get_sauce_data(file_bytes)

    assert sauce is not None
    assert sauce["Title"] == "clouds"
    assert sauce["Author"] == "mozz"
    assert sauce["Group"] == "mistigris"
    assert sauce["Date"] == "20260118"
    assert sauce["Comments"] == "blah\nblah\nblah"


def test_get_sauce_data_round_trip():
    """Test writing SAUCE metadata preserves the original bytes."""
    with open(get_project_file("core/tests/data/clouds.xb"), "rb") as fp:
        file_bytes = fp.read()

    sauce = get_sauce_data(file_bytes)
    assert sauce is not None

    new_bytes = write_sauce_data(file_bytes, sauce)

    assert file_bytes == new_bytes


def test_write_sauce_data_to_bytes():
    """Test writing SAUCE metadata and re-parsing it."""
    with open(get_project_file("core/tests/data/clouds.xb"), "rb") as fp:
        file_bytes = fp.read()

    original_sauce = get_sauce_data(file_bytes)
    assert original_sauce is not None

    modified_sauce = original_sauce.copy()
    modified_sauce["Title"] = "test"
    modified_sauce["Author"] = "test_author"
    modified_sauce["Group"] = "test_group"
    modified_sauce["Date"] = "20260101"
    modified_sauce["Comments"] = "This is a test comment"

    new_bytes = write_sauce_data(file_bytes, modified_sauce)

    reparsed_sauce = get_sauce_data(new_bytes)

    assert reparsed_sauce is not None
    assert reparsed_sauce["Title"] == "test"
    assert reparsed_sauce["Author"] == "test_author"
    assert reparsed_sauce["Group"] == "test_group"
    assert reparsed_sauce["Date"] == "20260101"
    assert reparsed_sauce["Comments"] == "This is a test comment"


def test_get_sauce_data_returns_none():
    """Test that get_sauce_data returns None when no SAUCE is present."""
    test_bytes = b"This is just some random data without SAUCE metadata."

    sauce = get_sauce_data(test_bytes)
    assert sauce is None
