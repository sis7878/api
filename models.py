from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False, index=True)  

    def __repr__(self):
        return f'<Pizza {self.name}>'
