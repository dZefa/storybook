from flask import Flask, g
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from pprint import pprint
import sqlalchemy_utils
import json

with open('../sensitive.json') as data_file:    
    sensitive = json.load(data_file)
    rds_endpoint = sensitive['rds_endpoint']
    username = sensitive['username']
    password = sensitive['password']

with open('../db/sample_metadata/sampleMetadata.json') as data_file:    
    data = json.load(data_file)

#############################
#initialize app:
app = Flask(__name__, instance_relative_config=True, static_folder="../../client/static", template_folder="../../client/static")

#############################
#load compiled assets:
assets = Environment(app)
js = Bundle('bundle.js', output='gen/packed.js')
assets.register('js_all', js)

#############################
#app configs:
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://"+username+":"+password+"@"+rds_endpoint+"/"+username

#############################
#load database:
db = SQLAlchemy()
db.init_app(app)
db.app = app

from schema import Image, User, Relationship, Chatroom, Messages, Comments, Likes

db.drop_all()
db.create_all()
db.session.add(User("hello", 0, ["yes"]))

for i in data:
  db.session.add(Image(i['image_url'],  i['scn_code'], i['image_user_id'], i['latitude'], i['longitude'], i['likes_count'], i['caption'], i['image_tags_array']))
db.session.commit()

query = Image.query.all()
print(query)

##############################
#load Routes:
from app import routes