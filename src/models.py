from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    favorite_characters = db.relationship('FavoriteCharacter', back_populates='user')
    favorite_planets = db.relationship('FavoritePlanet', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'

class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('personaje.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    character = db.relationship('Personaje', back_populates='favorited_by')
    user = db.relationship('User', back_populates='favorite_characters')

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planeta.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    planet = db.relationship('Planeta', back_populates='favorited_by')
    user = db.relationship('User', back_populates='favorite_planets')

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(10))
    mass = db.Column(db.String(10))
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    
    favorited_by = db.relationship('FavoriteCharacter', back_populates='character')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'mass': self.mass,
            'hair_color': self.hair_color,
            'skin_color': self.skin_color,
            'eye_color': self.eye_color,
            'birth_year': self.birth_year,
            'gender': self.gender
        }

class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    diameter = db.Column(db.String(10))
    climate = db.Column(db.String(100))
    terrain = db.Column(db.String(100))
    population = db.Column(db.String(20))

    favorited_by = db.relationship('FavoritePlanet', back_populates='planet')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'diameter': self.diameter,
            'climate': self.climate,
            'terrain': self.terrain,
            'population': self.population
        }
