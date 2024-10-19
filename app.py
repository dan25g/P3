from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
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
    
    db.create_all()

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'response': 'pong'})



if __name__ == '__main__':
    app.run()