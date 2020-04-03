# Test scraper

import scraper
import jobbankapply

# Find JobBank urls for applicable jobs
test = scraper.scrape()
jobs = []
employer = []
links = []
jobs, employer, links, count = test.search("software developer", "toronto", True)

# find job information and print out
j = jobbankapply.apply(links)
emails, jobs, employer = j.run()
print(emails)
print(jobs)
print(employer)

