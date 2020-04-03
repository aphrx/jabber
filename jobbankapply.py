from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import base64
import os
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from sendgrid import SendGridAPIClient
import time
import secret
import cvgen

# Global Vars
emails = []
titles = []
occ = []

class apply:
	def __init__(self, jobs):
		self.jobs = jobs

	def run(self):
		global emails, titles, occ
		for i in self.jobs:
			
			# Chromedriver options
			options = webdriver.ChromeOptions()
			options.add_argument('--ignore-certificate-errors-spki-list')
			options.add_argument('--ignore-ssl-errors')
			options.add_argument("--window-size=1920,1080")
			options.add_argument("--headless")
			driver = webdriver.Chrome(chrome_options=options)

			# Half of link, other half will be passed to function
			driver.get("https://www.jobbank.gc.ca/" + i)

			try:
				# Click button which reveals email
				elems = driver.find_element_by_class_name("btn-success")
				elems.click()

				# allow html to reload
				time.sleep(0.5)

				# get job title & employer
				title = driver.find_element_by_xpath("//span[@property='title']")
				employer = driver.find_element_by_xpath("//a[@class='external']")

				# Find all 'a' links on html page
				elems = driver.find_elements_by_xpath("//a[@href]")		
				print("Looping through links")
				for elem in elems:
					
					# if value of 'a' href contains an @ symbol, append all variables to list
					val = elem.get_attribute("href")
					if "@" in val:
						titles.append(title.get_attribute('innerHTML').strip())
						occ.append(employer.get_attribute('innerHTML'))
						emails.append(val.replace("mailto:", ""))
						break
			except:
				pass

			driver.quit()

		return emails, titles, occ

	def email(self, emails, jobs, employer, cv_data, resume, user, email):
		
		for i in range(len(emails)):
			
			# Generate email
			message = Mail(
			    from_email='hire@jabber.store',
			    to_emails=str(email),
			    subject='Resume',
			    html_content='<p>To whoever this may concern,</p><p>Attached below is a copy of a resume & cover letter for a qualified candidate for your position at ' + str(employer[i]) + ' for the position of ' + str(jobs[i]) +'. We have contacted you through your listed email at ' + str(emails[i]) +'</p><p>Thank you for your consideration,</p><p>The Jabber Team</p>')
			
			# Generate Cover Letter
			cv = cvgen.cvgen(cv_data, jobs[i], employer[i], "Toronto, ON", 'data/' + user +'CVE.pdf')
			cv.generate()

			# Generate Resume
			cv = cvgen.cvgen(resume, jobs[i], employer[i], "Toronto, ON", 'data/' + user +'RE.pdf')
			cv.generate()

			# Attach Cover Letter
			file_path = user + 'CVE.pdf'
			
			with open('data/' + file_path, 'rb') as f:
			    data = f.read()
			    f.close()
			encoded = base64.b64encode(data).decode()
			attachment = Attachment()
			attachment.file_content = FileContent(encoded)
			attachment.file_type = FileType('application/pdf')
			attachment.file_name = FileName(user + 'CVE.pdf')
			attachment.disposition = Disposition('attachment')
			attachment.content_id = ContentId('Example Content ID')
			message.attachment = attachment

			# Attach Resume
			file_path = user + 'RE.pdf'
			
			with open('data/' + file_path, 'rb') as f:
			    data = f.read()
			    f.close()
			encoded = base64.b64encode(data).decode()
			attachment = Attachment()
			attachment.file_content = FileContent(encoded)
			attachment.file_type = FileType('application/pdf')
			attachment.file_name = FileName(user + 'RE.pdf')
			attachment.disposition = Disposition('attachment')
			attachment.content_id = ContentId('Example Content ID')
			message.attachment = attachment

			# Send Email
			try:
			    sendgrid_client = SendGridAPIClient(secret.SENDGRID_KEY)
			    response = sendgrid_client.send(message)
			    print(response.status_code)
			    print(response.body)
			    print(response.headers)
			except Exception as e:
			    print(e.message)
		
		# Generate confirmation email to user
		message = Mail(
			from_email='hire@jabber.store',
			to_emails=str(email),
			subject='Resume',
			html_content='<p>Hello,</p><p>Our automated service has executed and applied you for the following roles:</p> ' + str(employer) + ' <br> ' + str(jobs) +'<p>Thank you for using our service,</p><p>The Jabber Team</p>')
		
		# Send confirmation email to user
		try:
			sendgrid_client = SendGridAPIClient(secret.SENDGRID_KEY)
			response = sendgrid_client.send(message)
			print(response.status_code)
			print(response.body)
			print(response.headers)
		except Exception as e:
			print(e.message)


