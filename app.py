from flask import Flask, request, url_for, jsonify, session, g, send_from_directory
import mysql.connector
from dotenv import load_dotenv
from flask_limiter import Limiter
import json
import os
from flask_cors import CORS, cross_origin

load_dotenv()

app = Flask(__name__)
CORS(app)  # , origins=['http://192.168.13.1:5173/'])  replace with actual domain


def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=os.getenv('DATABASE_URL'),
                user="REMOTE_USER",
                password="REMOTE_USER_PASSWORD",
                database="Marketplace",
                port=3306
            )
        except Exception as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    return g.db


@app.before_request
def before_request():
    get_db()

    if is_excluded_route():
        return
    if request.method == 'OPTIONS':
        return
    token = request.headers.get('token')
    if token and browser_token_required(token):
        return
    else:
        return jsonify({'message': 'You are not allowed!'}), 401


def is_excluded_route():
    excluded_routes = ['/', '/image/<image_token>']
    if request.url_rule is not None:
        return request.url_rule.rule in excluded_routes
    return False


@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()


@app.route('/', methods=['POST'])
def genrate_token():  # verify if it's from my domain, by giving a token and verifying it everytime any request is sent
    if request.headers.get('token'):
        if browser_token_required(request.headers['token']):
            return jsonify({'message': 'token still valid!'}), 202

    token = decorators.create_browser_only_token()
    return jsonify({'token': token}), 200


@app.route('/home', methods=['POST'])
@optional_jwt
def homepage():
    db = g.db
    cursor = db.cursor()
    authorized = g.authorized
    parties = Parties.get_parties_by_newest(cursor, 40)
    print(parties)
    if authorized:
        personalized = []
        user = g.user_data['username']
        response_data = {
            'message': 'success',
            'for_you': personalized,
            'newest': newest_listings
        }
        return jsonify(response_data)
    else:
        response_data = {
            'newest': newest_listings
        }
        return jsonify(response_data)


@app.route('/testing')
def serve_avatar():
    return 'testing'


@app.route('/myip')
def myip():
    client_ip = request.remote_addr
    return f'Your IP address is {client_ip}!'


app.register_blueprint(user_routes)
app.register_blueprint(image_routes)
app.register_blueprint(listing_routes)

if __name__ == '__main__':
    app.run()
