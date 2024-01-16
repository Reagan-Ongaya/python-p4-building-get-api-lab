#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    
    bakery = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "name":bakery.name,
            "location": bakery.location
        }
        bakery.append(bakery_dict)
        
    response = make_response(
        jsonify(bakeries),
        200
    )    
    bakery = Bakery()
    return jsonify({'location': bakery.location})

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    
    bakery_dict = bakery.to_dict()
    
    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers["Content-Type"] = "application/json"
     
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price(price):
    bakedgood = BakedGood.query.filter_by( price=price ).first()
    
    bakedgood_dict = bakedgood.to_dict()
    
    response = make_response(
        jsonify(bakedgood_dict),
        200
    ) 
    
    response.headers["Content-Type"] = "application/json"
    
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    bakedgood = BakedGood
    
    baked_goods = bakedgood.to_dict()
    
    if not baked_goods:
        
        return jsonify({"error": "No baked goods available"}), 404

    most_expensive_good = max(baked_goods, key=lambda x: x["price"])

    return jsonify(most_expensive_good)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
