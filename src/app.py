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

@app.route('/user', methods=['GET'])
def handle_user():

   user_list = User.query.all()

   serialized_user = [item.serialize() for item in user_list]

   return jsonify(serialized_user), 200





@app.route('/people', methods=['GET'])
def handle_people():

    people_list = People.query.all()

    serialized_people = [item.serialize() for item in people_list]

    return jsonify(serialized_people), 200


@app.route('/people/<int:id>', methods=['GET'])

def handle_people_by_id(id):

    character = People.query.get(id) #Devuelve None si no lo encuentra

    if character != None:
        return jsonify(character.serialize()), 200    
    return jsonify({"error": "character not found"}), 404

@app.route('/favorite', methods=['POST'])

def handle_favorite():

    try:

        body = request.json
        newFavorite = Favorite()
        newFavorite.planet_id = body.get("planet_id")
        newFavorite.character_id = body.get("character_id")
        newFavorite.user_id = body.get("user_id")

        
        db.session.add (newFavorite) #Guarda en Ram
        
        db.session.commit() # Guarda en SQL

        return jsonify(newFavorite.serialize()), 200
    
    except ValueError:

        return jsonify({"error": "cant create favorite"}), 500

    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
