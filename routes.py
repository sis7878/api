from flask import Blueprint, request, jsonify, abort
from models import db, Pizza

pizza_bp = Blueprint('pizza', __name__)


@pizza_bp.route('/', methods=['POST'])
def create_pizza():
    data = request.get_json()

    if not data or not 'name' in data or not 'price' in data:
        abort(400, description="Missing required fields: name, price")

    new_pizza = Pizza(name=data['name'], description=data.get('description'), price=data['price'])

    db.session.add(new_pizza)
    db.session.commit()

    return jsonify({'id': new_pizza.id, 'name': new_pizza.name, 'price': new_pizza.price}), 201



@pizza_bp.route('/', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{'id': pizza.id, 'name': pizza.name, 'description': pizza.description, 'price': pizza.price} for pizza in pizzas])



@pizza_bp.route('/<int:id>', methods=['GET'])
def get_pizza(id):
    pizza = Pizza.query.get_or_404(id)
    return jsonify({'id': pizza.id, 'name': pizza.name, 'description': pizza.description, 'price': pizza.price})



@pizza_bp.route('/<int:id>', methods=['PUT'])
def update_pizza(id):
    pizza = Pizza.query.get_or_404(id)

    data = request.get_json()
    pizza.name = data.get('name', pizza.name)
    pizza.description = data.get('description', pizza.description)
    pizza.price = data.get('price', pizza.price)

    db.session.commit()

    return jsonify({'id': pizza.id, 'name': pizza.name, 'description': pizza.description, 'price': pizza.price})



@pizza_bp.route('/<int:id>', methods=['DELETE'])
def delete_pizza(id):
    pizza = Pizza.query.get_or_404(id)
    db.session.delete(pizza)
    db.session.commit()

    return jsonify({'message': 'Pizza deleted successfully'}), 204
