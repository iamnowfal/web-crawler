from flask import Blueprint, request, render_template, redirect, url_for, session
from src.models.users.user import User
import src.models.users.error as UserError
from src.models.searchs.search import Search
from src.models.favourites.favourite import Favourite

user_blueprint = Blueprint('users', __name__)


# User login
@user_blueprint.route('/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.is_login_valid(username, password):
            session['username'] = username
            return redirect(url_for('home_page'))

    return render_template('/users/login.html')


# User register
@user_blueprint.route('/register', methods=['POST', 'GET'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re-password']
        if User.register_user(username, password):
            if re_password == password:
                session['username'] = username
                return redirect(url_for('home_page'))
            else:
                raise UserError.ReTypePasswordError("Please confirm re-type password is the same as password")

    return render_template('/users/register.html')


# User search page
@user_blueprint.route('/<string:search_term>/<string:place>', methods=['POST', 'GET'])
def search(search_term, place):


    if request.method == 'GET':
        titles, tels, urls, addresses, rates = Search.search(search_term, place)
        return render_template('/users/search_results.html',
                           titles=titles, search_term=search_term, tels=tels, place=place,
                           urls=urls, addresses=addresses, rates=rates)

    if request.method == 'POST':
        search_term = request.form['search']
        search_term = search_term.replace(' ', '-')
        place = request.form['place']
        place = place.replace(' ', '-')
        return redirect(url_for('.search', search_term=search_term, place=place))



# Logout
@ user_blueprint.route('/logout')
def user_logout():
    session['username'] = None
    return redirect(url_for('home_page'))
