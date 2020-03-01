from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

class apply:
	def __init__(self, user, passwd, link):
		self.user = user
		self.passwd = passwd
		self.link = link

	def run(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors-spki-list')
		options.add_argument('--ignore-ssl-errors')
		options.add_argument("--start-maximized")
		driver = webdriver.Chrome(chrome_options=options)
		driver.get(self.link)

		apply_button = driver.find_element_by_class_name("nav__button-secondary")
		apply_button.click()

		time.sleep(4)

		actions = ActionChains(driver)
		actions.send_keys(self.user + Keys.TAB + self.passwd +  Keys.TAB + Keys.TAB + Keys.ENTER)# +  Keys.TAB + Keys.ENTER)# + "Resume.pdf" + Keys.ENTER)
		actions.perform()

		time.sleep(4)

		apply_button = driver.find_element_by_class_name("jobs-apply-button")
		apply_button.click()

		time.sleep(4)

		apply_button = driver.find_element_by_class_name("artdeco-button--primary")
		apply_button.click()

		apply_button = driver.find_element_by_class_name("continue-btn")
		apply_button.click()

		driver.close()


