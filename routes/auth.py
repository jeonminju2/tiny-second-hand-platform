from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"msg": "모든 필드를 입력해야 합니다."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "이미 존재하는 사용자 이름입니다."}), 400

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "회원가입 성공"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        expires = datetime.timedelta(days=1)
        # identity를 반드시 str(user.id)로!
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "로그인 실패"}), 401
