from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import time
# from app import globaluser, globalpasswd


class PortalBot():
	# user = "rares.ioan@icloud.com"
	# password = "mavros-putgob-2kiQby"
	journey_period_start = "19/10/2021"
	journey_period_end = "12/11/2021"
	options = webdriver.ChromeOptions()
	
	

	def __init__(self, user, password):
		self.user = user
		self.password = password

		self.options.add_argument('--ignore-certificate-errors')
		self.options.add_argument('--incognito')
		self.options.add_argument('--headless')
		self.driver = webdriver.Chrome("/Users/rares/Downloads/chromedriver", options = self.options)
		
		self.driver.get("https://photocardportal.tfl.gov.uk")
		assert "Transport for London" in self.driver.title
		time.sleep(2)

	def login(self):
		email_field = self.driver.find_element(By.XPATH, '//*[@id="login-email"]')
		email_field.send_keys(self.user)
		password_field = self.driver.find_element(By.XPATH, '//*[@id="login-password"]')
		password_field.send_keys(self.password)

	def navigate_to_journeys(self):
		self.driver.find_element(By.XPATH, '//*[@id="btn-submit"]').click()
		time.sleep(3)
		self.driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div/div/div/div/ul/li[3]/a').click()
		time.sleep(2)
		Select(self.driver.find_element(By.XPATH, '//*[@id="date-range"]')).select_by_value("custom")
		self.driver.find_element(By.XPATH, '//*[@id="start-date"]').send_keys(self.journey_period_start)
		self.driver.find_element(By.XPATH, '//*[@id="end-date"]').send_keys(self.journey_period_end)
		self.driver.find_element(By.XPATH, '//*[@id="btn-submit-dates"]').click()
		time.sleep(10)

	def get_page_source(self):
		# self.login()
		self.navigate_to_journeys()
		return self.driver.page_source


# Global variables


"""
	Selenium code to get to the list of journeys

"""

# Setting up the chrome webdriver


# Loading the TfL page and logging in



# Navigating the TfL page to the list of journeys




# ---------------- end of selenium bit ----------------------


