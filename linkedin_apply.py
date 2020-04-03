from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

class apply:
	def __init__(self, user, passwd, link):
		# Variables needed for LinkedIn Easy apply
		self.user = user
		self.passwd = passwd
		self.link = link

	def run(self):
		# ChromeDriver options
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors-spki-list')
		options.add_argument('--ignore-ssl-errors')
		options.add_argument("--start-maximized")
		driver = webdriver.Chrome(chrome_options=options)
		driver.get(self.link)

		# Click Login Button
		apply_button = driver.find_element_by_class_name("nav__button-secondary")
		apply_button.click()
		time.sleep(4)

		# Enter credentials
		actions = ActionChains(driver)
		actions.send_keys(self.user + Keys.TAB + self.passwd +  Keys.TAB + Keys.TAB + Keys.ENTER)
		actions.perform()
		time.sleep(4)

		# Click Apply button
		apply_button = driver.find_element_by_class_name("jobs-apply-button")
		apply_button.click()
		time.sleep(4)

		# Click Submit button if applicable
		apply_button = driver.find_element_by_class_name("artdeco-button--primary")
		apply_button.click()

		# Click continue button if applicable
		apply_button = driver.find_element_by_class_name("continue-btn")
		apply_button.click()

		driver.close()


