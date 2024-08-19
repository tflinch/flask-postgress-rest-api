from flask import Flask, request
from dotenv import load_dotenv
import os, psycopg2 , psycopg2.extras
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)

CORS(app)

def get_db_connection():
    connection = psycopg2.connect(
        host='localhost',
        database='pets_db',
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )
    return connection

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/pets')
def pets_index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM pets;")
        pets = cursor.fetchall()
        connection.close()
        return pets
    except:
        return "Application Error", 500

@app.route('/create_pets', methods=['POST'])
def create_pet():
    try:
        new_pet = request.json
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("INSERT INTO pets (name, age, breed) VALUES (%s, %s, %s) RETURNING *", (new_pet['name'], new_pet['age'], new_pet['breed']))
        created_pet = cursor.fetchone()  
        connection.commit()
        return created_pet, 201
    except Exception as e:
        return str(e), 500
    
@app.route('/pets/<pet_id>', methods=['GET'])
def show_pet(pet_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM pets WHERE id = %s", (pet_id,))
        pet = cursor.fetchone()
        if pet is None:
            connection.close()
            return "Pet Not Found", 404
        connection.close()
        return pet, 200
    except Exception as e:
        return str(e), 500
    
@app.route('/pets/<pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM pets WHERE id = %s", (pet_id,))
        connection.commit()
        cursor.close()
        return "Pet deleted successfully", 204
    except Exception as e:
        return str(e), 500

@app.route('/pets/<pet_id>', methods=['PUT'])
def update_pet(pet_id):
    try:
      connection = get_db_connection()
      cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cursor.execute("UPDATE pets SET name = %s, age = %s, breed = %s WHERE id = %s RETURNING *", (request.json['name'], request.json['age'], request.json['breed'], pet_id))
      updated_pet = cursor.fetchone()
      if updated_pet is None:
        return "Pet Not Found", 404
      connection.commit()
      connection.close()
      return updated_pet, 202
    except Exception as e:
      return str(e), 500

app.run()