from ascii.textmode.tests.factories import ArtFileFactory, ArtFileTagFactory


def test_artfile_tag_signals():
    """
    Ensure the signals keep the ArtFileTag.artfile_count field up-to-date.
    """
    artfile1 = ArtFileFactory()
    artfile2 = ArtFileFactory()
    artfile3 = ArtFileFactory()

    tag = ArtFileTagFactory()

    artfile1.tags.add(tag)
    artfile2.tags.add(tag)
    artfile3.tags.set([tag])

    tag.refresh_from_db()
    assert tag.artfile_count == 3

    artfile1.tags.remove(tag)
    tag.refresh_from_db()
    assert tag.artfile_count == 2

    artfile2.tags.clear()
    tag.refresh_from_db()
    assert tag.artfile_count == 1

    artfile3.delete()
    tag.refresh_from_db()
    assert tag.artfile_count == 0
