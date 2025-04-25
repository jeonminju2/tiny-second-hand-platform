from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, ChatMessage

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/send", methods=["POST"])
@jwt_required()
def send_message():
    data = request.get_json()
    receiver_id = data.get("receiver_id")
    message = data.get("message")
    sender_id = get_jwt_identity()
    
    if not receiver_id or not message:
        return jsonify({"msg": "필수값 누락"}), 400
    
    chat = ChatMessage(  # 괄호 오류 수정
        sender_id=sender_id,
        receiver_id=receiver_id,
        message=message
    )
    db.session.add(chat)
    db.session.commit()
    return jsonify({"msg": "메시지 전송 성공"}), 201

@chat_bp.route("/history/<int:user_id>", methods=["GET"])  # 라우트 경로 수정
@jwt_required()
def chat_history(user_id):
    current_user = get_jwt_identity()
    messages = ChatMessage.query.filter(
        ((ChatMessage.sender_id == current_user) & (ChatMessage.receiver_id == user_id)) |
        ((ChatMessage.sender_id == user_id) & (ChatMessage.receiver_id == current_user))
    ).order_by(ChatMessage.timestamp).all()
    return jsonify([{
        "id": msg.id,
        "sender": msg.sender_id,
        "message": msg.message,
        "timestamp": msg.timestamp.isoformat()
    } for msg in messages]), 200
