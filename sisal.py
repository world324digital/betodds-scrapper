from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from translate import Translator
from db_manager import DbManager

class Sisal:

	options = Options()
	options.add_argument("start-maximized")
	options.add_argument("ignore-certificate-errors")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	def __init__(self, epoch = 1, epoch_time = ""):
		self.epoch = epoch
		self.epoch_time = epoch_time
		self.total_counts = 0
		self.db_manager = DbManager()
		self.odds_list = []

	def fetch_data(self, item):
		link_click_item = item.find_element(By.XPATH, "a")
		# link_click_item.click()
		self.driver.execute_script("arguments[0].click();", link_click_item)
		link_item = item.find_element(By.XPATH, "a/p").text.split(" ", 1)
		list_title = link_item[0]
		print(list_title)
		time.sleep(5)
		sub_title = link_item[1]
		print("--- " + sub_title)
		match_list = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'grid_mg-row-wrapper')]")
		time.sleep(3)
		# print(len(match_list))
		for match_item in match_list:
			match_link = match_item.find_element(By.XPATH, "//a[contains(@class, 'regulator_description')]")
			self.driver.execute_script("arguments[0].click();", match_link)
			# print(match_link)
			# event_date = ""
			# event_time = ""
			# if len(time_info) > 1:
			# 	event_date = time_info[0]
			# 	event_time = time_info[1]
			# equal = match_item.get_attribute("data-evtname")
			# team_info = equal.split(" - ")
			# team1 = ""
			# team2 = ""
			# if len(team_info) > 1:
			# 	team1 = team_info[0]
			# 	team2 = team_info[1]
			# first = ""
			# draw = ""
			# second = ""
			# under = ""
			# over = ""
			# gg = ""
			# ng = ""
			# odd_info = match_item.find_elements(By.XPATH, "//span[@data-markname='1X2']")
			# first = odd_info[0].text
			# draw = odd_info[1].text
			# second = odd_info[2].text
			# uo_info = match_item.find_elements(By.XPATH, "//span[@data-markname='U/O(2.5)']")
			# under = uo_info[0].text
			# over = uo_info[1].text
			# gol_info = match_item.find_elements(By.XPATH, "//span[@data-markname='GG/NG']")
			# gg = gol_info[0].text
			# ng = gol_info[1].text
			# row = (list_title, sub_title, team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "goldbet", self.epoch_time)
			# if self.total_counts == 200:
			# 	self.db_manager.insert_data(self.odds_list)
			# 	self.odds_list = []
			# 	self.total_counts = 0
			# if team1 != "" and team2 != "":
			# 	print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng)
			# 	self.odds_list.append(row)
			# 	self.total_counts = self.total_counts + 1
		self.driver.execute_script("arguments[0].click();", link_click_item)

	def main(self):
		self.driver.get("https://www.sisal.it/scommesse-matchpoint/sport/calcio")
		time.sleep(3)
		if self.epoch == 1:
			cookie_close_btn = self.driver.find_element(By.XPATH, "//div[@id='onetrust-close-btn-container']/button")
			cookie_close_btn.click()
			time.sleep(2)

		# 	button = self.driver.find_element(By.CLASS_NAME, "ot-pc-refuse-all-handler")
		# 	button.click()
		sport_list = self.driver.find_elements(By.XPATH, "//div/ul/li/ul/li[contains(@class, 'competitionsMenu_listGroupItem__1Soj_')]")
		time.sleep(2)
		# print(len(sport_list))
		for i in range(len(sport_list)):
			item = sport_list[i]
			self.fetch_data(item)
		self.db_manager.insert_data(self.odds_list)
		# self.driver.quit()
		# self.driver.close()

if __name__ == "__main__":
	sisal = Sisal()
	sisal.main()