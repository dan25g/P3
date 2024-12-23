from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from email_validator import validate_email, EmailNotValidError


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')


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

    @staticmethod
    def validate_emails(email_list):
        for email in email_list:
            try:
                # Validar el email
                validate_email(email)
            except EmailNotValidError as e:
                # Retornar el mensaje de error si el email no es válido
                return str(e)
        return None
db.create_all()

#Responde simplemente pong
@app.route('/status', methods=['GET'])
def status():
    return jsonify({'response': 'pong'})

# Obtener todos los directorios
@app.route('/directories', methods=['GET'])
def get_directories():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    directories = Directory.query.paginate(page=page, per_page=per_page, error_out=False)
    if not directories.items:
        return jsonify({'message': 'No directories found'}), 404
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

        # Validar los correos electrónicos
        validation_error = Directory.validate_emails(data['emails'])
        if validation_error:
            return make_response(jsonify({'message': validation_error}), 400)
        
        new_directory = Directory(name=data['name'], emails=data['emails'])
        db.session.add(new_directory)
        db.session.commit()
        return make_response(jsonify(new_directory.json()),201)
    except  Exception as e:
        return make_response(jsonify({'message': e}), 500)
    

#Obtener un directorio
@app.route('/directories/<int:directory_id>', methods=['GET'])
def get_directory(directory_id):
    directory = Directory.query.get_or_404(directory_id)
    return jsonify(directory.json())


# Actualizar un directorio
@app.route('/directories/<int:directory_id>', methods=['PUT'])
def update_directory(directory_id):
    try:
        directory = Directory.query.get_or_404(directory_id)
        data = request.get_json()
        directory.name = data['name']
        directory.emails = data['emails']
        db.session.commit()
        return jsonify(directory.json())
    except Exception as e:
        return make_response(jsonify({'message': e}), 500)
    
#Actualizar parcialmente un directorio
@app.route('/directories/<int:directory_id>', methods=['PATCH'])
def partial_update_directory(directory_id):
    try:
        directory = Directory.query.get_or_404(directory_id)
        data = request.get_json()
        for key, value in data.items():
            setattr(directory, key, value)
            db.session.commit()
            return jsonify(directory.json())
    except Exception as e:
        return make_response(jsonify({'message': e}), 500)    
    
# Eliminar un directorio

@app.route('/directories/<int:directory_id>', methods=['DELETE'])
def delete_directory(directory_id):
    try:
        directory = Directory.query.get_or_404(directory_id)
        db.session.delete(directory)
        db.session.commit()
        return make_response(jsonify({'message': 'directorio eliminado'}), 200)
    except Exception as e:
        return make_response(jsonify({'message': e}), 500)    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)