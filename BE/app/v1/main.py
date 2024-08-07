from quart import Blueprint
from app.v1.register.users.users import users_bp

# Create Blueprint
v1_bp = Blueprint('v1', __name__)

# Resister Blueprint
v1_bp.register_blueprint(users_bp, url_prefix='/register')
