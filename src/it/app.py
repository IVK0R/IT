from flask import Flask, render_template, request, jsonify, session, redirect
import mysql.connector
from llama_cpp import Llama
import hashlib
import os

REPO_ID = "bartowski/Qwen2.5-0.5B-Instruct-GGUF"
FILENAME = "Qwen2.5-0.5B-Instruct-Q4_K_M.gguf"

print(f"Загрузка модели {FILENAME} из {REPO_ID}...")
llm = Llama.from_pretrained(
    repo_id=REPO_ID,
    filename=FILENAME,
    n_ctx=2048,
    verbose=False
)
print("Модель успешно загружена.")
salt = os.fsencode('привет')
def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
    return salt.hex() + '$' + hash_object.hex()

def connection():
    return mysql.connector.connect(
        host="185.114.247.43",
        port=3306,
        database="sch688_vvedenie",
        user="sch688_vvedenie",
        password="Qwerty123")

app = Flask(__name__)  
app.secret_key = "1581"


@app.route('/user_registeration', methods=['POST'])
def user_registration():
    email = req['email']
    password_hash = hash_password(req['password'])  # хешируем пароль
    date = (name, email, password_hash)
    cnx  = connection()
    try:
        cur = cnx.cursor(dictionary=True)
        cur.execute('SELECT id FROM users WHERE email = %s', (email,))
        if cur.fetchone():
            return jsonify({'error': 'пользователь с таким email уже существует'})

        cur.execute(
            'INSERT INTO `users`(`username`, `email`, `password_hash`) VALUES (%s, %s, %s)',
            (name, email, password_hash)
        )
        cnx.commit()
    finally:
        cur.close()
        cnx.close()

    return jsonify({'ok': True})


@app.route('/user_authorization', methods=['POST'])
def user_authorization():
    req = request.get_json()
    name = req['name']
    email = req['email']
    password_hash = hash_password(req['password'])
    date = (name, email, password_hash)
    cnx = connection()
    cur = cnx.cursor()

    rows = cur.execute('SELECT * FROM users WHERE email=%s AND password_hash=%s', date)
    cnx.commit()
    cnx.close()
    return {'result': True}

    return 'Пользователь успешно зарегистрирован'

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/")
def registration():
    return render_template('registration.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

app.run()