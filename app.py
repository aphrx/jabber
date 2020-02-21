try:
    import secret
except:
    print('Create secret.py with GOOGLE credentials')
import os
import json
import requests
import scraper
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, redirect, request, url_for, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)


app = Flask(__name__, template_folder='templates')
# We can make this secret key as environ variable later to sign cookies if we want
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)
# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

@app.route('/')
def index():
        test = scraper.scrape()
        jobs = [[], [], []]
        jobs[0], jobs[1], jobs[2], count = test.search("software developer", "Kitchener")
	return render_template('index.html', jobs=jobs, count=count)

# flask-login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == "__main__":
	app.run(debug=True)
