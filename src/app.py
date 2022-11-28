"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Fav_Characters, Fav_Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#***************** USERS *************************

#ENDPOINT GET LOS USUARIOS CREADOS
@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(user.serialize())
    return jsonify(user_list), 200

#ENDPOINT GET UN USUARIO SEGÚN SU ID
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).one()
    user = user.serialize()
    return jsonify(user), 200


#***************** CHARACTERS *************************

#ENDPOINT GET CHARACTERS CREADOS
@app.route('/people', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    characters_list = []
    for character in characters:
        characters_list.append(character.serialize())
    return jsonify(characters_list), 200

#ENDPOINT GET UN CHARACTER SEGÚN SU ID
@app.route('/people/<int:id>', methods=['GET'])
def get_character(id):
    character = Characters.query.filter_by(id=id).one()
    character = character.serialize()
    return jsonify(character), 200


#ENDPOINT PARA CREAR UN CHARACTER (SIN USAR EL MENU DADO) / XEJ CON ESTO PUEDO AÑADIR UN CHARACTER DESDE POSTMAN
@app.route('/people', methods=['POST'])
def create_character():
    data = request.data
    data = json.loads(data)
    character_new = Characters(
        name = data["name"],
        birthday_year = data["birthday_year"],
        gender = data["gender"],
        height = data["height"],
        skin_color = data["skin_color"],
        eye_color = data["eye_color"])
    db.session.add(character_new)
    db.session.commit()
    response_body = {
        "msg": "Añadido un personaje"
    }
    return jsonify(response_body), 200

#ENDPOINT PARA MODIFICAR UN CHARACTER (SIN USAR EL MENU DADO) 
@app.route('/people/<int:id>', methods=['PUT'])
def modify_character(id):
    data = request.data
    data = json.loads(data)
    character_modified = Characters.query.filter_by(id=id).one()
    character_modified.skin_color = data["skin_color"]
    character_modified.verified = True
    db.session.commit()
    response_body = {
        "msg": "Personaje modificado"
    }
    return jsonify(response_body), 200


#ENDPOINT PARA DELETE UN CHARACTER (SIN USAR EL MENU DADO) 
@app.route('/people/<int:id>', methods=['DELETE'])
def delete_character(id):
    character_deleted = Characters.query.filter_by(id=id).one()
    db.session.delete(character_deleted)
    db.session.commit()
    response_body = {
        "msg": "Personaje borrado"
    }
    return jsonify(response_body), 200



#***************** PLANETS *************************


#ENDPOINT GET PLANETS CREADOS
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_list = []
    for planet in planets:
        planets_list.append(planet.serialize())
    return jsonify(planets_list), 200

#ENDPOINT GET UN PLANET SEGÚN SU ID
@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planets.query.filter_by(id=id).one()
    planet = planet.serialize()
    return jsonify(planet), 200


#ENDPOINT PARA CREAR UN PLANET (SIN USAR EL MENU DADO) 
@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.data
    data = json.loads(data)
    planet_new = Planets(
        name = data["name"],
        diameter = data["diameter"],
        rotation_period = data["rotation_period"],
        orbital_period = data["orbital_period"])
    db.session.add(planet_new)
    db.session.commit()
    response_body = {
        "msg": "Añadido un planet"
    }
    return jsonify(response_body), 200

#ENDPOINT PARA MODIFICAR UN PLANET (SIN USAR EL MENU DADO) 
@app.route('/planets/<int:id>', methods=['PUT'])
def modify_planets(id):
    data = request.data
    data = json.loads(data)
    planet_modified = Planets.query.filter_by(id=id).one()
    planet_modified.diameter = data["diameter"]
    planet_modified.verified = True
    db.session.commit()
    response_body = {
        "msg": "Planet modificado"
    }
    return jsonify(response_body), 200

#ENDPOINT PARA DELETE UN PLANET (SIN USAR EL MENU DADO) 
@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet_deleted = Planets.query.filter_by(id=id).one()
    db.session.delete(planet_deleted)
    db.session.commit()
    response_body = {
        "msg": "Planet borrado"
    }
    return jsonify(response_body), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
