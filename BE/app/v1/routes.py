from quart import Blueprint
from app.v1.users.main import main_bp
from app.v1.data_source.main_ds import main_ds
from app.v1.data_group.main_dg import main_dg

# Create Blueprint
v1_bp = Blueprint('v1', __name__)

# Resister Blueprint
v1_bp.register_blueprint(main_bp, url_prefix='/users')
v1_bp.register_blueprint(main_ds, url_prefix='/data_source')
v1_bp.register_blueprint(main_dg, url_prefix='/data_group')