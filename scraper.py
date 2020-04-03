import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

class scrape:
	def __init__(self):
		# variables needed to scrape
		self.URL = None
		self.soup = None
		self.jobs = []
		self.employer = []
		self.links = []
		self.company_link = []

	def search(self, search, location, easy):
		search_r = search.replace(" ", "-")

		# Linkedin stuff, currently not working

		#if easy is True:
		#	self.URL = "https://www.linkedin.com/jobs/search/?keywords=" + search_r + "&location=" + location + "&f_LF=f_AL"
		#else:
		#	self.URL = "https://www.linkedin.com/jobs/search/?keywords=" + search_r + "&location=" + location
		#print(self.URL)
		#page =  requests.get(self.URL)
		#self.soup = BeautifulSoup(page.text, "html.parser")

		#self.job_title()

		# If easy apply is false, search indeed
		if easy is False:
			search_r = search.replace(" ", "-")
			self.URL = "https://ca.indeed.com/" + search_r + "-jobs-in-" + location
			print(self.URL)
			page =  requests.get(self.URL)
			self.soup = BeautifulSoup(page.text, "html.parser")
			self.job_title_indeed()

		# If easy apply is true, search Job Bank
		if easy is True:
			search_r = search.replace(" ", "+")
			self.URL = "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring="+search_r+"+in+" + location+"&sort=D"
			print(self.URL)
			page =  requests.get(self.URL)
			self.soup = BeautifulSoup(page.text, "html.parser")
			self.job_title_can()

		return self.jobs, self.employer, self.links, len(self.jobs)

	# Linkedin scraper
	def job_title(self):

		# For each job, scrape job, employee and link information
		for div in self.soup.find_all(name="li", attrs={"class":"job-result-card"}):
			job = div.find(name="h3", attrs={"class": "job-result-card__title"})
			employe = div.find(name="a", attrs={"class": "job-result-card__subtitle-link"})
			link = div.find(name="a", attrs={"class": "result-card__full-card-link"}).attrs['href']
		
			# Append to list if all are availeble
			if(job and employe and link is not None):
				self.jobs.append(job.text)
				self.employer.append(employe.text)
				self.links.append(link)

	# Indeed scraper
	def job_title_indeed(self):
		for div in self.soup.find_all(name="div", attrs={"class":"row"}):

			# Find job title and append to list
			for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
				self.jobs.append(a["title"])

			# Find employer and append to list
			company = div.find_all(name="span", attrs={"class":"company"})
			if len(company) > 0:
				for b in company:
					self.employer.append(b.text.strip())
			else:
				sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
				for span in sec_try:
					self.employer.append(span.text.strip())
			
			# Append link for job to list
			self.links.append("https://ca.indeed.com/rc/clk?jk=" + str(div["data-jk"]))

	# Job bank scraper
	def job_title_can(self):

		# For each job, append link to variable fields, (job and employer can only be found in jobbankapply.py)
		for div in self.soup.find_all(name="article"):
			for job in div.find_all(name="a", attrs={"class":"resultJobItem"}):
				j = job['href']
				self.jobs.append(j)
				self.employer.append(j)
				self.links.append(j)
				
