from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    pokemon_team = db.relationship('Pokemon', secondary='user_pokemon', lazy='dynamic')
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Pokemon(db.Model):
    name = db.Column(db.String, primary_key=True)
    base_hp = db.Column(db.Integer, nullable=False)
    base_atk = db.Column(db.Integer, nullable=False)
    base_def = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False)
    
    def __init__(self, name, base_hp, base_atk, base_def, image):
        self.name = name
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.image = image
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
class UserPokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_name = db.Column(db.String, db.ForeignKey('pokemon.name'), nullable=False)
    user = db.relationship('User', backref=db.backref('pokemon_caught', lazy=True))
    pokemon = db.relationship('Pokemon', backref=db.backref('caught_by_users', lazy=True))

    def __init__(self, user_id, pokemon_name):
        self.user_id = user_id
        self.pokemon_name = pokemon_name

    def save(self):
        db.session.add(self)
        db.session.commit()