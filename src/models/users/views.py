from flask import Blueprint, request, render_template, redirect, url_for, session
from src.models.users.user import User
import src.models.users.error as UserError
from src.models.searchs.search import Search
from flask_paginate import Pagination

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
    search = False

    if request.method == 'GET':
        titles, tels, urls, addresses, rates = Search.search(search_term, place)
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1
        i = 0

        while i < len(titles):

            search = Search(title=titles[i], tel=tels[i], url=urls[i],
                            address=addresses[i], rates=rates[i], username=session['username'])
            try:
                search.save_to_mongo()
            except:
                pass

            i+=1

        search_results = Search.find_by_username(session['username'])

        pagination = Pagination(page=page, total=len(search_results), search=search, per_page=10, record_name='search_results')
        return render_template('/users/search_results.html', pagination=pagination,
                               search_results=search_results, search_term=search_term, place=place)

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
