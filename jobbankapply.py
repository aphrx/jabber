from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

class apply:
	def __init__(self, jobs):
		self.jobs = jobs

	def run(self):
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
				        print(val)
				        break
			except:
				pass


