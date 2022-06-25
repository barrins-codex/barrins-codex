import os


class BaseConfig(object):
    DEBUG = os.environ.get("DEBUG", False)
    TESTING = DEBUG


def configure_app(app):
    app.config.from_object(BaseConfig)
