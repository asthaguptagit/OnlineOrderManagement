from UserManagement import create_app, db
from UserManagement.models import Roles

app = create_app()

with app.app_context():
    roles = ['Admin', 'User']
    for role_name in roles :
        if not Roles.query.filter_by(name = role_name).first():
            role = Roles(name = role_name, description = f"{role_name} role")
            db.session.add(role)
    db.session.commit() 

'''
with app.app_context():
    roles = ['Admin', 'User']
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            role = Role(name=role_name, description=f"{role_name} role")
            db.session.add(role)
    db.session.commit()
Breakdown:
with app.app_context():

This creates a temporary context for the Flask application.
This is necessary because database operations require an active Flask application context, which is not available in regular Python scripts or modules.
Within this context, all Flask extensions, like db, are accessible.
roles = ['Admin', 'User']

This defines a list of roles to seed into the database.
for role_name in roles:

Iterates over the list of roles (Admin and User in this case).
if not Role.query.filter_by(name=role_name).first():

Checks if a role with the specified name already exists in the Role table.
Role.query.filter_by(name=role_name).first():
Queries the Role model for a role with the given name.
If no role with that name exists, it returns None.
role = Role(name=role_name, description=f"{role_name} role")

If the role does not exist, a new Role object is created with the given name and a description.
db.session.add(role)

Adds the newly created Role object to the session, so that it can be persisted in the database.
db.session.commit()

Commits the transaction to the database, effectively saving the new roles to the database.
Flow:
The application context ensures that the Flask app has a consistent state.
Each role is checked in the database to avoid duplicates.
New roles are created and added to the session only if they do not exist.
Finally, the session is committed, making the changes permanent in the database.
'''