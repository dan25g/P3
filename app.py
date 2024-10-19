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
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    emails = db.Column(db.ARRAY(db.String(120)), unique=False, nullable=False)
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'emails': self.emails
        }
    
@app.route('/status', methods=['GET'])
def status():
    return jsonify({'response': 'pong'})



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)