import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://ca.indeed.com/new-grad-software-jobs-in-Toronto"

page =  requests.get(URL)

soup = BeautifulSoup(page.text, "html.parser")
#print(soup)

jobs = []
jobCount = 0
employer = []
employerCount = 0
links = []
company_link = []
link_counter = 0

def job_title(soup):
	global jobCount, employerCount
	for div in soup.find_all(name="div", attrs={"class":"row"}):
		for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
			jobs.append(a["title"])
			jobCount = jobCount + 1
		company = div.find_all(name="span", attrs={"class":"company"})
		if len(company) > 0:
			for b in company:
				employer.append(b.text.strip())
				employerCount = employerCount + 1
		else:
			sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
			for span in sec_try:
				employer.append(span.text.strip())
				employerCount = employerCount + 1
		links.append("https://ca.indeed.com/rc/clk?jk=" + str(div["data-jk"]))			

job_title(soup)

for i in range(0, jobCount):
	print(jobs[i])
	print(employer[i])
	#print(link_counter)
	print(links[i] + "\n")