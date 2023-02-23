
class Config(object):
    DEBUG = False
    TESTING = False

    # secret_key can be ngerated with secrets module
    SECRET_KEY = "fasghioywroiwahqoirwh189398t2w"

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "gnsakgbw"

    UPLOADS = "/home/username/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "gnsakgbw"

    UPLOADS = "/home/username/flask_test/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "gnsakgbw"

    UPLOADS = "/home/username/flask_test/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False
