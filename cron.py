# Cron testing (not for deployment)

from pymongo import MongoClient
import scraper
import jobbankapply

# connect to mongodb and get users
client = MongoClient('mongodb://localhost:27017')
db = client['jabberDatabase']
users = db.users

# find users who signed up for cron job
users = db.users.find({'cron': { "$exists": True} })

# for users who have signed up for cron job
for u in users:
    print(u['cron']['cron_job'])

    # Scrape for jobs that user is interested in
    test = scraper.scrape()
    jobs = []
    employer = []
    links = []
    jobs, employer, links, count = test.search(u['cron']['cron_job'], u['cron']['cron_loc'], True)
    j = jobbankapply.apply(links)
    emails, jobs, employer = j.run()

    # print fetched data and email recruiters on behalf of user
    print(emails)
    print(jobs)
    print(employer)
    j.email(emails, jobs, employer, u['cv'], u['resume'], u['id'])
