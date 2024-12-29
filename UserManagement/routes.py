from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from UserManagement.models import db, User, Role

main_bp = Blueprint("main", __name__)

@main_bp.route('users/register', methods = ['POST'] )
def register_user():
    data = request.json
    if User.query.filter_by(email = data['email']).first():
        return jsonify({'error' : 'User already exists'}),400
    user = User(data['email'],data['name'],data['role'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'success' : 'User registered successfully'}),201


#The 201 status code is part of the HTTP response status codes and indicates that a resource has been successfully created. 
# It is commonly used when creating new resources via HTTP methods like POST.

@main_bp.route('users/login', methods = ['POST'])
def user_login():
    data = request.json
    user = User.query.filter_by(email = data['email']).first()
    if not user or not user.set_password(data['password']):
        return jsonify({'error' : 'email or password is invalid'}),401
    
    # Set token expiration to 15 minutes
    access_token = create_access_token(identity= user.email, expires_time = timedelta(minutes = 15))
    refresh_token = create_refresh_token(identity= user.email)
    return jsonify({'token' : access_token, 'refresh_token': refresh_token}),200

@main_bp.route('users/refresh', methods = ['POST'])
@jwt_required(refresh=True)
def refresh_user_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity= user.email, expires_delta = timedelta(minutes = 15))
    return jsonify({'token' : new_access_token}),200

'''
How create_access_token Works Internally
When you call create_access_token(identity=current_user):

It creates a JWT token by:
Encoding the identity (which in this case is the user's email or identifier).
Signing the token using the JWT_SECRET_KEY.
Here's a breakdown:

Code Breakdown:
python
Copy code
from flask_jwt_extended import create_access_token

@main_bp.route('/users/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Create JWT access token
    access_token = create_access_token(identity=user.email)
    return jsonify({'access_token': access_token}), 200
How create_access_token Works:
Identity:
In this case, the identity is user.email, but it can be any unique identifier, such as a user ID or username.
Signing:
create_access_token internally handles signing the token with the JWT_SECRET_KEY set in your Flask app configuration.
What create_access_token Does:
It takes the identity and encrypts it using the JWT_SECRET_KEY.
Generates a secure, tamper-proof JWT with a payload that contains metadata (e.g., expiration time, subject) and signs it.
Returns a compact JWT token string.

'''

    
    
    
    
        
    
