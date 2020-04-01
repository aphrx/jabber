from pymongo import MongoClient
import scraper
import jobbankapply

client = MongoClient('mongodb://localhost:27017')
db = client['jabberDatabase']
users = db.users

users = users.find({'cron': { "$exists": True} })

for u in users:
    print(u['cron']['cron_job'])

    test = scraper.scrape()

    jobs = []
    employer = []
    links = []

    jobs, employer, links, count = test.search(u['cron']['cron_job'], u['cron']['cron_loc'], True)

    j = jobbankapply.apply(links)
    emails, jobs, employer = j.run()
    print(emails)
    print(jobs)
    print(employer)

    j.email(emails, jobs, employer, u['cv'], u['resume'], u['id'])
