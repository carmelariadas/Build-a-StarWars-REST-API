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
    # aqui esta creando un objeto con lo que va recogiendo que le metemos al body de postman?
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


#***************** FAVORITOS USUARIO *************************
#********** CHARACTERS *************

# la parte de la ruta /user/yelid es ficticia pa que parezca que pertenecen a un user segun su id, peor en la siguiente clase vemos la autenticacion
@app.route('/user/<int:id>/fav_characters', methods=['POST'])
# como parametro de la funcion uso la variable de la ruta
def add_fav_character(id):
    id_character = request.json.get("id_character", None)
    # el primer id en el siguiente parentesis es el nombre de la columna id del class Character
    fav_character = Characters.query.filter_by(id=id_character).first()
    # en la siguiente linea buscamos un  usuario con ese id ¿ese id cual, el de la ruta? sii
    # el primer id es la key del modelo user, el segundo es el argumento de la funcion
    user = User.query.filter_by(id=id).first()
    print(fav_character)
    if fav_character and user:
        # vamos a crear el objeto, es asi como se crea un objeto en base a un modelo con sql alchemy, las key son las key del modelo character
        favorite = Fav_Characters(user_id=user.id, character_id=fav_character.id)
        # y lo añadimos a la db
        db.session.add(favorite)
        db.session.commit()

        response_body = {
            "msg": "ok"
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "ko"
        }
        return jsonify(response_body), 400

# y ya en postman solo tengo que meter como body en el post un {"id_character": 2} (xej 2 como puede ser otro ide de otro character)


@app.route('/user/<int:id>/fav_characters', methods=['DELETE'])
def delete_fav_character(id):
    id_character = request.json.get("id_character", None)
    delete_fav_character = Characters.query.filter_by(id=id_character).first()
    user = User.query.filter_by(id=id).first()
    print(delete_fav_character)
    print(user)
    if delete_fav_character and user:
        # añado que lo busco, no lo creo como en el POST
        favorite = Fav_Characters.query.filter_by(user_id=user.id, character_id=delete_fav_character.id).first()
        db.session.delete(favorite)
        db.session.commit()

        response_body = {
            "msg": "ok"
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "ko"
        }
        return jsonify(response_body), 400


@app.route('/user/<int:id>/fav_characters', methods=['GET'])
def get_fav_character(id):
    user = User.query.filter_by(id=id).first()
    # y si quiero en la siguiente linea decir que todos lo que sean asi en vez de first()? pues all parece 
    favoritos = Fav_Characters.query.filter_by(user_id=user.id).all()
    fav_characters_list = []
    for favorito in favoritos:
        fav_characters_list.append(favorito.serialize())
    return jsonify(fav_characters_list), 200

#********** PLANETS *************

@app.route('/user/<int:id>/fav_planets', methods=['POST'])
def add_fav_planet(id):
    id_planet = request.json.get("id_planet", None)
    # el primer id en el siguiente parentesis es el nombre de la columna id del class Planet
    fav_planet = Planets.query.filter_by(id=id_planet).first()
    # en la siguiente linea buscamos un usuario con ese id
    user = User.query.filter_by(id=id).first()
    print(fav_planet)
    if fav_planet and user:
        # ya encontramos tal y tal, ahora vamos a crear el objeto usando lo encontrado, es asi como se crea un objeto en base a un modelo con sql alchemy
        favorite = Fav_Planets(user_id=user.id, planet_id=fav_planet.id)
        # y lo añadimos a la db
        db.session.add(favorite)
        db.session.commit()

        response_body = {
            "msg": "ok"
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "ko"
        }
        return jsonify(response_body), 400

# y ya en postman solo tengo que meter como body en el post un {"id_planet": 2} (xej 2 como puede ser otro ide de otro planeta)


@app.route('/user/<int:id>/fav_planets', methods=['DELETE'])
def delete_fav_planet(id):
    id_planet = request.json.get("id_planet", None)
    delete_fav_planet = Planets.query.filter_by(id=id_planet).first()
    user = User.query.filter_by(id=id).first()
    print(delete_fav_planet)
    print(user)
    if delete_fav_planet and user:
        # añado que lo busco, no lo creo como en el POST
        favorite = Fav_Planets.query.filter_by(user_id=user.id, planet_id=delete_fav_planet.id).first()
        db.session.delete(favorite)
        db.session.commit()

        response_body = {
            "msg": "ok"
        }
        return jsonify(response_body), 200
    else:
        response_body = {
            "msg": "ko"
        }
        return jsonify(response_body), 400


@app.route('/user/<int:id>/fav_planets', methods=['GET'])
def get_fav_planet(id):
    user = User.query.filter_by(id=id).first()
    # y si quiero en la siguiente linea decir que todos lo que sean asi en vez de first()?
    favoritos = Fav_Planets.query.filter_by(user_id=user.id).all()
    fav_planets_list = []
    for favorito in favoritos:
        fav_planets_list.append(favorito.serialize())
    return jsonify(fav_planets_list), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
