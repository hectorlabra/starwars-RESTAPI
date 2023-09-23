import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Personaje, Planeta, FavoriteCharacter, FavoritePlanet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'


db.init_app(app)

migrate = Migrate(app, db)

admin = Admin(app, name='hector Admin', template_mode='bootstrap3', url='/admin')

models = [User, Personaje, Planeta, FavoriteCharacter, FavoritePlanet]

for model in models:
    admin.add_view(ModelView(model, db.session, name=f'{model.__name__} Admin'))

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_character_to_favorites(character_id):
    user_id = 1  
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    character = Personaje.query.get(character_id)

    if character is None:
        return jsonify({"message": "Character not found"}), 404

    favorite = FavoriteCharacter(user=user, character=character)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": f"Character with ID {character_id} added to favorites"}), 200

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_character_from_favorites(character_id):
    user_id = 1  
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    favorite = FavoriteCharacter.query.filter_by(user=user, character_id=character_id).first()

    if favorite is None:
        return jsonify({"message": "Character not found in favorites"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": f"Character with ID {character_id} removed from favorites"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorites(planet_id):
    user_id = 1  
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    planet = Planeta.query.get(planet_id)

    if planet is None:
        return jsonify({"message": "Planet not found"}), 404

    favorite = FavoritePlanet(user=user, planet=planet)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": f"Planet with ID {planet_id} added to favorites"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_planet_from_favorites(planet_id):
    user_id = 1  
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    favorite = FavoritePlanet.query.filter_by(user=user, planet_id=planet_id).first()

    if favorite is None:
        return jsonify({"message": "Planet not found in favorites"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": f"Planet with ID {planet_id} removed from favorites"}), 200

if __name__ == "__main__":
    with app.app_context():
        
        db.create_all()
      
    app.run(debug=True)
