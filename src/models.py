from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'  
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }

class Planet(db.Model):
    __tablename__ = 'planet' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(800))
    weather = db.Column(db.String(250))
    population = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "weather": self.weather,
            "population": self.population
        }

class People(db.Model):
    __tablename__ = 'people'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.String(250), nullable=False)
    origin_planet = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "origin_planet": self.origin_planet,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'  
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    character_id = db.Column(db.Integer, db.ForeignKey('people.id'))  
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))  
  
    user = db.relationship('User')
    planet = db.relationship('Planet')
    character = db.relationship('People')

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize() if self.user else None,  
            "character": self.character.serialize() if self.character else None, 
            "planet": self.planet.serialize() if self.planet else None  
        }
