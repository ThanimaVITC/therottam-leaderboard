import os
from flask import Flask
from flask_pymongo import PyMongo

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder=os.path.join(basedir, '..', 'static'))
app.secret_key = os.environ.get('SECRET_KEY', 'leaderboard_secret_key')

mongo_uri = os.environ.get('MONGO_DB_URI', 'mongodb://localhost:27017/leaderboard')
app.config['MONGO_URI'] = mongo_uri
mongo = PyMongo(app)

from app.routes.leaderboard import leaderboard_bp
from app.routes.admin import admin_bp

app.register_blueprint(leaderboard_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
