from flask import Flask
from models import db
from flask_jwt_extended import JWTManager
from config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

# models.py에 새 모델 추가
from models import User, Product

# Flask-Admin 설정 (관리자 페이지)
admin = Admin(app, name='관리자', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))

# 블루프린트 등록
from routes.auth import auth_bp
from routes.products import products_bp

# 기존 블루프린트 등록
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(products_bp, url_prefix="/products")

# 새 블루프린트 등록 (등록된 파일이 존재할 경우만)
try:
    from routes.chat import chat_bp
    app.register_blueprint(chat_bp, url_prefix="/chat")
except ImportError:
    print("chat_bp를 찾을 수 없습니다.")

try:
    from routes.report import report_bp
    app.register_blueprint(report_bp, url_prefix="/report")
except ImportError:
    print("report_bp를 찾을 수 없습니다.")

try:
    from routes.transfer import transfer_bp
    app.register_blueprint(transfer_bp, url_prefix="/transfer")
except ImportError:
    print("transfer_bp를 찾을 수 없습니다.")

if __name__ == "__main__":
    with app.app_context():
        # 데이터베이스 테이블 자동 생성
        db.create_all()
    
    app.run(debug=True)
    
    print("==== 등록된 URL 목록 ====")
    print(app.url_map)
    print("=======================")
