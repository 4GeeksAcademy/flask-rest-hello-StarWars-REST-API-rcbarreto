"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
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

@app.route('/users', methods=['GET'])
def get_users():

   user_list = User.query.all()

   serialized_user = [item.serialize() for item in user_list]

   return jsonify(serialized_user), 200





@app.route('/people', methods=['GET'])
def get_people():

    people_list = People.query.all()

    serialized_people = [item.serialize() for item in people_list]

    return jsonify(serialized_people), 200


@app.route('/people/<int:id>', methods=['GET'])

def get_people_by_id(id):

    character = People.query.get(id) #Devuelve None si no lo encuentra

    if character != None:
        return jsonify(character.serialize()), 200    
    return jsonify({"error": "character not found"}), 404



@app.route('/planets', methods=['GET'])
def get_planets():

    planets_list = Planet.query.all()

    serialized_planets = [item.serialize() for item in planets_list]

    return jsonify(serialized_planets), 200


@app.route('/planets/<int:id>', methods=['GET'])

def get_planets_by_id(id):

    planet = Planet.query.get(id) #Devuelve None si no lo encuentra

    if planet != None:
        return jsonify(planet.serialize()), 200    
    return jsonify({"error": "planet not found"}), 404









@app.route('/users/favorites', methods=['GET'])

def get_favorites_by_user():

    try:    
        
        body = request.json
        if not body or "user_id" not in body:
            return jsonify({"msg": "User ID is required"}), 400
        
        user = User.query.get(body.get("user_id"))
        if not user:
            return jsonify({"msg": "User doesn't exist"}), 404
    
        favorite_list = Favorite.query.filter_by(user_id = body.get("user_id"))

        serialized_favorite = [item.serialize() for item in favorite_list]

        return jsonify(serialized_favorite), 200

    except ValueError:

        return jsonify({"error": "cant create favorite"}), 500









@app.route('/favorite/people/<int:id>', methods=['POST'])

def add_favorite_people(id):

    try:

        
        people = People.query.get(id)
        if not people:
            return jsonify({"msg": "People doesn't exist"}), 404
        
        body = request.json
        if not body or "user_id" not in body:
            return jsonify({"msg": "User ID is required"}), 400
        
        user = User.query.get(body.get("user_id"))
        if not user:
            return jsonify({"msg": "User doesn't exist"}), 404
        
        body = request.json
        newFavorite = Favorite()
        #newFavorite.planet_id = id
        newFavorite.character_id = id
        newFavorite.user_id = body.get("user_id")

        
        db.session.add (newFavorite) #Guarda en Ram
        
        db.session.commit() # Guarda en SQL

        return jsonify(newFavorite.serialize()), 200
    
    except ValueError:

        return jsonify({"error": "cant create favorite"}), 500
    


@app.route('/favorite/planet/<int:id>', methods=['POST'])

def add_favorite_planet(id):

    try:

        
        planet = Planet.query.get(id)
        if not planet:
            return jsonify({"msg": "Planet doesn't exist"}), 404
        
        body = request.json
        if not body or "user_id" not in body:
            return jsonify({"msg": "User ID is required"}), 400
        
        user = User.query.get(body.get("user_id"))
        if not user:
            return jsonify({"msg": "User doesn't exist"}), 404
        
        body = request.json
        newFavorite = Favorite()
        newFavorite.planet_id = id
        # newFavorite.character_id = id
        newFavorite.user_id = body.get("user_id")

        
        db.session.add (newFavorite) #Guarda en Ram
        
        db.session.commit() # Guarda en SQL

        return jsonify(newFavorite.serialize()), 200
    
    except ValueError:

        return jsonify({"error": "cant create favorite"}), 500
    
    


@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def delete_people_favorite(id):
    try:
                      
        people = People.query.get(id)
        if not people:
            return jsonify({"msg": "People doesn't exist"}), 404
        
        
        favorite_delete = Favorite.query.filter_by( character_id=people.id).first()
        if not favorite_delete:
            return jsonify({"msg": "Favorite doesn't exist"}), 404
        
        
        db.session.delete(favorite_delete)
        db.session.commit()
        
       
        return jsonify({"msg": "Favorite successfully deleted"}), 200

    except Exception as e:
        
        return jsonify({"error": str(e)}), 500


@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_planet_favorite(id):
    try:
                      
        planet = Planet.query.get(id)
        if not planet:
            return jsonify({"msg": "Planet doesn't exist"}), 404
        
        # Verificar si el favorito existe
        favorite_delete = Favorite.query.filter_by( planet_id=planet.id).first()
        if not favorite_delete:
            return jsonify({"msg": "Favorite doesn't exist"}), 404
        
        # Eliminar el favorito
        db.session.delete(favorite_delete)
        db.session.commit()
        
        
        return jsonify({"msg": "Favorite successfully deleted"}), 200

    except Exception as e:
        
        return jsonify({"error": str(e)}), 500

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
