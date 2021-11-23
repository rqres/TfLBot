from bs4 import BeautifulSoup
import re
from collections import defaultdict
import json
import requests
# from portal_bot import PortalBot


class JourneyListGenerator():
	journeys = defaultdict(list)

	def __init__(self, soup):
		# self.page_source = PortalBot().get_page_source()
		# self.soup = BeautifulSoup(self.page_source, 'lxml')
		self.soup = soup


	# def is_journey(self, tag):
	# 	return tag.name == "span" and re.search(" to ", tag.string)


	def get_journey_list(self):
		for tag in self.soup.find_all("span", string=re.compile(" to ")):
			# print(tag.string)
			indx = tag.string.find(" to ")
			start = tag.string[0:indx].strip()
			end = tag.string[indx+3:].strip()
			start = re.sub("\(.+", "", start)
			start = re.sub("\[.+", "", start)
			end = re.sub("\(.+", "", end)
			end = re.sub("\[.+", "", end)
			# print(start)
			# print(end)
			if start and end:
				self.journeys[start].append(end)

		return self.journeys


"""
	Beautiful Soup code
"""




####   page_source = open("tfl-page-source.txt")

# tfl_url = f"https://tfl.gov.uk/plan-a-journey/results?InputFrom={}&InputTo={}&ToId=1000169&Time=1000"


# f = open("tfl-page-source.txt", "w")
# f.write(soup.prettify())
# f.close()


	
# for start in journeys:
# 	for destination in journeys[start]:
# 		print(start + end)
# 		source = requests.get(f"https://tfl.gov.uk/plan-a-journey/results?InputFrom={start}&InputTo={destination}&ToId=1000169&Time=1000").text
# 		fare_soup = BeautifulSoup(source, 'lxml')
# 		f = open("fare_soup.html", "w")
# 		f.write(str(fare_soup))
# 		f.close()
# 		break
# 	break

# print(json.dumps(journeys, indent=4))








