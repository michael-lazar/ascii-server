"""Tests for SAUCE encoder/decoder."""

from ascii.core.sauce import get_sauce, write_sauce


def test_get_sauce_from_file():
    """Test parsing existing SAUCE metadata from clouds.xb file."""
    with open("ascii/core/tests/data/clouds.xb", "rb") as f:
        file_bytes = f.read()

    sauce = get_sauce(file_bytes)

    assert sauce is not None
    assert sauce["title"] == "clouds"
    assert sauce["author"] == "mozz"
    assert sauce["group"] == "mistigris"
    assert sauce["date"] == "20260118"
    assert sauce["comments"] == "blah\nblah\nblah"


def test_write_sauce_to_bytes():
    """Test writing SAUCE metadata and re-parsing it."""
    with open("ascii/core/tests/data/clouds.xb", "rb") as f:
        file_bytes = f.read()

    original_sauce = get_sauce(file_bytes)
    assert original_sauce is not None

    modified_sauce = original_sauce.copy()
    modified_sauce["title"] = "test"
    modified_sauce["author"] = "test_author"
    modified_sauce["group"] = "test_group"
    modified_sauce["date"] = "20260101"
    modified_sauce["comments"] = "This is a test comment"

    new_bytes = write_sauce(file_bytes, modified_sauce)

    reparsed_sauce = get_sauce(new_bytes)

    assert reparsed_sauce is not None
    assert reparsed_sauce["title"] == "test"
    assert reparsed_sauce["author"] == "test_author"
    assert reparsed_sauce["group"] == "test_group"
    assert reparsed_sauce["date"] == "20260101"
    assert reparsed_sauce["comments"] == "This is a test comment"


def test_get_sauce_returns_none():
    """Test that get_sauce returns None when no SAUCE is present."""
    test_bytes = b"This is just some random data without SAUCE metadata."

    sauce = get_sauce(test_bytes)

    assert sauce is None
