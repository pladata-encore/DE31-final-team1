from quart import Blueprint
from app.v1.users.main import users_bp
from app.v1.data_source.main_ds import data_source_bp
from app.v1.data_group.main_dg import data_group_bp
from app.v1.subprocess.main import subprocess_bp
from app.v1.nifi.nifi_api import nifi_api_bp
from app.v1.nifi.components.nifi_default import nifi_default_bp
from app.v1.airflow.airflow_api import airflow_bp

# Create Blueprint
v1_bp = Blueprint('v1', __name__)

# Resister Blueprint
v1_bp.register_blueprint(users_bp, url_prefix='/users')
v1_bp.register_blueprint(data_source_bp, url_prefix='/data-source')
v1_bp.register_blueprint(data_group_bp, url_prefix='/data-group')
v1_bp.register_blueprint(subprocess_bp, url_prefix='/subprocess')
v1_bp.register_blueprint(nifi_api_bp, url_prefix='/nifi_api')
v1_bp.register_blueprint(nifi_default_bp, url_prefix='/nifi_default')
v1_bp.register_blueprint(airflow_bp, url_prefix='/airflow')