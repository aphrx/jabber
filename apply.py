from selenium import webdriver

driver = webdriver.Chrome()
driver.get("ontariotechu.ca")
assert "Python" in driver.title
