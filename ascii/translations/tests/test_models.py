import pytest

from ascii.translations.choices import TranslationLanguages
from ascii.translations.clients import GoogleTranslateClient
from ascii.translations.models import Translation

ZH = TranslationLanguages.CHINESE_SIMPLIFIED


def test_get_or_translate_persists_on_success(monkeypatch):
    monkeypatch.setattr(GoogleTranslateClient, "translate", lambda self, text, language: "hello")

    translation = Translation.get_or_translate("你好", ZH)

    assert translation.pk is not None
    assert translation.translated == "hello"
    assert Translation.objects.count() == 1


def test_get_or_translate_does_not_persist_on_failure(monkeypatch):
    def raise_timeout(self, text, language):
        raise ConnectionError("connect timeout")

    monkeypatch.setattr(GoogleTranslateClient, "translate", raise_timeout)

    with pytest.raises(ConnectionError):
        Translation.get_or_translate("你好", ZH)

    assert Translation.objects.count() == 0


def test_get_or_translate_returns_cached_without_api_call(monkeypatch):
    Translation.objects.create(original="你好", language=ZH, translated="cached")

    def raise_unexpected(self, text, language):
        raise AssertionError("API should not be called for cached translations")

    monkeypatch.setattr(GoogleTranslateClient, "translate", raise_unexpected)

    translation = Translation.get_or_translate("你好", ZH)

    assert translation.translated == "cached"
    assert Translation.objects.count() == 1


def test_get_or_translate_retries_stuck_blank_row(monkeypatch):
    stuck = Translation.objects.create(original="你好", language=ZH, translated="")
    monkeypatch.setattr(GoogleTranslateClient, "translate", lambda self, text, language: "hello")

    translation = Translation.get_or_translate("你好", ZH)

    assert translation.pk == stuck.pk
    assert translation.translated == "hello"
    stuck.refresh_from_db()
    assert stuck.translated == "hello"


def test_get_or_translate_skips_api_for_blank_text(monkeypatch):
    def raise_unexpected(self, text, language):
        raise AssertionError("API should not be called for blank text")

    monkeypatch.setattr(GoogleTranslateClient, "translate", raise_unexpected)

    translation = Translation.get_or_translate("\n \n", ZH)

    assert translation.translated == ""
