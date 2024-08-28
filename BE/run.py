from quart import Quart
from app.v1.routes import v1_bp
from app.v2.main import v2_bp
from app.test.main import t_bp
import os
import quart_cors
import quart

from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# cors 적용 (모두 허용)
app = quart_cors.cors(quart.Quart(__name__), 
    allow_origin='*', 
    allow_methods=['POST','GET','OPTIONS','PUT'], 
    allow_headers=['Content-Type', 
                   'Access-Control-Allow-Origin',
                   'Access-Control-Allow-Methods',
                   'Access-Control-Allow-Headers',
                   'Access-Control-Allow-Credentials'],
    allow_credentials=False
    )

# jwt key
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# 블루프린트를 등록하여 버전별로 API를 관리
app.register_blueprint(v1_bp, url_prefix='/v1')
app.register_blueprint(v2_bp, url_prefix='/v2')
app.register_blueprint(t_bp, url_prefix='/t')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=19020)