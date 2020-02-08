from flask import Flask, render_template, url_for
import scraper

app = Flask(__name__, template_folder='templates')

test = scraper.scrape()

jobs = [[], [], []]

jobs[0], jobs[1], jobs[2], count = test.search("software developer", "Kitchener")


@app.route('/')
def index():
	return render_template('index.html', jobs=jobs, count=count)

if __name__ == "__main__":
	app.run(debug=True)