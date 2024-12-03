from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    liked_recipes = db.relationship('Recipe', secondary='likes', backref=db.backref('liked_by', lazy='dynamic'))

    def __repr__(self):
        return f"<User(username ={self.username})>"

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)    
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Likes', backref='recipe', lazy='dynamic')

    def __repr__(self):
        return f"<Recipe(title={self.title}, category={self.category})>"
    
    def like_count(self):
        return self.likes.count()

class Likes(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
