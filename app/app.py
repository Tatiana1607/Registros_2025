from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__) # Se crea una instancia de la app Flask
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import hallazgos, incidentes # Importa las rutas de los módulos
    app.register_blueprint(hallazgos.bp)
    app.register_blueprint(incidentes.bp)

    return app # Devuelve la aplicación configurada
    