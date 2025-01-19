from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
from UserManagement.models import db, User, Roles
from datetime import timedelta

main_bp = Blueprint("main", __name__, url_prefix='/api')

@main_bp.route('/users/register', methods = ['POST'] )
def register_user():
    data = request.json
    console.log(data)
    if User.query.filter_by(email = data['email']).first():
        return jsonify({'error' : 'User already exists'}),400
    user = User(email = data['email'],name = data['name'],role = data['role'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'success' : 'User registered successfully'}),201


#The 201 status code is part of the HTTP response status codes and indicates that a resource has been successfully created. 
# It is commonly used when creating new resources via HTTP methods like POST.

@main_bp.route('/users/login', methods = ['POST'])
def user_login():
    data = request.json
    user = User.query.filter_by(email = data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error' : 'email or password is invalid'}),401
    
    # Set token expiration to 15 minutes
    access_token = create_access_token(identity= user.email, expires_delta = timedelta(minutes = 15))
    refresh_token = create_refresh_token(identity= user.email,expires_delta=timedelta(days=30) )
    return jsonify({'token' : access_token, 'refresh_token': refresh_token}),200

'''
1. Token Expiration
JWT tokens are typically given an expiration time to ensure they don’t stay valid indefinitely.

How It Works
When creating a token with create_access_token, you can set an expiration time using the expires_delta parameter

Validation
If a token has expired, the server will automatically reject it when the @jwt_required() decorator is used

Example Workflow
Login:
Client gets an access token (valid for 15 minutes) and a refresh token (valid for 7 days).
Access Protected Route:
Client sends the access token in the header.
Token Expired:
Client sends the refresh token to the /users/refresh endpoint.
Server Issues a New Access Token.
'''

@main_bp.route('/users/refresh', methods = ['POST'])
@jwt_required(refresh=True)
def refresh_user_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity= current_user, expires_delta = timedelta(minutes = 15))
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

@main_bp.route('/users/profile', methods = ['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()
    #print(f"user : {current_user}")
    #user_email = current_user.get('email')
    user = User.query.filter_by(email = current_user).first()
    if not user:
        return jsonify({'error' : 'User not found'}),404
    
    return jsonify(
        {
            'email' : user.email,
            'name' : user.name,
            'role' : user.role,
            'createdAt' : user.created_at
            
        }
    )

@main_bp.route('/user/roles', methods = ['GET'])
@jwt_required()
def get_roles():
    roles = Roles.query.all()
    return jsonify({
        'roles' : [role.name for role in roles]
    })
    
    
    


    
    
    
    
        
    
