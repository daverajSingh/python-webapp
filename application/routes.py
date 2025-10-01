from flask import render_template
import random
from application import app
from data_access import get_jokes, get_joke


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/welcome/<string:name>')
def welcome(name='Team'):
    return render_template('welcome.html', title="Welcome", name=name.title(), group='Everyone')


@app.route('/joke')
def joke():
    joke_number = random.randrange(21)
    joke = get_joke(joke_number)
    joke_question = joke[0].json['joke']
    joke_answer = joke[0].json['punchline']
    return render_template('joke.html', title="Joke Time", joke_question=joke_question, joke_answer=joke_answer, number_of_jokes=21)

       
@app.route('/hello')
def hello():
    return render_template('hello.html', title='Hello')