from flask import Blueprint, render_template, request, redirect, url_for
from src.models.searchs.search import Search

search_blueprint = Blueprint('search', __name__)


@search_blueprint.route('/<string:search_term>/<string:place>', methods=['POST', 'GET'])
def index(search_term, place):
    if request.method == 'GET':
        titles, tels, urls, addresses, rates = Search.search(search_term, place)
        return render_template('/search/index.html',
                           titles=titles, search_term=search_term, tels=tels, place=place,
                           urls=urls, addresses=addresses, rates=rates)

    if request.method == 'POST':
        search_term = request.form['search']
        search_term = search_term.replace(' ', '-')
        place = request.form['place']
        place = place.replace(' ', '-')
        return redirect(url_for('search.index', search_term=search_term, place=place))

