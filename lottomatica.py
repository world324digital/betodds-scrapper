from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from translate import Translator
from db_manager import DbManager

class LottoMatica:

	options = Options()
	options.add_argument("start-maximized")
	options.add_argument("ignore-certificate-errors")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	def __init__(self):
		self.total_counts = 0
		self.db_manager = DbManager()
		self.odds_list = []

	def convert_date(self, txt):
		splited_txt = txt.split(" ")
		day = splited_txt[0]
		translator = Translator(from_lang="italian", to_lang="english")
		return day + " " + translator.translate(splited_txt[1]) + " " + splited_txt[2]

	def fetch_data(self, item):
		item.click()
		link_item = item.find_element(By.XPATH, "a/div/span[last()]")
		list_title = link_item.text
		print(list_title)
		time.sleep(3)
		sub_list = item.find_elements(By.XPATH, "ul/li")
		for sub_item in sub_list:
			sub_item.click()
			sub_link_item = sub_item.find_element(By.XPATH, "a/span/div/div")
			sub_title = sub_link_item.text
			print("--- " + sub_title)
			time.sleep(3)
			match_list = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'sport-table')]/table[contains(@class, 'table-full')]//tr[contains(@class, 'oddsRow')]")
			# print(len(match_list))
			for match_item in match_list:
				time_info = match_item.get_attribute("data-evndate").split(" ")
				event_date = ""
				event_time = ""
				if len(time_info) > 1:
					event_date = time_info[0]
					event_time = time_info[1]
				equal = match_item.get_attribute("data-evtname")
				team_info = equal.split(" - ")
				team1 = ""
				team2 = ""
				if len(team_info) > 1:
					team1 = team_info[0]
					team2 = team_info[1]
				first = ""
				draw = ""
				second = ""
				under = ""
				over = ""
				gg = ""
				ng = ""
				odd_info = match_item.find_elements(By.XPATH, "//span[@data-markname='1X2']")
				first = odd_info[0].text
				draw = odd_info[1].text
				second = odd_info[2].text
				uo_info = match_item.find_elements(By.XPATH, "//span[@data-markname='U/O(2.5)']")
				under = uo_info[0].text
				over = uo_info[1].text
				gol_info = match_item.find_elements(By.XPATH, "//span[@data-markname='GG/NG']")
				gg = gol_info[0].text
				ng = gol_info[1].text
				row = (list_title, sub_title, team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "lottomatica")
				if self.total_counts == 200:
					self.db_manager.insert_data(self.odds_list)
					self.odds_list = []
					self.total_counts = 0
				if team1 != "" and team2 != "":
					print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng)
					self.odds_list.append(row)
					self.total_counts = self.total_counts + 1
			sub_item.click()

	def main(self):
		self.driver.get("https://www.lottomatica.it/scommesse/sport/")
		time.sleep(3)
		cookie_close_btn = self.driver.find_element(By.ID, "onetrust-pc-btn-handler")
		cookie_close_btn.click()
		time.sleep(2)

		button = self.driver.find_element(By.CLASS_NAME, "ot-pc-refuse-all-handler")
		button.click()

		soccer_menu = self.driver.find_element(By.XPATH, "//ul[@id='menu']/li[2]")
		soccer_menu.click()
		soccer_sidebar = self.driver.find_element(By.XPATH, "//ul[@id='menu']/li[2]/ul")
		sport_list = soccer_sidebar.find_elements(By.XPATH, "li")
		time.sleep(2)
		# print(len(sport_list))
		# time.sleep(200)
		for i in range(len(sport_list)):
			item = sport_list[i]
			self.fetch_data(item)
		self.db_manager.insert_data(self.odds_list)
		# self.driver.quit()
		# self.driver.close()

if __name__ == "__main__":
	lottomatica = LottoMatica()
	lottomatica.main()