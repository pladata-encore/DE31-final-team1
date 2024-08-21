from quart import Blueprint
from app.v1.users.register.createUser import createUser_bp
from app.v1.users.authorization.login import login_bp

# Create Blueprint
v1_bp = Blueprint('v1', __name__)

# Resister Blueprint
v1_bp.register_blueprint(createUser_bp, url_prefix='/users')
v1_bp.register_blueprint(login_bp, url_prefix='/users')
