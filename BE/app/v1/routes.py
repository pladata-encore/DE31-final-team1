from quart import Blueprint
from app.v1.users.main import main_bp
from app.v1.nifi.nifi_api import nifi_api_bp
from app.v1.nifi.components.nifi_default import nifi_default_bp
from app.v1.data_group.main_dg import main_dg
# Create Blueprint
v1_bp = Blueprint('v1', __name__)

# Resister Blueprint
v1_bp.register_blueprint(main_bp, url_prefix='/users')
v1_bp.register_blueprint(nifi_api_bp, url_prefix='/nifi_api')
v1_bp.register_blueprint(nifi_default_bp, url_prefix='/nifi_default')
v1_bp.register_blueprint(main_dg, url_prefix='/data_group')