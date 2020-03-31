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

emails = []
titles = []
occ = []

class apply:
	def __init__(self, jobs):
		self.jobs = jobs

	def run(self):
		global emails, titles, occ
		for i in self.jobs:
			options = webdriver.ChromeOptions()
			options.add_argument('--ignore-certificate-errors-spki-list')
			options.add_argument('--ignore-ssl-errors')
			options.add_argument("--window-size=1920,1080")
			options.add_argument("--headless")

			driver = webdriver.Chrome(chrome_options=options)
			driver.get("https://www.jobbank.gc.ca/" + i)

			try:
				elems = driver.find_element_by_class_name("btn-success")
				elems.click()

				time.sleep(0.5)

				title = driver.find_element_by_xpath("//span[@property='title']")
				employer = driver.find_element_by_xpath("//a[@class='external']")

				elems = driver.find_elements_by_xpath("//a[@href]")
				e = []
			
				print("looping")
				for elem in elems:
					
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

	def email(self, emails, jobs, employer, cv_data, resume, user):
		print("emailing")
		for i in range(len(emails)):
			
			message = Mail(
			    from_email='hire@jabber.store',
			    to_emails=secret.SENDER,
			    subject='Resume',
			    #html_content='<p>To whoever this may concern,</p><p>Attached below is a copy of a resume & cover letter for a qualified candidate for your position. We have contacted you through your listed email at the job bank</p><p>Thank you for your consideration,</p><p>The Jabber Team</p>')
				html_content='Attached below is a copy of a resume & cover letter for a qualified candidate for your position at ' + str(employer[i]) + ' for the position of ' + str(jobs[i]) +'. We have contacted you through your listed email at ' + str(emails[i]))
			
			cv = cvgen.cvgen(cv_data, jobs[i], employer[i], "Toronto, ON", 'data/' + user +'CVE.pdf')
			cv.generate()

			cv = cvgen.cvgen(resume, jobs[i], employer[i], "Toronto, ON", 'data/' + user +'RE.pdf')
			cv.generate()

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

			try:
			    sendgrid_client = SendGridAPIClient(secret.SENDGRID_KEY)
			    response = sendgrid_client.send(message)
			    print(response.status_code)
			    print(response.body)
			    print(response.headers)
			except Exception as e:
			    print(e.message)


