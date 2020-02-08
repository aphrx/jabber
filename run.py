<<<<<<< HEAD
import scraper

test = scraper.scrape()

jobs = []
employer = []
links = []

jobs, employer, links = test.search("software developer", "toronto")

for i in range(0, len(jobs)):
=======
import scraper

test = scraper.scrape()

jobs = []
employer = []
links = []

jobs, employer, links = test.search("software developer", "toronto")

for i in range(0, len(jobs)):
>>>>>>> 39b4a0e4b1d4f844fa9ce12a06c086aa71b75ea0
	print(jobs[i] + "\n" + employer[i] + "\n" + links[i] + "\n")