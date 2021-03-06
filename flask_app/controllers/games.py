from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.game import Game

@app.route('/home')
def home():
    if not session.get('user_id'):
        session['user_id'] = None
        
    data = {
        'atlas_game_id' : 'F1aw7kyGTA'
    }
    featured = Game.get_game_info(data)

    random = Game.get_random_game()
    # featured = {
    #     'id': 'F1aw7kyGTA',
    #     'image_url': 'https://s3-us-west-1.amazonaws.com/5cc.images/games/uploaded/1559254186139-51cXhVYYHwL.jpg',
    #     "name": "Bohnanza",
    #     "description_preview": " This great card game is about planting, trading, and selling beans - 11 kinds of beans (this English version includes all the cards from the original game and the first expansion).   Players try to collect large sets of beans to sell for gold. There is limited growing space and always new beans to plant. To avoid planting unwanted beans, players trade them to other players who want them for their bean fields. "
    # }

    # random = {
    #     'id': 'F1aw7kyGTA',
    #     'image_url': 'https://s3-us-west-1.amazonaws.com/5cc.images/games/uploaded/1559254186139-51cXhVYYHwL.jpg',
    #     "name": "Bohnanza",
    #     "description_preview": " This great card game is about planting, trading, and selling beans - 11 kinds of beans (this English version includes all the cards from the original game and the first expansion).   Players try to collect large sets of beans to sell for gold. There is limited growing space and always new beans to plant. To avoid planting unwanted beans, players trade them to other players who want them for their bean fields. "
    # }

    return render_template('index.html', featured = featured, random = random)

@app.route('/game/<game_id>')
def get_game(game_id):
    data = {
        'atlas_game_id' : game_id,
        'user_id' : session['user_id']
    }

    game_info = Game.get_game_info(data)

    is_favorite = Game.is_favorite_game(data)
    is_owned = Game.is_owned_game(data)

    return render_template('game_details.html', game_info = game_info, is_favorite = is_favorite, is_owned = is_owned)

@app.route('/add_favorite_game/<atlas_game_id>', methods = ['POST'])
def add_fav_game(atlas_game_id):

    data = {
        'user_id' : session['user_id'],
        'atlas_game_id' : request.form['atlas_game_id'],
        'atlas_game_name' : request.form['atlas_game_name']
    }

    Game.add_favorite_game(data)

    return redirect(f'/game/{atlas_game_id}')

@app.route('/game_detail/remove_favorite_game/<atlas_game_id>', methods = ['POST'])
def game_details_remove_fav_game(atlas_game_id):
    data = {
        'user_id' : session['user_id'],
        'atlas_game_id' : request.form['atlas_game_id'],
        'atlas_game_name' : request.form['atlas_game_name']
    }

    Game.remove_favorite_game(data)

    return redirect(f'/game/{atlas_game_id}')

@app.route('/dashboard/remove_favorite_game/<atlas_game_id>', methods = ['POST'])
def dashboard_remove_fav_game(atlas_game_id):
    data = {
        'user_id' : session['user_id'],
        'atlas_game_id' : request.form['atlas_game_id'],
        'atlas_game_name' : request.form['atlas_game_name']
    }

    Game.remove_favorite_game(data)

    return redirect('/dashboard')

@app.route('/add_owned_game/<atlas_game_id>', methods = ['POST'])
def add_game_owned(atlas_game_id):
    data = {
        'user_id' : session['user_id'],
        'atlas_game_id' : request.form['atlas_game_id'],
        'atlas_game_name' : request.form['atlas_game_name']
    }

    Game.add_owned_game(data)

    return redirect(f'/game/{atlas_game_id}')

@app.route('/game_detail/remove_owned_game/<atlas_game_id>', methods = ['POST'])
def game_detail_remove_owned(atlas_game_id):
    data = {
        'user_id' : session['user_id'],
        'atlas_game_id' : request.form['atlas_game_id'],
        'atlas_game_name' : request.form['atlas_game_name']
    }

    Game.remove_owned_game(data)

    return redirect(f'/game/{atlas_game_id}')

@app.route('/dashboard/remove_owned_game/<atlas_game_id>', methods = ['POST'])
def dashboard_remove_owned(atlas_game_id):
    data = {
        'user_id' : session['user_id'],
        'atlas_game_id' : request.form['atlas_game_id'],
        'atlas_game_name' : request.form['atlas_game_name']
    }

    Game.remove_owned_game(data)

    return redirect('/dashboard')

@app.route('/game_search', methods = ['POST'])
def game_search():
    search_term = request.form['search_term']

    return redirect(f'/game_results/{search_term}')

@app.route('/game_results/<string:search_term>')
def game_search_results(search_term):
    data = {
        'search_term' : search_term
    }
    search_term = search_term
    
    search_results = Game.search_for_games(data)

    return render_template('game_results.html', search_results = search_results, search_term = search_term)