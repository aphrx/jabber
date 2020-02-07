import scraper

test = scraper.scrape()

jobs = []
employer = []
links = []

jobs, employer, links = test.search("software developer", "toronto")

for i in range(0, len(jobs)):
	print(jobs[i] + "\n" + employer[i] + "\n" + links[i] + "\n")