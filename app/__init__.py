from flask import Flask, Blueprint
from config import Config
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)

    with app.app_context():

        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        # Import Dash application
        from app.dash import dash_example
        app = dash_example.Add_Dash(app)

        return app


