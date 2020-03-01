import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

class scrape:
	def __init__(self):
		self.URL = None
		self.soup = None

		self.jobs = []
		self.employer = []
		self.links = []
		self.company_link = []

	def search(self, search, location, easy):
		search_r = search.replace(" ", "-")
		if easy is True:
			self.URL = "https://www.linkedin.com/jobs/search/?keywords=" + search_r + "&location=" + location + "&f_LF=f_AL"
		else:
			self.URL = "https://www.linkedin.com/jobs/search/?keywords=" + search_r + "&location=" + location
		print(self.URL)
		page =  requests.get(self.URL)
		self.soup = BeautifulSoup(page.text, "html.parser")

		self.job_title()

		return self.jobs, self.employer, self.links, len(self.jobs)

	def job_title(self):
		print("Looking")
		for div in self.soup.find_all(name="li", attrs={"class":"job-result-card"}):
			job = div.find(name="h3", attrs={"class": "job-result-card__title"})
			employe = div.find(name="a", attrs={"class": "job-result-card__subtitle-link"})
			link = div.find(name="a", attrs={"class": "result-card__full-card-link"}).attrs['href']
		
			if(job and employe and link is not None):
				self.jobs.append(job.text)
				self.employer.append(employe.text)
				self.links.append(link)
