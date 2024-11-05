from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SeasonalFlavor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(80), nullable=False, unique=True)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(80), nullable=False, unique=True)
    stock = db.Column(db.Integer, nullable=False)

class CustomerSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    flavor = db.Column(db.String(80), nullable=False)
    allergy_concerns = db.Column(db.String(200))