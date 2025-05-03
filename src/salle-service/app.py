from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Salle Service API')

# Mock database
salles = [
    {"id": 1, "name": "Conference Room A", "capacity": 10},
    {"id": 2, "name": "Meeting Room B", "capacity": 6}
]

@api.route('/salles')
class SalleList(Resource):
    def get(self):
        return jsonify(salles)
    
    def post(self):
        data = request.get_json()
        new_salle = {
            "id": len(salles) + 1,
            "name": data["name"],
            "capacity": data["capacity"]
        }
        salles.append(new_salle)
        return jsonify(new_salle)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)