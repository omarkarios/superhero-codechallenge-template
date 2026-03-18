#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# --- Resource Classes ---

class Heroes(Resource):
    def get(self):
        # Rubric: Return simple list of heroes
        heroes = [h.to_dict(only=('id', 'name', 'super_name')) for h in Hero.query.all()]
        return make_response(heroes, 200)

class HeroByID(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            # Rubric: Includes nested hero_powers and power data
            return make_response(hero.to_dict(), 200)
        else:
            return make_response({"error": "Hero not found"}, 404)

# --- Route Registration ---

api.add_resource(Heroes, '/heroes')
api.add_resource(HeroByID, '/heroes/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)