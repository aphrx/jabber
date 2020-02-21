try:
    import secret
except ImportError:
    print('Create secret.py with GOOGLE credentials')
import os
import json
import requests
import scraper
from user import User
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
app.config["MONGO_URI"] = "mongodb://localhost:27017/jabberDatabase"
mongo = PyMongo(app)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)
# OAuth 2 client setup
client = WebApplicationClient(secret.GOOGLE_CLIENT_ID)

# @app.route('/')
# def index():
#     test = scraper.scrape()
#     jobs = [[], [], []]
#     jobs[0], jobs[1], jobs[2], count = test.search("software developer",
#                                                    "Kitchener")
#     return render_template('index.html', jobs=jobs, count=count)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return ("<p>Hello, {}! You're logged in! Email: {}</p>"
                "<div><p>Google Profile Picture:</p>"
                '<img src="{}" alt="Google profile pic"></img></div>'
                '<a class="button" href="/logout">Logout</a>'.format(
                    current_user.name, current_user.email,
                    current_user.profile_pic))
    else:
        return '<a class="button" href="/login">Google Login</a>'


def get_google_provider_cfg():
    return requests.get(secret.GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")  # Google calls this function after authorization
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code)
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(secret.GOOGLE_CLIENT_ID, secret.GOOGLE_CLIENT_SECRET),
    )
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens, let's find and hit the URL from Google
    # that gives you the user's profile information, including their
    # Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        print("User is not verified")
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided by google
    user = User(id_=unique_id,
                name=users_name,
                email=users_email,
                profile_pic=picture)

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id, mongo):
        User.create(unique_id, users_name, users_email, picture, mongo)
    # Begin user session by logging the user in
    login_user(user)
    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# flask-login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id, mongo)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
