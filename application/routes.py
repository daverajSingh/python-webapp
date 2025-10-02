from flask import render_template, request, redirect, url_for, make_response, g
import random
from application import app
from data_access import get_jokes, get_joke, add_joke, get_joke_count, create_new_user, login_user
from jwt_utility import create_jwt, decode_jwt


@app.route('/')
@app.route('/home')
def home():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    decoded_token = decode_jwt(token)
    if not decoded_token:
        return redirect(url_for('login'))
    return render_template('home.html', title='Home')

@app.route('/welcome/<string:name>')
def welcome(name='Team'):
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    decoded_token = decode_jwt(token)
    if not decoded_token:
        return redirect(url_for('login'))
    return render_template('welcome.html', title="Welcome", name=name.title(), group='Everyone')

@app.route('/joke')
def joke():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    decoded_token = decode_jwt(token)
    if not decoded_token:
        return redirect(url_for('login'))
    all_jokes = get_jokes()
    random_joke = random.choice(all_jokes[0].json)
    joke_question = random_joke['joke']
    joke_answer = random_joke['punchline']
    joke_count_json = get_joke_count()
    joke_count = joke_count_json[0].json[0]['joke_count']
    return render_template('joke.html', title="Joke Time", joke_question=joke_question, joke_answer=joke_answer, number_of_jokes=joke_count)

@app.route('/insert_joke', methods=['GET', 'POST'])
def insert_joke():
    if request.method == 'POST':
        joke = request.form['joke']
        punchline = request.form['punchline']
        add_joke(joke, punchline)
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    decoded_token = decode_jwt(token)
    if not decoded_token:
        return redirect(url_for('login'))
    return render_template('insert_joke.html', title="Insert joke")

@app.route('/hello')
def hello():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    decoded_token = decode_jwt(token)
    if not decoded_token:
        return redirect(url_for('login'))
    return render_template('hello.html', title='Hello')

# Login & Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        create_new_user(email, password)
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = login_user(email, password)
        if result:
            token = create_jwt(email)
            response = make_response(redirect(url_for('home')))
            response.set_cookie('token', token)
            return response
        else:
            return redirect(url_for('register'))
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('token')
    return response

# @app.context_processor
# def inject_current_user():
#     token = request.cookies.get("token")
#     if not token:
#         return {"current_user": None}
#     user = decode_jwt(token)
#     return {"current_user": user}


# Postman test routes
@app.route('/get_joke/<int:joke_id>', methods=['GET'])
def get_joke_id(joke_id):
    joke = get_joke(joke_id)
    return joke[0].json

@app.route('/get_all_jokes', methods=['GET'])
def get_all_jokes():
    all_jokes = get_jokes()
    return all_jokes[0].json

@app.route('/add_new_joke/<string:joke>&<string:punchline>', methods=['POST'])
def add_new_joke(joke, punchline):
    add_joke(joke, punchline)
    return [joke, punchline]

@app.route('/authenticate_user/<string:email>&<string:password>', methods=['POST'])
def authenticate_user(email, password):
    e = login_user(email, password)
    return [email, password] if e[0] == 200 else e[0].json

@app.route('/add_new_user/<string:email>&<string:password>', methods=['POST'])
def add_new_user(email, password):
    e = create_new_user(email, password)
    return [email, password] if not e else e[0].json

