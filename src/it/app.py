from flask import Flask, render_template, request, jsonify
import mysql.connector
import hashlib
import os

def hash_password(password):
    salt = os.urandom(32)
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
    return salt.hex() + '$' + hash_object.hex()


app = Flask(__name__)  

@app.route('/user_register', methods=['POST'])
def user_register():
    req = request.get_json()
    cnx = mysql.connector.connect(
        host="185.114.247.43",
        port=3306,
        database="sch688_vvedenie",
        user="sch688_vvedenie",
        password="Qwerty123")
    
    name = req['name']
    login = req['email']
    password_hash = hash_password(req['password'])  # хешируем пароль
    date = (name, login, password_hash)
    cur = cnx.cursor()

    cur.execute('SELECT 1 FROM `users` WHERE `email` = %s LIMIT 1', (login,))
    if cur.fetchone() is not None:
        cnx.close()
        return jsonify({'error': 'Пользователь с таким email уже существует'}), 409

    rows = cur.execute('INSERT INTO `users`(`username`, `email`, `password_hash`) VALUES (%s, %s, %s)', date)
    cnx.commit()
    cnx.close()

    return 'Пользователь успешно зарегистрирован'


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/")
def registration():
    return render_template('registration.html')

app.run()