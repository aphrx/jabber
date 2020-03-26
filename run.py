import scraper
import linkedin_apply
import jobbankapply

test = scraper.scrape()

jobs = []
employer = []
links = []
selenium = []

jobs, employer, links, count = test.search("software developer", "toronto", False)


#for i in range(0, len(jobs)):
	#print(jobs[i])
	#print(employer[i])
	#print(links[i])
	#print(" ")

j = jobbankapply.apply(jobs)
j.run()

#for j in range(0, len(links)):
#	jobs[j] = linkedin_apply.apply("amalnnath20@gmail.com", "Pikachu20s", links[j])
#	jobs[j].run()
