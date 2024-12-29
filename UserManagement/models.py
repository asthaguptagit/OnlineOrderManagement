from UserManagement import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable = False, unique= True)
    name = db.Column(db.String(255), nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(20), db.ForeignKey("roles.name"))
    created_at = db.Column(db.dateTime, server_default = db.func.now())
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
        
    

class Roles(db.model):
    __tablename__ = "roles"
    
    name = db.Column(db.String(20), primary_key= True)
    description = db.Column(db.String(255), nullable= False)

