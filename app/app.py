from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.routes import hallazgos, incidentes
        app.register_blueprint(hallazgos.bp)
        app.register_blueprint(incidentes.bp)
    return app
app = create_app()