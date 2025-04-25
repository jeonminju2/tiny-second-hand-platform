from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Report

# "report" 대신 "report_bp"로 이름 변경
report_bp = Blueprint("report_bp", __name__)

@report_bp.route("/user", methods=["POST"])
@jwt_required()
def report_user():
    data = request.get_json()
    reported_user_id = data.get("reported_user_id")
    reason = data.get("reason")
    reporter_id = get_jwt_identity()
    
    if not reported_user_id or not reason:
        return jsonify({"msg": "필수값 누락"}), 400
    
    report = Report(
        reporter_id=reporter_id,
        reported_user_id=reported_user_id,
        reason=reason
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({"msg": "사용자 신고 완료"}), 201

@report_bp.route("/product", methods=["POST"])
@jwt_required()
def report_product():
    data = request.get_json()
    reported_product_id = data.get("reported_product_id")
    reason = data.get("reason")
    reporter_id = get_jwt_identity()
    
    if not reported_product_id or not reason:
        return jsonify({"msg": "필수값 누락"}), 400
    
    report = Report(
        reporter_id=reporter_id,
        reported_product_id=reported_product_id,
        reason=reason
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({"msg": "상품 신고 완료"}), 201
