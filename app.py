from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import hashlib

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")
db = client.person_db

@app.route('/')
def index():
    people = list(db.people.find({}, {"_id": 0, "id": 1, "nome_pessoa": 1, "token": 1}))
    return render_template('index.html', people=people)

@app.route('/register', methods=['POST'])
def register_person():
    data = request.form
    id = int(data['id'])
    nome_pessoa = data['nome_pessoa']
    token = generate_token(id, nome_pessoa)
    db.people.insert_one({"id": id, "nome_pessoa": nome_pessoa, "token": token})
    return jsonify({"id": id, "nome_pessoa": nome_pessoa, "token": token})

@app.route('/get_people', methods=['GET'])
def get_people():
    people = list(db.people.find({}, {"_id": 0, "id": 1, "nome_pessoa": 1, "token": 1}))
    return jsonify(people)

def generate_token(id, nome_pessoa):
    return hashlib.md5(f"{id}{nome_pessoa}".encode()).hexdigest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
