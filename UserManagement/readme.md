 Login Process

Client Request:

The client (browser, mobile app, etc.) sends a POST request to /users/login with the user's email and password in the request body.
Example:
json
Copy code
{
    "email": "user@example.com",
    "password": "mypassword"
}

Server Validation:

The server checks:
If the user exists in the database.
If the provided password matches the hashed password in the database (using check_password).
Token Creation:

If the email and password are valid, the server generates a JWT access token using:

python
Copy code
create_access_token(identity=user.email)
identity: The value stored in the token's payload (commonly email or user_id). This helps identify the user in subsequent requests.

Token Sent to Client:

The generated token is sent back to the client as part of the response:
json
Copy code
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
The client stores this token in:
Local storage
Session storage
Secure HTTP-only cookies (recommended for security).


2. Protected Routes
Client Request:

For any protected endpoint (e.g., /users/profile), the client includes the token in the Authorization header:
makefile
Copy code
Authorization: Bearer <JWT_TOKEN>
Server Validation:

The @jwt_required() decorator automatically:
Decodes the token using the secret key (JWT_SECRET_KEY).
Validates the token's signature and expiration.
Extracts the identity (e.g., email) from the token.
If the token is valid, the request is processed further.
Example:
python
Copy code
from flask_jwt_extended import jwt_required, get_jwt_identity

@main_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    # Get the user's identity from the token
    current_user = get_jwt_identity()
    return jsonify({"email": current_user, "message": "Welcome!"})
3. No Need to Store Tokens on the Server
The JWT is self-contained:

It includes all the necessary information (e.g., identity, claims).
The server does not need to store the token or manage sessions.
Validation:

As long as the JWT is signed with a secure secret key, the server can verify its authenticity.
Flow Recap
Login:
The client authenticates with email and password.
The server generates and sends a JWT token to the client.
Subsequent Requests:
The client sends the token with each request in the Authorization header.
The server validates the token using the @jwt_required() decorator.
Access Granted:
If the token is valid, the server processes the request.



Topics to explore further : 

Handling Invalid Tokens
Tokens can become invalid for several reasons, such as expiration, tampering, or revocation. Here’s how to handle these cases:

Token Revocation
If a user logs out or a token is suspected to be compromised, it should be invalidated. You can implement token revocation by maintaining a list of revoked tokens.

Implementation
Store Revoked Tokens:

Use a database or in-memory cache (e.g., Redis) to store tokens that have been revoked.
Check Token Validity:

Add a custom callback to check if a token is revoked:
python
Copy code
from flask_jwt_extended import JWTManager

jwt = JWTManager(app)

revoked_tokens = set()  # Example using a set (use Redis/DB in production)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload['jti'] in revoked_tokens
Revoke Token on Logout:

When a user logs out, add the token’s unique identifier (jti) to the revoked list:
python
Copy code
from flask_jwt_extended import get_jwt

@main_bp.route('/users/logout', methods=['POST'])
@jwt_required()
def logout_user():
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    return jsonify({'msg': 'Token revoked'}), 200

4. Handling Tampered Tokens
The server validates the token’s signature using the JWT_SECRET_KEY. If the token has been tampered with, the server will reject it automatically with an error message like:
json
Copy code
{
    "msg": "Signature verification failed"
}



Description about .env files : 

'''
Why JWT_SECRET_KEY is Required
Signing and Encryption:

When we generate a JWT, such as an access token (create_access_token(identity=current_user)), it is signed using the JWT_SECRET_KEY.
The JWT_SECRET_KEY is used to create a cryptographic signature on the JWT, ensuring that the token has not been tampered with during transmission.
This signature allows the server to verify the authenticity and integrity of the token by checking if it matches the expected secret key.
Token Validation:

On the server-side, after the client sends the token back (e.g., in the Authorization header), the server will use the same JWT_SECRET_KEY to decode and validate the token.
If the token is tampered with or if the wrong key is used, validation will fail.
Confidentiality:

Although the token itself can be sent over insecure channels, the cryptographic signature ensures that the data within the token is verified and has not been altered.
Process in Detail:
Client Requests:
The client sends a request with an access token in the Authorization header.
Server Verification:
The server uses the JWT_SECRET_KEY to decode and validate the token.
If the signature matches and the token is valid (i.e., not expired and correctly signed), the request is authenticated.
Summary:
JWT_SECRET_KEY is used to sign the JWT tokens.
It ensures that the tokens sent by clients are valid, unaltered, and have not expired.
Without JWT_SECRET_KEY, the server cannot properly verify the authenticity of the JWTs it receives.

SECRET_KEY: Used to secure session data (e.g., cookies), ensuring integrity and preventing unauthorized access.
'''