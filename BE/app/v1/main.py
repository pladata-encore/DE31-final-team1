from quart import Blueprint
from app.v1.users.register.createUser import createUser_bp

# Create Blueprint
v1_bp = Blueprint('v1', __name__)

# Resister Blueprint
v1_bp.register_blueprint(createUser_bp, url_prefix='/users')
