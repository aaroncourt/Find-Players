from flask_app.config.mysqlconnection import MySQLConnection
from flask_app import app
from flask import flash, session
import re
import requests
import logging

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, db_data):
    # data object from users.py passed into db_data
        self.id = db_data['id']
        self.name= db_data['name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.nickname = db_data['nickname']
        self.zip_code = db_data['zip_code']
        self.city = db_data['city']
        self.favorite_game = db_data['favorite_game']
        self.play_preference = db_data['play_preference']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @staticmethod
    def validate_registration(response):
    # request.form data passed into response
        is_valid = True
        query = "SELECT email FROM users;"
        results = MySQLConnection('find_players').query_db(query)

        # name validation
        if not str.isalnum(response['name']):
            flash('Please enter a name that contains only alphanumerica characters (a-z, 0-9) and no punctuation.', 'registration')
            is_valid = False
        elif len(response['name']) < 2:
            flash('Please enter a name that is at least two characters in length.', 'registration')
            is_valid = False
        
        # email validation
        if len(response['user_email']) < 1:
            flash('Please enter an email address.', 'registration')
            is_valid = False
        elif not EMAIL_REGEX.match(response['user_email']): 
            flash('Invalid email address format.', 'registration')
            is_valid = False
        for email in results:
            if response['user_email'] == email['email']:
                flash('Email already in use.', 'registration')
                is_valid = False
                break

        # password validation
        if len(response['user_password']) < 8:
            flash('Please enter a password that is at least 8 characters.', 'registration')
            is_valid = False

        if not response['user_password'] == response['confirm_pass']:
            flash('Your password entries do not match.', 'registration')
            is_valid = False

        # nickname validation
        if len(response['nickname']) < 2:
            flash('Please enter a nickname that is at least two characters in length.', 'registration')
            is_valid = False
        
        # zip code validation
        if len(response['zip_code']) != 5:
            flash('Please enter your five digit zip code.', 'registration')
            is_valid = False

        # favorite game validation
        if len(response['zip_code']) < 2:
            flash('Please enter your favorite board game, even if it is from your childhood, that is at least two characters in length :)', 'registration')
            is_valid = False

        # preferred play validation
        if len(response['play_preference']) == 'none':
            flash('Please choose your preferred way to play board games. :)', 'registration')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(login):
    # data object from users.py passed into login
        is_valid = True
        if len(login['user_email']) < 1:
            flash('Invalid Email/Password', 'login')
            is_valid = False 

        if len(login['user_password']) < 1:
            flash('Invalid Email/Password', 'login')
            is_valid = False

        return is_valid

    @staticmethod
    def logged_in():
        is_valid = True
        if session.get('user_id') == None:
            flash('You must be logged in to acccess that page!', 'denied')
            is_valid = False
        return is_valid


    @classmethod
    def add_user(cls, data):
        results = requests.get(f'https://www.zipcodeapi.com/rest/v5hqMECYHXO5GxC9WXxOlVLsaTHIw5CuSS7XMBJd0IALZeM2rGOlm7CwPNc1Fddo/info.json/{data["zip_code"]}/degrees')
                
        city_results = results.json()
        data['city'] = city_results['city']

        query = 'INSERT INTO users (name, email, password, nickname, zip_code, city, favorite_game, play_preference) VALUES (%(name)s, %(user_email)s, %(pw_hash)s, %(nickname)s, %(zip_code)s, %(city)s, %(favorite_game)s, %(play_preference)s);'
        
        return MySQLConnection('find_players').query_db(query, data)

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = MySQLConnection('find_players').query_db(query, data)

        if len(result) < 1:
            return False

        return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = MySQLConnection('find_players').query_db(query, data)
        logging.debug(result)

        if result == False:
            return False

        return cls(result[0])

    @classmethod
    def add_favorite(cls, data):
        query = 'INSERT INTO users_has_user_favorites (user_id, favorite_user_id) VALUES (%(user_id)s, %(favorite_user_id)s)'
        
        return MySQLConnection('find_players').query_db(query, data)

    @classmethod
    def is_favorite_user(cls, data):
        is_favorite = False
        
        query = 'SELECT * FROM users_has_user_favorites WHERE user_id = %(user_id)s AND favorite_user_id = %(favorite_user_id)s'

        check_favorite = MySQLConnection('find_players').query_db(query, data)

        if check_favorite:
            is_favorite = True
        
        return is_favorite
    
    @classmethod
    def get_all_favorite_users(cls, data):
        query = 'SELECT user.id AS user_id, user.name AS user_name, favorites.favorite_user_id AS favorite_id, users2.name AS favorite_name, users2.nickname AS favorite_nickname FROM users AS user JOIN users_has_user_favorites AS favorites ON user.id = favorites.user_id JOIN users as users2 ON users2.id = favorites.favorite_user_id WHERE user.id = %(user_id)s'

        result = MySQLConnection('find_players').query_db(query, data)

        return result

    @classmethod
    def remove_favorite_user(cls, data):
        query = "DELETE FROM users_has_user_favorites WHERE user_id = %(user_id)s AND favorite_user_id = %(favorite_user_id)s"
        
        return MySQLConnection('find_players').query_db(query, data)

    @classmethod
    def search_by_zip(cls, data):
        results = requests.get(f'https://www.zipcodeapi.com/rest/v5hqMECYHXO5GxC9WXxOlVLsaTHIw5CuSS7XMBJd0IALZeM2rGOlm7CwPNc1Fddo/radius.json/{data["zip_code"]}/10/mile')

        zip_results = results.json()
        zip_results = zip_results['zip_codes']
        
        zip_codes = []
        for result in zip_results:
            zip_code = result['zip_code']
            zip_code = str(zip_code)
            zip_codes.append(zip_code)

        zip_code_string = ','.join(zip_codes)

        query = f'SELECT id, nickname, favorite_game, play_preference FROM users WHERE zip_code IN ({zip_code_string})'

        return MySQLConnection('find_players').query_db(query, data)

    @classmethod
    def submit_profile_edits(cls, response):
    # request.form data passed into response
        is_valid = True

        response['favorite_game'] = response['favorite_game'].capitalize()

        user_email_query = "SELECT email FROM users WHERE id = %(user_id)s;"
        email_query= MySQLConnection('find_players').query_db(user_email_query, response)
        
        # name validation
        if not str.isalnum(response['name']):
            flash('Please enter a name that contains only alphanumerica characters (a-z, 0-9) and no punctuation.', 'registration')
            is_valid = False
        elif len(response['name']) < 2:
            flash('Please enter a name that is at least two characters in length.', 'registration')
            is_valid = False
        

        # email validation
        if email_query[0]['email'] != response['user_email']:
            if len(response['user_email']) < 1:
                flash('Please enter an email address.', 'registration')
                is_valid = False
            elif not EMAIL_REGEX.match(response['user_email']): 
                flash('Invalid email address format.', 'registration')
                is_valid = False
            else:       
                query1 = "SELECT email FROM users;"
                email_results = MySQLConnection('find_players').query_db(query1)

                for email in email_results:
                    if response['user_email'] == email['email']:
                        flash('Email already in use.', 'registration')
                        is_valid = False
                        break

        # nickname validation
        if len(response['nickname']) < 2:
            flash('Please enter a nickname that is at least two characters in length.', 'registration')
            is_valid = False
        
        # zip code validation
        if len(response['zip_code']) != 5:
            flash('Please enter your five digit zip code.', 'registration')
            is_valid = False

        # favorite game validation
        if len(response['favorite_game']) < 2:
            flash('Please enter your favorite board game, even if it is from your childhood, that is at least two characters in length :)', 'registration')
            is_valid = False

        # preferred play validation
        if len(response['play_preference']) == 'none':
            flash('Please choose your preferred way to play board games. :)', 'registration')
            is_valid = False

        if is_valid == False:
            return is_valid

        results = requests.get(f'https://www.zipcodeapi.com/rest/v5hqMECYHXO5GxC9WXxOlVLsaTHIw5CuSS7XMBJd0IALZeM2rGOlm7CwPNc1Fddo/info.json/{response["zip_code"]}/degrees')
        
        city_results = results.json()
        response['city'] = city_results['city']
        
        query2 = 'UPDATE users SET name = %(name)s, email = %(user_email)s, nickname = %(nickname)s, zip_code = %(zip_code)s, city = %(city)s, favorite_game = %(favorite_game)s, play_preference = %(play_preference)s WHERE id = %(user_id)s;'

        updated =  MySQLConnection('find_players').query_db(query2, response)

        flash('Your profile has been updated.', 'update')
        
        return updated
