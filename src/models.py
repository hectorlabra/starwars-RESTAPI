from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def add_favorite(self, resource):
        self.favorites.append(resource)

    def get_favorites(self):
        return [favorite.name for favorite in self.favorites]


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Favorite {self.name}>'


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Agregar más columnas relacionadas con los recursos si es necesario

    def serialize(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Definir modelos adicionales (Personaje, Planeta, Vehiculo) de manera similar a Resource

# Ejemplo de definición de la clase Personaje


class Personaje(Resource):
    height = db.Column(db.String(10))
    mass = db.Column(db.String(10))
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(10))
    gender = db.Column(db.String(10))

# Ejemplo de definición de la clase Planeta


class Planeta(Resource):
    diameter = db.Column(db.String(10))
    climate = db.Column(db.String(100))
    terrain = db.Column(db.String(100))
    population = db.Column(db.String(20))

# Ejemplo de definición de la clase Vehiculo


class Vehiculo(Resource):
    model = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    cost_in_credits = db.Column(db.String(20))
    length = db.Column(db.String(20))
    crew = db.Column(db.String(10))
    passengers = db.Column(db.String(10))
    vehicle_class = db.Column(db.String(100))
