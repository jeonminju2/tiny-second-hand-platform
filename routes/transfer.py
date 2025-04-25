from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Transaction

transfer_bp = Blueprint("transfer", __name__)

@transfer_bp.route("", methods=["POST"])
@jwt_required()
def transfer():
    data = request.get_json()
    receiver_id = data.get("receiver_id")
    amount = data.get("amount")
    sender_id = get_jwt_identity()
    
    if not receiver_id or not amount:
        return jsonify({"msg": "필수값 누락"}), 400
    
    sender = User.query.get(sender_id)
    receiver = User.query.get(receiver_id)
    
    if not receiver:
        return jsonify({"msg": "수신자가 존재하지 않습니다."}), 404
    if sender.balance < amount:
        return jsonify({"msg": "잔액이 부족합니다."}), 400
    
    sender.balance -= amount
    receiver.balance += amount
    
    transaction = Transaction(  # 괄호 오류 수정
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=amount
    )
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({"msg": "송금 완료"}), 201
