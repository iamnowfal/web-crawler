from flask import Blueprint, request, render_template, redirect, url_for, session
from src.models.users.user import User
import src.models.users.error as UserError

user_blueprint = Blueprint('users', __name__)

#User login
@user_blueprint.route('/login', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.is_login_valid(username,password):
            session['username'] = username
            return redirect(url_for('.search'))

    return render_template('/users/login.html')

#User register
@user_blueprint.route('/register', methods=['POST', 'GET'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re-password']
        if User.register_user(username, password):
            if re_password == password:
                session['username'] = username
                return redirect(url_for('.search'))
            else:
                raise UserError.ReTypePasswordError("Please confirm re-type password is the same as password")

    return render_template('/users/register.html')

#User search page
@user_blueprint.route('/')
def search():
    return render_template('/users/search.html')

#Logout
@user_blueprint.route('/logout')
def user_logout():
    session['username'] = None
    return redirect(url_for('home.html'))