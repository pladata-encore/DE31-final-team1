from quart import Blueprint
from app.v1.users.main import main_bp

# Create Blueprint
v1_bp = Blueprint('v1', __name__)

# Resister Blueprint
v1_bp.register_blueprint(main_bp, url_prefix='/users')
