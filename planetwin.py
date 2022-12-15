from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
from datetime import datetime
from translate import Translator
from db_manager import DbManager

class PlanetWin:

	options = Options()
	options.add_argument("start-maximized")
	options.add_argument("ignore-certificate-errors")
	driver1 = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	def __init__(self, epoch = 1, epoch_time = ""):
		self.epoch = epoch
		self.epoch_time = epoch_time
		self.total_counts = 0
		self.db_manager = DbManager()
		self.odds_list = []

	def fetch_data(self, item):
		time.sleep(1)
		link_item = item.find_element(By.XPATH, "a")
		list_title = link_item.text
		if self.total_counts > 0:
			self.driver.execute_script("arguments[0].click();", link_item)
		print(list_title)
		time.sleep(1)
		sub_list = item.find_elements(By.XPATH, "ul/li")
		for sub_item in sub_list:
			sub_link_item = sub_item.find_element(By.XPATH, "a")
			sub_title = sub_link_item.get_attribute("data-title")
			href = sub_link_item.get_attribute("href")
			if self.total_counts > 0:
				self.driver.execute_script("arguments[0].click();", sub_link_item)
			# sub_link_item.click()
			print("--- " + sub_title)
			time.sleep(3)
			match_list = self.driver.find_elements(By.XPATH, "//tr[@class='dgAItem']")
			time.sleep(3)
			# print(len(match_list))
			for match_item in match_list:
				time_info = match_item.get_attribute("data-datainizio").split("+")[0].split("T")
				event_date = ""
				event_time = ""
				if len(time_info) > 1:
					event_date = time_info[0]
					event_time = time_info[1]
				equal = match_item.get_attribute("data-sottoevento-name")
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
				first_item = match_item.find_elements(By.XPATH, "//td[@data-tipoquota='1']")
				draw_item = match_item.find_elements(By.XPATH, "//td[@data-tipoquota='X']")
				second_item = match_item.find_elements(By.XPATH, "//td[@data-tipoquota='2']")
				over_item = match_item.find_elements(By.XPATH, "//td[@data-tipoquota='Ov. 2.5']")
				under_item = match_item.find_elements(By.XPATH, "//td[@data-tipoquota='Un. 2.5']")
				gg_item = match_item.find_elements(By.XPATH, "//td[@data-tipoquota='GG']")
				ng_item = match_item.find_elements(By.XPATH, "//td[@data-tipoquota='NG']")
				if len(first_item) > 0:
					first = first_item[0].get_attribute("data-quota")
				if len(draw_item) > 0:
					draw = draw_item[0].get_attribute("data-quota")
				if len(second_item) > 0:
					second = second_item[0].get_attribute("data-quota")
				if len(over_item) > 0:
					over = over_item[0].get_attribute("data-quota")
				if len(under_item) > 0:
					under = under_item[0].get_attribute("data-quota")
				if len(gg_item) > 0:
					gg = gg_item[0].get_attribute("data-quota")
				if len(ng_item) > 0:
					ng = ng_item[0].get_attribute("data-quota")
				row = (list_title, sub_title, team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "planetwin365", self.epoch_time)
				if self.total_counts == 200:
					self.db_manager.insert_data(self.odds_list)
					self.odds_list = []
					self.total_counts = 0
				if team1 != "" and team2 != "":
					# print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng)
					self.odds_list.append(row)
					self.total_counts = self.total_counts + 1
			time.sleep(1)
			self.driver.execute_script("arguments[0].click();", sub_link_item)
			# sub_link_item.click()

	def main(self):
		self.driver1.get("https://planetwin365.it/it/scommesse/calcio")
		time.sleep(3)
		if self.epoch == 1:
			cookie_close_btn = self.driver1.find_element(By.CSS_SELECTOR, "a.eupopup-closebutton")
			cookie_close_btn.click()
			time.sleep(2)

			soccer_menu = self.driver1.find_element(By.XPATH, "//ul[@id='menuSports']//div[@data-title='Calcio']")
			soccer_menu = soccer_menu.find_element(By.XPATH, "../..")
			self.driver1.execute_script("arguments[0].click();", soccer_menu)
			soccer_sidebar = soccer_menu.find_element(By.XPATH, "..")
			sport_list = soccer_sidebar.find_elements(By.XPATH, "ul/li")
		if len(sport_list) > 0:
			first_link = sport_list[0].find_element(By.XPATH, "ul/li[1]/a")
			href = first_link.get_attribute("href")
			self.driver1.close()
			self.driver.get(href)
			time.sleep(2)
			soccer_menu = self.driver.find_element(By.XPATH, "//ul[@id='menuSports']//div[@data-title='Calcio']")
			soccer_menu = soccer_menu.find_element(By.XPATH, "../..")
			# self.driver.execute_script("arguments[0].click();", soccer_menu)
			soccer_sidebar = soccer_menu.find_element(By.XPATH, "..")
			sport_list = soccer_sidebar.find_elements(By.XPATH, "ul/li")
			# print(len(sport_list))
			# time.sleep(200)
			for i in range(len(sport_list)):
				item = sport_list[i]
				self.fetch_data(item)
			self.db_manager.insert_data(self.odds_list)
		# self.driver.quit()

    def run(self):
        threading.Timer(1800, self.run).start()
        now_time = datetime.fromtimestamp(time.time())
        self.epoch_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
        print(self.epoch, self.epoch_time)
        self.main()
        self.epoch = self.epoch + 1

if __name__ == "__main__":
	planetwin = PlanetWin()
	planetwin.run()