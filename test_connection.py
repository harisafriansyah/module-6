from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.hkyvdzyrfxbsscvufrvb:kYpXqQJK8rzXMGVA@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

try:
    with app.app_context():
        # Create a connection from the engine and execute a query
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print("Connection successful, result:", result.scalar())
except Exception as e:
    print(f"Error: {e}")
