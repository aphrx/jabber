import scraper
import linkedin_apply
import jobbankapply

test = scraper.scrape()

jobs = []
employer = []
links = []

jobs, employer, links, count = test.search("software developer", "toronto", True)

j = jobbankapply.apply(links)
emails, jobs, employer = j.run()
print(emails)
print(jobs)
print(employer)

#j.email(emails, jobs, employer)