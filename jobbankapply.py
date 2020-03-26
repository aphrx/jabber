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

emails = []

class apply:
	def __init__(self, jobs):
		self.jobs = jobs

	def run(self):
		global emails
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

				time.sleep(1)

				elems = driver.find_elements_by_xpath("//a[@href]")
				e = []
			
				for elem in elems:
				    val = elem.get_attribute("href")

				    if "@" in val:
				        emails.append(val.replace("mailto:", ""))
				        break
			except:
				pass

		return emails

	def email(self, emails):
		for e in emails:
			message = Mail(
			    from_email='hire@jabber.store',
			    to_emails=e,
			    subject='Resume',
			    html_content='To whoever this may concern')

			file_path = 'file.pdf'
			with open(file_path, 'rb') as f:
			    data = f.read()
			    f.close()
			encoded = base64.b64encode(data).decode()
			attachment = Attachment()
			attachment.file_content = FileContent(encoded)
			attachment.file_type = FileType('application/pdf')
			attachment.file_name = FileName('file.pdf')
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


