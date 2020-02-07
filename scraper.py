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

	def search(self, search, location):
		search_r = search.replace(" ", "-")
		self.URL = "https://ca.indeed.com/" + search_r + "-jobs-in-" + location
		print(self.URL)
		page =  requests.get(self.URL)
		self.soup = BeautifulSoup(page.text, "html.parser")

		self.job_title()

		return self.jobs, self.employer, self.links

	def job_title(self):
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

	