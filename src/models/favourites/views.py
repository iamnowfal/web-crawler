from flask import Blueprint, session, render_template
from src.models.favourites.favourite import Favourite


favourite_blueprint = Blueprint('favourites', __name__)


@favourite_blueprint.route('/add/<string:titles>/<string:tels>/<string:urls>/<string:addresses>/<string:rates>')
def add_favourite(titles, tels, urls, addresses, rates):
    favourite = Favourite(session['username'], titles, tels, urls, addresses, rates)
    favourite.save_to_mongo
    return render_template('/users/search_results.html')



@favourite_blueprint.route('/favourites')
def show_favourite():
    pass


@favourite_blueprint.route('/delete/favourite')
def delete_favourite():
    pass