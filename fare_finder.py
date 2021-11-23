from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
# from journey_list_generator import JourneyListGenerator


class FareFinderBot():
	fare_finder_url = "https://tfl.gov.uk/fares/find-fares/tube-and-rail-fares/single-fare-finder"
	grand_total = 0
	options = webdriver.ChromeOptions()
	jrn_list = []
	fares_list = []

	def __init__(self, journeys):
		self.journeys = journeys

		self.options.add_argument('--ignore-certificate-errors')
		self.options.add_argument('--incognito')
		self.options.add_argument('--headless')
		self.driver = webdriver.Chrome("/Users/rares/Downloads/chromedriver", options = self.options)

		self.driver.get(self.fare_finder_url)
		assert "Single fare finder" in self.driver.title
		time.sleep(3)
		self.driver.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
		time.sleep(1)
		self.driver.find_element(By.XPATH, './/button[.="Done"]').click()
		time.sleep(2)

	def begin_fare_search(self):
		for start, destlist in self.journeys.items():
			for dest in destlist:
				print(f"{start} - {dest}")
				self.jrn_list.append(f"{start} - {dest}")
				from_field = self.driver.find_element(By.XPATH, '//*[@id="From"]')
				from_field.send_keys(start)
				time.sleep(2)
				self.driver.find_element(By.ID, 'stop-points-search-from-suggestion-0').click()
				dest_field = self.driver.find_element(By.XPATH, '//*[@id="To"]')
				dest_field.send_keys(dest)
				time.sleep(2)
				self.driver.find_element(By.ID, 'stop-points-search-to-suggestion-0').click()
				self.driver.find_element(By.ID, 'submit').click()
				time.sleep(3)
				try:
					fare = self.driver.find_element(By.XPATH, '//*[@id="results"]/div[1]/div[2]/div/div[1]/div[2]/p[2]/strong').text
				except Exception as e:
					fare = self.driver.find_element(By.XPATH, '//*[@id="results"]/div[1]/div[2]/div/div[1]/div[2]/p/strong').text
				
				fare = fare[-4:]  
				# final_dictionary[f"{start}-{dest}"].append(fare)
				self.fares_list.append(fare)
				self.grand_total += float(fare)
				print(f"{fare}, grand total so far: {self.grand_total}")

				from_field.send_keys(Keys.COMMAND + 'a')
				from_field.send_keys(Keys.DELETE)
				dest_field.send_keys(Keys.COMMAND + 'a')
				dest_field.send_keys(Keys.DELETE)


	def get_grand_total(self):
		return self.grand_total
				
