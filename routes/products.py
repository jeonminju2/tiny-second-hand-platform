import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Product

products_bp = Blueprint("products", __name__)

def is_safe_string(s):
    return isinstance(s, str) and len(s) <= 100 and re.match(r"^[\w\s가-힣.,!?~()\[\]-]*$", s)

@products_bp.route("/", methods=["POST"])
@jwt_required()
def create_product():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")
    seller_id = get_jwt_identity()
    
    if not is_safe_string(title) or not is_safe_string(description):
        return jsonify({"msg": "입력값이 유효하지 않습니다."}), 400
    if not isinstance(price, (int, float)) or price < 0:
        return jsonify({"msg": "가격은 0 이상의 숫자여야 합니다."}), 400
    
    product = Product(  # 괄호 오류 수정
        title=title,
        description=description,
        price=price,
        seller_id=seller_id
    )
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

@products_bp.route("/search")
def search_products():
    keyword = request.args.get("keyword", "")
    results = Product.query.filter(Product.title.ilike(f"%{keyword}%")).all()
    return jsonify([{
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": p.price,
        "seller_id": p.seller_id
    } for p in results])
