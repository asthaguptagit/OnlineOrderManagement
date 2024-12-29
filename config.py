from dotenv import load_dotenv
import os

# This is responsible for loading env variables either locally or from azure (if its set up)
load_dotenv()

# This is config class where we set up our env variables . If doesnt find the value, it falls back to 
# default value. 
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://username:password@localhost:5432/default_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(16))
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', timedelta(minutes=30))
    JWT_REFRESH_TOKEN_EXPIRES = os.getenv('JWT_REFRESH_TOKEN_EXPIRES', timedelta(days=7))
    

    
    
# In case we want load env file as per the env, we cna use code below 
    
# class DevelopmentConfig(Config):
# DEBUG = True

#class ProductionConfig(Config):
#   DEBUG = False
#   SQLALCHEMY_DATABASE_URI = os.getenv(
#      'DATABASE_URL', 'postgresql://username:password@prod_db:5432/prod_user_management'
#   )

# Select configuration based on environment
#ENV = os.getenv('FLASK_ENV', 'development')
#if ENV == 'production':
#   app_config = ProductionConfig()
#else:
#   app_config = DevelopmentConfig()

