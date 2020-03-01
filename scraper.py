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

		if easy is False:
			search_r = search.replace(" ", "-")
			self.URL = "https://ca.indeed.com/" + search_r + "-jobs-in-" + location
			print(self.URL)
			page =  requests.get(self.URL)
			self.soup = BeautifulSoup(page.text, "html.parser")

			self.job_title_indeed()

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

	def job_title_indeed(self):
		for div in self.soup.find_all(name="div", attrs={"class":"row"}):
			for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
				self.jobs.append(a["title"])

			company = div.find_all(name="span", attrs={"class":"company"})
			if len(company) > 0:
				for b in company:
					self.employer.append(b.text.strip())
			else:
				sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
				for span in sec_try:
					self.employer.append(span.text.strip())
			self.links.append("https://ca.indeed.com/rc/clk?jk=" + str(div["data-jk"]))