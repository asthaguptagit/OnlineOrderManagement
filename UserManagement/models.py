from UserManagement import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True, server_default=db.text('NEXT VALUE FOR my_sequence'))
    email = db.Column(db.String(255), nullable = False, unique= True)
    name = db.Column(db.String(255), nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(20), db.ForeignKey("roles.name"))
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    
    def __init__(self, email, name, role):
        self.email = email
        self.name = name
        self.role = role
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
        
    

class Roles(db.Model):
    __tablename__ = "roles"
    name = db.Column(db.String(20), primary_key= True)
    description = db.Column(db.String(255), nullable= False)

