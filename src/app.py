from flask import Flask, render_template, request, redirect, url_for, session
from src.common.database import Database

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = '123'

@app.before_first_request
def init_db():
    Database.initialise()

@app.route('/', methods=['POST', 'GET'])
def home_page():
    if session['username']:
        if request.method == 'POST':
            search_term = request.form['search']
            search_term = search_term.replace(' ', '-')
            place = request.form['place']
            place = place.replace(' ', '-')
            return redirect(url_for('users.search', search_term=search_term, place=place))
        return render_template('/home.html')
    else:
        if request.method == 'POST':
            search_term = request.form['search']
            search_term = search_term.replace(' ', '-')
            place = request.form['place']
            place = place.replace(' ', '-')
            return redirect(url_for('search.index', search_term=search_term, place=place))
        return render_template('/home.html')

from src.models.users.views import user_blueprint
from src.models.favourites.views import favourite_blueprint
from src.models.searchs.views import search_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(search_blueprint, url_prefix='/search')
app.register_blueprint(favourite_blueprint, url_prefix='/favourites')


