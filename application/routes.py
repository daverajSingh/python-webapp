from flask import render_template, request
import random
from application import app
from data_access import get_jokes, get_joke, add_joke, get_joke_count


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/welcome/<string:name>')
def welcome(name='Team'):
    return render_template('welcome.html', title="Welcome", name=name.title(), group='Everyone')


@app.route('/joke')
def joke():
    all_jokes = get_jokes()
    random_joke = random.choice(all_jokes[0].json)
    joke_question = random_joke['joke']
    joke_answer = random_joke['punchline']
    joke_count_json = get_joke_count()
    joke_count = joke_count_json[0].json[0]['joke_count']
    return render_template('joke.html', title="Joke Time", joke_question=joke_question, joke_answer=joke_answer, number_of_jokes=joke_count)

@app.route('/add_joke')
def new_joke():
    # joke = request.form['joke']
    return render_template('insert_joke.html', title="Insert joke")

@app.route('/insert_joke', methods=['POST'])
def insert_joke():
    joke = request.form['joke']
    punchline = request.form['punchline']
    add_joke(joke, punchline)
    return render_template('insert_joke.html', title="Insert joke")


@app.route('/hello')
def hello():
    return render_template('hello.html', title='Hello')

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
