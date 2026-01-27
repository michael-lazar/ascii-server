"""Tests for mozz models."""

from django.core.files.uploadedfile import SimpleUploadedFile

from ascii.core.sauce import get_sauce_data
from ascii.core.utils import get_project_file
from ascii.mozz.tests.factories import ArtPostFactory


def test_artpost_saves_edited_sauce_data_to_file():
    """Test that editing sauce_data writes it back to the file."""
    # Read a test file with SAUCE metadata
    with open(get_project_file("core/tests/data/clouds.xb"), "rb") as fp:
        original_bytes = fp.read()

    # Create an ArtPost with the file
    file = SimpleUploadedFile("test.xb", original_bytes)
    art_post = ArtPostFactory.create(file=file)

    # Verify initial sauce data
    initial_sauce = art_post.sauce_data
    assert initial_sauce["Title"] == "clouds"
    assert initial_sauce["Author"] == "mozz"

    # Edit the sauce_data (must reassign to trigger dirty field detection)
    updated_sauce = art_post.sauce_data.copy()
    updated_sauce["Title"] = "modified_title"
    updated_sauce["Author"] = "modified_author"
    art_post.sauce_data = updated_sauce
    art_post.save()

    # Read the file back and verify SAUCE was written
    with art_post.file.open("rb") as fp:
        updated_bytes = fp.read()

    reparsed_sauce = get_sauce_data(updated_bytes)
    assert reparsed_sauce is not None
    assert reparsed_sauce["Title"] == "modified_title"
    assert reparsed_sauce["Author"] == "modified_author"


def test_artpost_does_not_save_sauce_data_when_not_dirty():
    """Test that sauce_data is not written if it hasn't changed."""
    # Read a test file with SAUCE metadata
    with open(get_project_file("core/tests/data/clouds.xb"), "rb") as fp:
        original_bytes = fp.read()

    # Create an ArtPost with the file
    file = SimpleUploadedFile("test.xb", original_bytes)
    art_post = ArtPostFactory.create(file=file)

    # Get the file modification time
    initial_modified_time = art_post.file.storage.get_modified_time(art_post.file.name)

    # Save without changing sauce_data
    art_post.title = "New Title"
    art_post.save()

    # Verify the file was not modified
    new_modified_time = art_post.file.storage.get_modified_time(art_post.file.name)
    assert initial_modified_time == new_modified_time
