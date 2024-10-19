from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

"""   USAR para la version definitiva

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

"""
#SOLO para probar
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:4520@localhost:5432/p3-test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

class Directory(db.Model):
    __tablename__ = 'Directories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    emails = db.Column(db.ARRAY(db.String(120)), unique=False, nullable=False)
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'emails': self.emails
        }

#Responde simplemente pong
@app.route('/status', methods=['GET'])
def status():
    return jsonify({'response': 'pong'})

# Obtener todos los directorios
@app.route('/directories', methods=['GET'])
def get_directories():
    page = request.args.get('page', 1, type=int)
    per_page = 1
    directories = Directory.query.paginate(page=page, per_page=per_page, error_out=False)
    base_url = request.base_url
    data = {
        'count': directories.total,
        'next': f"{base_url}?page={directories.next_num}" if directories.has_next else None,
        'prev': f"{base_url}?page={directories.prev_num}" if directories.has_prev else None,
        'results': [
            {
                'id': directory.id,
                'name': directory.name,
                'emails': directory.emails 
            } for directory in directories.items
        ]
    }
    return jsonify(data)


# Crear directorio
@app.route('/directories', methods=['POST'])
def create_directory():
    try:
        data = request.get_json()
        new_directory = Directory(name=data['name'], emails=data['emails'])
        db.session.add(new_directory)
        db.session.commit()
        return make_response(jsonify(new_directory.json()),201)
    except  Exception as e:
        return make_response(jsonify({'message': e}), 500)
    

"""
falta Obtener un directorio, Actualizar un directorio, 
Actualizar parcialmente un directorio y Eliminar un directorio

"""

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)