from flask import redirect, render_template, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.game import Game
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/newplayer', methods = ['GET'])
def new_user_page():

    return render_template('player_form.html')

@app.route('/newplayer', methods = ['POST'])
def new_user():
    if not User.validate_registration(request.form):
        return redirect('/newplayer')

    pw_hash = bcrypt.generate_password_hash(request.form['user_password'])

    data = {
        'name': request.form['name'],
        'user_email': request.form['user_email'],
        'pw_hash': pw_hash,
        'nickname' : request.form['nickname'],
        'zip_code' : request.form['zip_code'],
        'favorite_game' : request.form['favorite_game'],
        'play_preference' : request.form['play_preference']
    }

    user_id = User.add_user(data)

    session['user_id'] = user_id
    session['name'] = request.form['name']
    session['nickname'] = request.form['nickname']
    session['user_email'] = request.form['user_email']

    return redirect ('/dashboard')

@app.route('/login', methods = ['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/login')
    data = {'email': request.form['user_email']}

    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash('Invalid Email/Password', 'login')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['user_password']):
        flash('Invalid Email/Password', 'login')
        return redirect('/login')
    
    session['user_id'] = user_in_db.id
    session['name'] = user_in_db.name
    session['nickname'] = user_in_db.nickname

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if not User.logged_in():
        return redirect('/home')

    data = {
        'user_id' : session['user_id']
    }

    favorite_users = User.get_all_favorite_users(data)
    favorite_games = Game.get_favorite_games(data)
    owned_games = Game.get_owned_games(data)

    session_user_id = session['user_id']
    

    return render_template('player_dashboard.html', favorite_users = favorite_users, favorite_games = favorite_games, owned_games = owned_games, session_user_id = session_user_id)

@app.route('/add_favorite_user/<int:user_id>', methods=['POST'])
def add_fav_user(user_id):
    data = {
        'user_id' : session['user_id'],
        'favorite_user_id' : request.form['favorite_user_id']
    }

    User.add_favorite(data)

    return redirect(f'/player/{user_id}')

@app.route('/player_details/remove_favorite_user/<int:user_id>', methods=['POST'])
def player_details_remove_fav_user(user_id):
    data = {
        'user_id' : session['user_id'],
        'favorite_user_id' : request.form['favorite_user_id']
    }

    User.remove_favorite_user(data)

    return redirect(f'/player/{user_id}')

@app.route('/dashboard/remove_favorite_user/<int:user_id>', methods=['POST'])
def dashboard_remove_fav_user(user_id):
    data = {
        'user_id' : session['user_id'],
        'favorite_user_id' : user_id
    }

    User.remove_favorite_user(data)

    return redirect('/dashboard')

@app.route('/player/<int:user_id>')
def player_info(user_id):
    if not User.logged_in():
        return redirect('/home')
        
    favorite_search_data = {
        'user_id' : session['user_id'],
        'favorite_user_id' : user_id,
    }
    
    data = {
        'user_id' : user_id
    }
    is_favorite = User.is_favorite_user(favorite_search_data)

    user_info = User.get_user(data)

    return render_template('player_details.html', user_info = user_info, is_favorite = is_favorite)

@app.route('/player/edit/<int:user_id>')
def edit_player(user_id):
    if not User.logged_in():
        return redirect('/home')

    data = {
        'user_id' : user_id,
    }

    user_info = User.get_user(data)

    return render_template('player_edit.html', user_info = user_info)

@app.route('/submit_player_edit/<int:user_id>', methods=['POST'])
def submit_player_edits(user_id):
    data = {
        'user_id': request.form['user_id'],
        'name': request.form['name'],
        'user_email': request.form['user_email'],
        'nickname' : request.form['nickname'],
        'zip_code' : request.form['zip_code'],
        'favorite_game' : request.form['favorite_game'],
        'play_preference' : request.form['play_preference']
    }

    if not User.submit_profile_edits(data):
        return redirect(f'/player/edit/{user_id}')
    
    return redirect(f'/player/edit/{user_id}')

@app.route('/player_search', methods = ['POST'])
def player_zip_search():
    if not User.logged_in():
        return redirect('/home')

    search_term = request.form['search_term']

    return redirect(f'/player_results/{search_term}')

@app.route('/player_results/<int:search_term>')
def player_results(search_term):
    if not User.logged_in():
        return redirect('/home')
    data = {
        'zip_code' : search_term
    }

    search_results = User.search_by_zip(data)

    return render_template('player_results.html', search_results = search_results, search_term = search_term)

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user_id', None)
    return redirect('/home')