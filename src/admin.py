# admin.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Personaje, Planeta, Vehiculo, Favorite

def setup_admin(app):
    # Configurar Flask-Admin y agregar tus modelos
    admin = Admin(
        app,
        name='4Geeks Admin',
        template_mode='bootstrap3',
        url='/admin'
    )
    
    models_to_view = [User, Personaje, Planeta, Vehiculo, Favorite]
    
    for model in models_to_view:
        admin.add_view(ModelView(model, db.session, name=f'{model.__name__} Admin'))
