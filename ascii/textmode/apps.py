from django.apps import AppConfig


class TextmodeAppConfig(AppConfig):
    name = "ascii.textmode"

    def ready(self):
        import ascii.textmode.signals  # noqa: E402, F401
