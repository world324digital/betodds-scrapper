from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import mysql.connector
from datetime import datetime
from translate import Translator
# from db_manager import DbManager

class GoldBet:

	options = Options()
	options.add_argument("start-maximized")
	options.add_argument("ignore-certificate-errors")
	options.add_argument("headless")
	options.add_argument("window-size=1200x600")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	def __init__(self, epoch = 1, epoch_time = ""):
		self.epoch = epoch
		self.epoch_time = epoch_time
		self.total_counts = 0
		# self.db_manager = DbManager()
		self.odds_list = []
		self.host = "45.8.227.145"
		self.user = "oddsmatcher"
		self.password = "~exY([5~fjxN"
		self.database = "oddsmatcher-353030358ce0"
		self.port = "57558"

	def fetch_data(self, item):
		# time.sleep(3)
		link_click_item = item.find_element(By.XPATH, "a")
		link_item = item.find_element(By.XPATH, "a/div/span[last()]")
		list_title = link_item.text
		# link_click_item.click()
		if list_title != "OGGI-DOMANI":
			self.driver.execute_script("arguments[0].click();", link_click_item)
			print(list_title)
			# time.sleep(3)
			sub_list = item.find_elements(By.XPATH, "ul/li")
			for sub_item in sub_list:
				sub_link_item = sub_item.find_element(By.XPATH, "a/span/div/div")
				self.driver.execute_script("arguments[0].click();", sub_link_item)
				# sub_link_item.click()
				sub_title = sub_link_item.text
				if sub_title == "":
					sub_title = sub_link_item.get_attribute("innerHTML")
				print("--- " + sub_title)
				loading = 1
				while loading == 1:
					loading_element = self.driver.find_element(By.ID, "spinner-loading")
					if 'fade' in loading_element.get_attribute("class").split():
					    loading = 0
				time.sleep(3)
				match_list = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'sport-table')]/table[contains(@class, 'table-full')]//tr[contains(@class, 'oddsRow')]")
				# time.sleep(3)
				temp_list = []
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
					first_element = match_item.find_elements(By.XPATH, "//span[@data-selname='1']")
					draw_element = match_item.find_elements(By.XPATH, "//span[@data-selname='X']")
					second_element = match_item.find_elements(By.XPATH, "//span[@data-selname='2']")
					under_element = match_item.find_elements(By.XPATH, "//span[@data-selname='U']")
					over_element = match_item.find_elements(By.XPATH, "//span[@data-selname='O']")
					gg_element = match_item.find_elements(By.XPATH, "//span[@data-selname='GG']")
					ng_element = match_item.find_elements(By.XPATH, "//span[@data-selname='NG']")
					if len(first_element) > 0:
						first = first_element[0].get_attribute("innerHTML").replace(" ", "")
					if len(draw_element) > 0:
						draw = draw_element[0].get_attribute("innerHTML").replace(" ", "")
					if len(second_element) > 0:
						second = second_element[0].get_attribute("innerHTML").replace(" ", "")
					if len(under_element) > 0:
						under = under_element[0].get_attribute("innerHTML").replace(" ", "")
					if len(over_element) > 0:
						over = over_element[0].get_attribute("innerHTML").replace(" ", "")
					if len(gg_element) > 0:
						gg = gg_element[0].get_attribute("innerHTML").replace(" ", "")
					if len(ng_element) > 0:
						ng = ng_element[0].get_attribute("innerHTML").replace(" ", "")
					row = (list_title, sub_title, team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "goldbet", self.epoch_time)
					# if self.total_counts == 50:
					# 	self.db_manager.insert_data(self.odds_list)
					# 	self.odds_list = []
					# 	self.total_counts = 0
					if team1 != "" and team2 != "":
						print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng)
						self.odds_list.append(row)
						# self.db_manager.insert_row(row)
						# self.insert_row(row)
						# temp_list.append(row)
						self.total_counts = self.total_counts + 1
				loading_element = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'modal-backdrop')]")
				if len(loading_element) > 0:
					print(loading_element.get_attribute("outerHTML"))
				time.sleep(1)
				# self.insert_data(temp_list)
				self.driver.execute_script("arguments[0].click();", sub_link_item)
				# sub_link_item.click()
				# sub_click_item.click()

	def main(self):
		start_time = time.time()
		now_time = datetime.fromtimestamp(time.time())
		self.epoch_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
		self.driver.get("https://www.goldbet.it/scommesse/sport")
		time.sleep(3)
		if self.epoch == 1:
			cookie_close_btn = self.driver.find_element(By.ID, "onetrust-pc-btn-handler")
			cookie_close_btn.click()
			time.sleep(2)

			button = self.driver.find_element(By.CLASS_NAME, "ot-pc-refuse-all-handler")
			button.click()

		self.epoch = self.epoch + 1
		soccer_menu = self.driver.find_element(By.XPATH, "//ul[@id='menu']/li[2]")
		soccer_menu.click()
		soccer_sidebar = self.driver.find_element(By.XPATH, "//ul[@id='menu']/li[2]/ul")
		sport_list = soccer_sidebar.find_elements(By.XPATH, "li")
		time.sleep(2)
		# print(len(sport_list))
		for i in range(len(sport_list)):
			item = sport_list[i]
			self.fetch_data(item)
		self.insert_data(self.odds_list)
		print("completed time is ", time.time() - start_time)
		# time.sleep(1800)
		# self.main()
		self.odds_list = []
		self.total_counts = 0
		self.driver.quit()
		# self.driver.close()

	def run(self):
		threading.Timer(3600, self.run).start()
		now_time = datetime.fromtimestamp(time.time())
		print("GoldBet =======> ", self.total_counts, "Matches Saved")
		self.total_counts = 0
		self.epoch_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
		print(self.epoch, self.epoch_time)
		self.main()

	def insert_row(self, odds_list):
		mydb = mysql.connector.connect(
		    host = self.host,
		    user = self.user,
		    password = self.password,
		    database = self.database,
		    port = self.port
		)
		sql = "INSERT INTO `python_odds_table_new` (`category`, `subcategory`, `team1`, `team2`, `event_date`, `event_time`, `equal`, `first`, `second`, `draw`, `under`, `over`, `gg`, `ng`, `bookmarker`, `epoch_date_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		mycursor = mydb.cursor()
		mycursor.execute(sql, odds_list)
		mydb.commit()
		mycursor.close()

	def insert_data(self, odds_list):
		if len(odds_list) > 0:
			mydb = mysql.connector.connect(
				host = self.host,
				user = self.user,
				password = self.password,
				database = self.database,
				port = self.port
			)
			sql = "UPDATE `python_odds_table_new` SET `deleted_at` = CURRENT_TIMESTAMP WHERE `bookmarker` = '" + odds_list[0][-2] + "';"
			mycursor = mydb.cursor()
			mycursor.execute(sql)
			mydb.commit()
			mycursor.close()
			sql = "INSERT INTO `python_odds_table_new` (`category`, `subcategory`, `team1`, `team2`, `event_date`, `event_time`, `equal`, `first`, `second`, `draw`, `under`, `over`, `gg`, `ng`, `bookmarker`, `epoch_date_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			mycursor = mydb.cursor()
			mycursor.executemany(sql, odds_list)
			mydb.commit()
			mycursor.close()

if __name__ == "__main__":
	goldbet = GoldBet()
	goldbet.main()