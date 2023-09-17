import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Personaje, Planeta, Vehiculo, Favorite

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'

# Inicializar la base de datos
db.init_app(app)

# Configurar Flask-Migrate
migrate = Migrate(app, db)

# Configurar Flask-Admin
admin = Admin(app, name='hector Admin', template_mode='bootstrap3', url='/admin')

# Agregar vistas de modelos a Flask-Admin
models = [User, Personaje, Planeta, Vehiculo, Favorite]

for model in models:
    admin.add_view(ModelView(model, db.session, name=f'{model.__name__} Admin'))

# Rutas para obtener recursos
@app.route('/<resource_name>', methods=['GET'])
def get_resources(resource_name):
    resource_model = globals().get(resource_name, None)
    
    if resource_model is None:
        return jsonify({"message": f"{resource_name} not found"}), 404

    resources = resource_model.query.all()
    return jsonify([resource.serialize() for resource in resources]), 200

@app.route('/<resource_name>/<int:id>', methods=['GET'])
def get_resource_by_id(resource_name, id):
    resource_model = globals().get(resource_name, None)
    
    if resource_model is None:
        return jsonify({"message": f"{resource_name} not found"}), 404

    resource = resource_model.query.get(id)
    if not resource:
        return jsonify({"message": f"{resource_name} not found"}), 404

    return jsonify(resource.serialize())

# Rutas para agregar recursos a favoritos
@app.route('/favorite/<resource_name>/<int:resource_id>', methods=['POST'])
def add_resource_to_favorites(resource_name, resource_id):
    user_id = 1
    user = User.query.get(user_id)
    
    if user is None:
        return jsonify({"message": "User not found"}), 404

    resource_model = globals().get(resource_name, None)
    
    if resource_model is None:
        return jsonify({"message": f"{resource_name} not found"}), 404

    resource = resource_model.query.get(resource_id)
    
    if resource is None:
        return jsonify({"message": f"{resource_name} not found"}), 404

    user.add_favorite(resource)
    db.session.commit()

    return jsonify({"message": f"{resource_name.capitalize()} with ID {resource_id} added to favorites"}), 200

# Rutas para quitar recursos de favoritos
@app.route('/favorite/<resource_name>/<int:id>', methods=['DELETE'])
def remove_resource_from_favorites(resource_name, id):
    user_id = 1
    user = User.query.get(user_id)
    
    if user is None:
        return jsonify({"message": "User not found"}), 404

    resource_model = globals().get(resource_name, None)
    
    if resource_model is None:
        return jsonify({"message": f"{resource_name} not found"}), 404

    resource = resource_model.query.get(id)
    
    if resource is None:
        return jsonify({"message": f"{resource_name} not found"}), 404

    user.remove_favorite(resource)
    db.session.commit()

    return jsonify({"message": f"{resource_name.capitalize()} with ID {id} removed from favorites"}), 200

if __name__ == "__main__":
    with app.app_context():
        # Crear las tablas si no existen
        db.create_all()
      
    app.run(debug=True)
