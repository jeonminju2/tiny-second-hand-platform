from flask import Flask
from models import db
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

from routes.auth import auth_bp
from routes.products import products_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(products_bp, url_prefix="/products")

if __name__ == "__main__":
    app.run(debug=True)

print("==== 등록된 URL 목록 ====")
print(app.url_map)
print("=======================")
