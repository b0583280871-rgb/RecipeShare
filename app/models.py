from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='Reader')
    is_approved_uploader = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # קשר למתכונים
    recipes = db.relationship('Recipe', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recipe(BaseModel):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    title = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)#תמונה מקורית
    variation_paths = db.Column(db.Text, nullable=False)  # JSON של 3 וריאציות
    type = db.Column(db.String(20)) # Dairy, Meat, Parve
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ingredients = db.relationship('IngredientEntry', backref='recipe', lazy=True, cascade="all, delete")
    category = db.Column(db.String(30), nullable=False)
    instructions = db.Column(db.Text)

class IngredientEntry(BaseModel):
    __tablename__ = 'ingredients'
    name = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float)
    unit = db.Column(db.String(20))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)