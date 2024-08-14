from flask import Flask
from dotenv import load_dotenv
import os, psycopg2
load_dotenv()

app = Flask(__name__)

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
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM pets;")
    pets = cursor.fetchall()
    connection.close()
    return pets

app.run()