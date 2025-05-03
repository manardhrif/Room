from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

api = Api(app, version='1.0', title='User Service API')

# Mock database
users = [
    {"id": 1, "username": "admin", "password": generate_password_hash("admin123"), "role": "admin"},
    {"id": 2, "username": "employee", "password": generate_password_hash("emp123"), "role": "employee"}
]

# JWT Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {"message": "Token is missing!"}, 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return {"message": "Token is invalid!"}, 401
        return f(*args, **kwargs)
    return decorated

@api.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = next((u for u in users if u['username'] == username), None)
        if not user or not check_password_hash(user['password'], password):
            return {"message": "Invalid credentials"}, 401
        
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'])
        
        return {"token": token}

@api.route('/users')
class UserList(Resource):
    @token_required
    def get(self):
        return jsonify([{"id": u["id"], "username": u["username"], "role": u["role"]} for u in users])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)