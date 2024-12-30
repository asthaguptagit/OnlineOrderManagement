pip install -r requirements.txt
pip install flask flask-sqlalchemy alembic

flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask db revision --autogenerate -m "Added identity column to id" 

python seed_roles.py
python run.py





