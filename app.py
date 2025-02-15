try:
    import secret
except ImportError:
    print('Create secret.py with GOOGLE credentials..exiting')
    exit(1)
import os
import json
import requests
import sys
import linkedin_apply
import scraper
import jobbankapply
import cvgen
from user import User
from datetime import datetime
from flask_pymongo import PyMongo
from flask_apscheduler import APScheduler
from oauthlib.oauth2 import WebApplicationClient
from flask import (
    Flask,
    send_from_directory,
    redirect,
    request,
    url_for,
    render_template,
    session
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

app = Flask(__name__, template_folder='templates')
# We can make this secret key as environ variable later to sign cookies
app.secret_key = "test" #os.environ.get("SECRET_KEY")# or os.urandom(24)
app.config["MONGO_URI"] = "mongodb://localhost:27017/jabberDatabase"
mongo = PyMongo(app)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)
# OAuth 2 client setup
client = WebApplicationClient(secret.GOOGLE_CLIENT_ID)
account = "Login"

scheduler = APScheduler()

@app.route("/")
def index():
    if 'user_id' in session:
        print(session['user_id'])
    return render_template("index.html")


@app.route("/postings")
def postings():
    # If not logged in, show Login button
    global account
    account = "Login"
    if 'user_id' in session:
        account = "Settings"
    
    # By default, scrape for Developer jobs in toronto
    test = scraper.scrape()
    jobs = [[], [], []]
    jobs[0], jobs[1], jobs[2], count = test.search("Developer", "Toronto", False)
    return render_template('job_list.html',
                           jobs=jobs,
                           count=count,
                           account=account)


@app.route("/easy-apply")
def easy_apply():
    # If not logged in, show Login button, otherwise show Settings and redirect to easy apply page
    global account
    account = "Login"
    if 'user_id' in session:
        account = "Settings"
        return render_template('easy-apply.html', account=account)
    return redirect(url_for("login"))


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'user_id' in session:

        # if linkedin form was updated, update in mongodb
        if request.method == 'POST' and 'pwd' in request.form:
            email = request.form['email']
            pwd = request.form['pwd']
            linkedin_info = {"email": email, "pwd": pwd}
            mongo.db.users.update_one({"id": session['user_id']},
                                    {"$set": {
                                        "linkedIn": linkedin_info
                                    }})
            return redirect(url_for("profile"))
        
        # if cv form was submitted, update in mongodb
        elif request.method == 'POST' and 'cv' in request.form:
            cv_data = request.form['cv']
            mongo.db.users.update_one({"id": session['user_id']},
                                    {"$set": {
                                        "cv": cv_data
                                    }})
            return redirect(url_for("profile"))
        
        # If resume form was submitted, update in mongodb
        elif request.method == 'POST' and 'resume' in request.form:
            resume_data = request.form['resume']
            mongo.db.users.update_one({"id": session['user_id']},
                                    {"$set": {
                                        "resume": resume_data
                                    }})
            return redirect(url_for("profile"))
        
        # if cron form was submitted, update in mongodb
        elif request.method == 'POST' and 'keyword_cron' in request.form:
            keyword_cron = request.form['keyword_cron']
            location_cron = request.form['location_cron']
            cron = {"cron_job": keyword_cron, "cron_loc": location_cron}
            mongo.db.users.update_one({"id": session['user_id']},
                                    {"$set": {
                                        "cron": cron
                                    }})
            return redirect(url_for("profile"))
        else:  # GET
            linkedIn_ok = "false"
            cv_ok = "false"
            cv_data = ""
            resume_ok = "false"
            resume_data = ""

            # If user logged in, fetch data from mongodb
            if 'user_id' in session:
                user = mongo.db.users.find_one({"id": session['user_id']})
                if user["cv"] != "":
                    cv_ok = "true"
                    cv_data = user["cv"]
                if user["resume"] != "":
                    resume_ok = "true"
                    resume_data = user["resume"]
            return render_template("profile.html",
                                username=current_user.name,
                                email=current_user.email,
                                pic=current_user.profile_pic,
                                linkedIn_ok=linkedIn_ok,
                                cv_ok=cv_ok,
                                cv_data=cv_data,
                                resume_ok=resume_ok,
                                resume_data=resume_data,
                                account="Settings")


def get_google_provider_cfg():
    return requests.get(secret.GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    if 'user_id' in session:
        return redirect(url_for("profile"))
    else:
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
    session['user_id'] = unique_id
    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    session.pop('user_id', None)
    logout_user()  # built-in from flask-login lib
    return redirect(url_for("index"))


@app.route('/search', methods=['POST'])
def search():
    # If not logged in, show Login button, otherwise show Settinsg button
    global account
    account = "Login"
    if 'user_id' in session:
        account = "Settings"

    # Get keyword and location from form and find jobs using scraper for jobs
    keywrd = request.form['keywrd']
    location = request.form['location']
    test = scraper.scrape()
    jobs = [[], [], []]
    jobs[0], jobs[1], jobs[2], count = test.search(keywrd, location, False)

    # send arrays to html template to display accordingly
    return render_template('job_list.html',
                           jobs=jobs,
                           count=count,
                           account=account)

@app.route('/gen-cv/<string:job>/<string:employer>')
def gen_cv(job, employer):
    if 'user_id' in session:
        # Find user's cv template
        user = mongo.db.users.find_one({"id": session['user_id']})
        if user["cv"] != "":
            cv_data = user["cv"]
        cv_data = cv_data.encode('latin-1', 'replace').decode('latin-1')

        # Generate cv given cv, employer, job and location
        cv = cvgen.cvgen(cv_data, job, employer, "Toronto, ON", 'data/' + user['id'] +'CV.pdf')
        cv.generate()
        
        # Download CV
        return send_from_directory(directory="data",
                               filename= user['id'] +'CV.pdf',
                               mimetype='application/pdf')
    return redirect(url_for("login"))

@app.route('/search-easy', methods=['POST'])
def search_easy():

    # Keep track of when easy apply is deploted
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Easy Apply Executed at " + dt_string)
    
    output = "Applied to X jobs"

    # If not logged in, show Login button
    global account
    account = "Login"
    if 'user_id' in session:

        # Find user entry from session
        user = mongo.db.users.find_one({"id": session['user_id']})
        account = "Settings"

        # Get CV if not empty
        if user["cv"] != "":
            cv_data = user["cv"]
        cv_data = cv_data.encode('latin-1', 'replace').decode('latin-1')

        # Get resume if not empty
        if user["resume"] != "":
            resume = user["resume"]
        resume = resume.encode('latin-1', 'replace').decode('latin-1')

        # Get keyword and location from form and use them to scrape for jobs
        keywrd = request.form['keywrd']
        location = request.form['location']
        test = scraper.scrape()
        jobs = [[], [], []]
        jobs[0], jobs[1], jobs[2], count = test.search(keywrd, location, True)
        j = jobbankapply.apply(jobs[2])
        emails, jobs, employer = j.run()

        # email users on list and redirect to page
        j.email(emails, jobs, employer, cv_data, resume, session['user_id'], user["email"])
        return render_template('easy-apply.html', count=count, account=account, output=output)
    return redirect(url_for("login"))

# flask-login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id, mongo)

# redirect home if unauth
@login_manager.unauthorized_handler
def unauthorized():
    return render_template("index.html", login_err="yep")

@app.route("/cron")
def scheduled():

    # print out time that cron job was deployed in console
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Cron Job Executed at " + dt_string)

    # Find users who signed up for cron job
    users = mongo.db.users.find({'cron': { "$exists": True} })

    # For each user who has signed up for cron job, find jobs they are interested ibn
    for u in users:
        test = scraper.scrape()
        jobs = []
        employer = []
        links = []
        jobs, employer, links, count = test.search(u['cron']['cron_job'], u['cron']['cron_loc'], True)
        j = jobbankapply.apply(links)
        emails, jobs, employer = j.run()

        # find user's cv and resume
        cv_data = u['cv']
        cv_data = cv_data.encode('latin-1', 'replace').decode('latin-1')
        resume = u['resume']
        resume = resume.encode('latin-1', 'replace').decode('latin-1')

        # apply for jobs on behalf of user
        j.email(emails, jobs, employer, cv_data, resume, u['id'], u['email'])

# start scheduler once a day for testing purpose (once a week for regular deployment)
scheduler.add_job(id='scheduled', func=scheduled, trigger = 'interval', hours = 24)
scheduler.start()

if __name__ == "__main__":
    app.run(ssl_context="adhoc")

