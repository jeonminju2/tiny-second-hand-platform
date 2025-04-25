from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Product

products_bp = Blueprint("products", __name__)

@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")
    seller_id = get_jwt_identity()

    product = Product(title=title, description=description, price=price, seller_id=seller_id)
    db.session.add(product)
    db.session.commit()

    return jsonify({"msg": "상품이 등록되었습니다."}), 201

@products_bp.route("/", methods=["GET"])
def list_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": p.price,
        "seller_id": p.seller_id
    } for p in products]), 200