from flask import Flask

from .auth import load_logged_in_user, register_routes as register_auth_routes
from .config import Config
from .database import close_db, init_db
from .weather_routes import register_routes as register_weather_routes
from .tourism_routes import register_routes as register_tourism_routes


def create_app(config=None):
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    @app.before_request
    def load_user():
        load_logged_in_user(app)

    app.teardown_appcontext(close_db)
    register_auth_routes(app)
    register_weather_routes(app)
    register_tourism_routes(app)
    with app.app_context():
        init_db(app)
    return app
