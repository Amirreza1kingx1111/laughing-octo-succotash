import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-only-change-this-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + os.path.join(BASE_DIR, "instance", "school.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # وقتی سایت واقعاً روی HTTPS قرار گرفت، این را True می‌کنیم.
    SESSION_COOKIE_SECURE = os.environ.get(
        "SESSION_COOKIE_SECURE",
        "0"
    ) == "1"
