import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    DATABASE = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "clima.sqlite3"))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
