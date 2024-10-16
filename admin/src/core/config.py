from os import environ

class Config(object):

    """
        Configuración base
    """

    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):

    """
        Configuración de producción
    """

    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")


class DevelopmentConfig(Config):

    """
        Configuración de desarrollo
    """
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = "zMqOLexUSa8sEK1bNjoF"
    MINIO_SECRET_KEY = "mP4Mq3MvIzbjWYkH27wxulKuvItfvBKBDY5SKZNG"
    MINIO_SECURE = False
    BUCKET_NAME = "grupo06"
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo06"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class TestingConfig(Config):

    """
        Configuración de testeo
    """

    TESTING = True

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
}