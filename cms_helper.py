#!/usr/bin/env python

from tempfile import mkdtemp

HELPER_SETTINGS = dict(
    ROOT_URLCONF="tests.example_app.urls",
    INSTALLED_APPS=[
        "daphne",
        "channels",
        "sekizai",
        "meta",
        "tests.example_app",
    ],
    LANGUAGES=(
        ("en", "English"),
        ("fr", "French"),
        ("it", "Italiano"),
    ),
    PARLER_LANGUAGES={
        1: (
            {"code": "en"},
            {"code": "it"},
            {"code": "fr"},
        ),
        2: ({"code": "en"},),
        "default": {
            "fallbacks": ["en"],
            "hide_untranslated": False,
        },
    },
    META_USE_SITES=True,
    FILE_UPLOAD_TEMP_DIR=mkdtemp(),
    META_SITE_PROTOCOL="http",
    ASGI_APPLICATION="tests.example_app.routing.application",
    TEST_RUNNER="app_helper.pytest_runner.PytestTestRunner",
    CHANNEL_LAYERS={
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("localhost", 6379)],
            },
        },
    },
)


def run():
    from app_helper import runner

    runner.run("knocker")


def setup():
    import sys

    from app_helper import runner

    runner.setup("knocker", sys.modules[__name__], use_cms=False)


if __name__ == "__main__":
    run()

if __name__ == "cms_helper":
    # this is needed to run cms_helper in pycharm
    setup()
