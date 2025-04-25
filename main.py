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

# Flask-Admin 설정 (관리자 페이지)
admin = Admin(app, name='관리자', template_mode='bootstrap3')
from models import User, Product, Report, Transaction, ChatMessage, BlockedUser, BlockedProduct  # 추가된 모델
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Report, db.session))
admin.add_view(ModelView(Transaction, db.session))
admin.add_view(ModelView(ChatMessage, db.session))
admin.add_view(ModelView(BlockedUser, db.session))  # 추가
admin.add_view(ModelView(BlockedProduct, db.session))  # 추가

# 블루프린트 등록
from routes.auth import auth_bp
from routes.products import products_bp
from routes.chat import chat_bp
from routes.report import report_bp
from routes.transfer import transfer_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(report_bp, url_prefix="/report")
app.register_blueprint(transfer_bp, url_prefix="/transfer")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    print("==== 등록된 URL 목록 ====")
    print(app.url_map)
    print("=======================")
