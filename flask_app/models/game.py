from flask_app.config.mysqlconnection import MySQLConnection
import requests
import os
import json
from flask_app import app
from flask import flash, request, jsonify

class Game:
    def __init__(self, db_data):
        self.atlas_game_id = db_data['atlas_game_id']
        self.atlas_game_name = db_data['atlas_game_name']

    @classmethod
    def get_game_info(cls, data):
        results = requests.get(f'https://api.boardgameatlas.com/api/search?ids={data["atlas_game_id"]}&client_id={os.environ.get("boardgame_atlas_api")}')
        
        return results.json()

    @classmethod
    def get_random_game(cls):
        results = requests.get(f'https://api.boardgameatlas.com/api/search?random=true&client_id={os.environ.get("boardgame_atlas_api")}')

        return results.json()

    @classmethod
    def search_for_games(cls, data):
        results = requests.get(f'https://api.boardgameatlas.com/api/search?name={data["search_term"]}&limit=3&client_id={os.environ.get("boardgame_atlas_api")}')
        
        results = results.json()
        results = results['games']
        search_results=[]

        for game in results:
            search_results.append(game)

        return search_results

    @classmethod
    def add_favorite_game(cls, data):
        query = 'INSERT INTO users_favorite_games (user_id, atlas_game_id, atlas_game_name) VALUES (%(user_id)s, %(atlas_game_id)s, %(atlas_game_name)s);'

        return MySQLConnection('find_players').query_db(query, data)

    @classmethod
    def is_favorite_game(cls, data):
        is_favorite = False
        
        query = 'SELECT * FROM users_favorite_games WHERE user_id = %(user_id)s AND atlas_game_id = %(atlas_game_id)s'

        check_favorite = MySQLConnection('find_players').query_db(query, data)

        if check_favorite:
            is_favorite = True
        
        return is_favorite

    @classmethod
    def get_favorite_games(cls, data):
        query = 'SELECT * FROM users_favorite_games WHERE user_id=%(user_id)s;'
        results =  MySQLConnection('find_players').query_db(query, data)
        favorite_games = []
        for game in results:
            favorite_games.append(cls(game))

        return favorite_games
    
    @classmethod
    def remove_favorite_game(cls, data):
        query = 'DELETE FROM users_favorite_games WHERE user_id = %(user_id)s AND atlas_game_id = %(atlas_game_id)s'
        return MySQLConnection('find_players').query_db(query, data)

    @classmethod
    def add_owned_game(cls, data):
        query = 'INSERT INTO users_own_games (user_id, atlas_game_id, atlas_game_name) VALUES (%(user_id)s, %(atlas_game_id)s, %(atlas_game_name)s);'

        return MySQLConnection('find_players').query_db(query, data)

    @classmethod
    def get_owned_games(cls, data):
        query = 'SELECT * FROM users_own_games WHERE user_id=%(user_id)s;'
        results =  MySQLConnection('find_players').query_db(query, data)
        owned_games = []
        for game in results:
            owned_games.append(cls(game))

        return owned_games

    @classmethod
    def is_owned_game(cls, data):
        is_owned = False
        
        query = 'SELECT * FROM users_own_games WHERE user_id = %(user_id)s AND atlas_game_id = %(atlas_game_id)s'

        check_owned = MySQLConnection('find_players').query_db(query, data)

        if check_owned:
            is_owned = True
        
        return is_owned

    @classmethod
    def remove_owned_game(cls, data):
        query = "DELETE FROM users_own_games WHERE user_id = %(user_id)s AND atlas_game_id = %(atlas_game_id)s"
        
        return MySQLConnection('find_players').query_db(query, data)
    