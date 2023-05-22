from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from user import User
import json
import os

secret_key = os.urandom(24).hex()

app = Flask(__name__)
app.secret_key = secret_key

# establish database connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/news'
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database()
users = db.users

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('login-email')
    password = request.form.get('login-password')
    user_data = users.find_one({'email': email})
    print(user_data)

    if user_data and user_data['password'] == password:
        # successful login

        # create user instance
        user = User(user_data['fname'], user_data['lname'], user_data['email'], user_data['password'], user_data['interests'], user_data['article_history'])
        session['user_id'] = str(user_data['_id'])
        return redirect('/home')
    else:
        # failed login
        return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    fname = request.form.get('signup-firstName')
    lname = request.form.get('signup-lastName')
    email = request.form.get('signup-email')
    password = request.form.get('signup-password')

    # check if user exists
    if users.find_one({'email': email}):
        print('failed')
        return redirect('/')

    # add user to the database and create an instance of the user
    new_user = {
        'fname': fname,
        'lname:': lname,
        'email': email,
        'password': password,
        'interests': None,
        'article_history': None
    }
    users.insert_one(new_user)
    user = User(new_user['fname'], new_user['lname'], new_user['email'], new_user['password'],
                new_user['interests'], new_user['article_history'])
    session['user_id'] = str(new_user['_id'])

    return redirect('/home')


@app.route('/home')
def dashboard():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
