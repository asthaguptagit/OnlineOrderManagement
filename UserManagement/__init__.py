#Flask: Core library for creating Flask web applications.
#SQLAlchemy: ORM (Object Relational Mapper) library to interact with relational databases using Python objects.
#Migrate: Extension that manages database migrations (e.g., schema changes) using Alembic in conjunction with SQLAlchemy.
#JWTManager: Library for handling JSON Web Tokens (JWTs), used for user authentication and authorization.


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager,verify_jwt_in_request


#db = SQLAlchemy(): Creates a SQLAlchemy object for database interaction.
#migrate = Migrate(): Creates a Migrate object for handling database migrations.
#jwt = JWTManager(): Creates a JWTManager object to handle JWT-related tasks like token

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

#This is a factory function that creates and configures a Flask application instance. 
# It’s commonly used in larger applications to allow flexibility and reuse of the app creation logic.
#app = Flask(__name__): Instantiates a Flask application.
#__name__: The name of the current module. It helps Flask locate resources such as templates and static files.
#app.config.from_object('config.Config'): Loads configuration settings from a Config class defined in a config.py module. This may include settings like the database URI, secret keys, and JWT configurations.


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    from UserManagement.routes import main_bp
    app.register_blueprint(main_bp)
    
    @app.before_request
    def check_token_expiry():
        try:
            verify_jwt_identity()
        except Exception as e :
            if "Token Has Expired" in str(e):
                return jsonify({'error': 'Token expired, please refresh'}), 401

    return app
    
#db.init_app(app): Binds the SQLAlchemy instance to the Flask app, enabling database interactions.
#migrate.init_app(app, db): Binds the Migrate instance to both the app and the database, enabling database migration commands such as flask db migrate.
#jwt.init_app(app): Binds the JWTManager instance to the app, enabling JWT-based authentication functionalities.
#By calling init_app, extensions are configured for use with the app instance.



#from app.routes import main_bp: Imports a blueprint named main_bp from the app.routes module.
#app.register_blueprint(main_bp): Registers the blueprint with the Flask application.
#Blueprints: A way to organize application routes, models, and other logic into smaller, modular components. This promotes a cleaner and more maintainable codebase.








    