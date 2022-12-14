from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import mysql.connector
from datetime import datetime
# from db_manager import DbManager

class BetFlag:

	options = Options()
	sub_list = []
	match_list = []
	options.add_argument("start-maximized")
	# options.add_argument("headless")
	# options.add_argument("window-size=1200x600")
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
		item.click()
		# self.driver.execute_script("arguments[0].click();", item)
		list_title = item.find_element(By.XPATH, "a").text
		print(list_title)
		time.sleep(3)
		sub_list = item.find_elements(By.XPATH, "ul/li")
		for sub_item in sub_list:
			sub_title = sub_item.find_element(By.XPATH, "a").text
			if sub_title != "":
				sub_item.click()
				# self.driver.execute_script("arguments[0].click();", sub_item)
				print("--- " + sub_title)
				time.sleep(3)
				match_list = self.driver.find_elements(By.XPATH, "//div[@class='containerEvents']/div")
				# print(len(match_list))
				temp_list = []
				for match_item in match_list:
					time_info = match_item.get_attribute("c_dat")
					event_date = time_info.split("T")[0]
					event_time = time_info.split("T")[1]
					equal = match_item.get_attribute("c_dav")
					if len(equal.split(" - ")) > 1:
						team1 = equal.split(" - ")[0]
						team2 = equal.split(" - ")[1]
					else:
						team1 = ""
						team2 = ""
					first = ""
					draw = ""
					second = ""
					under = ""
					over = ""
					gg = ""
					ng = ""
					event_odds = match_item.find_elements(By.XPATH, "*[@class='bets']/div[contains(@class, 'odds p1')]//div[contains(@class, 'oddPrematch')]")
					odd_index = 0
					for odd_item in event_odds:
						odd_info = odd_item.find_elements(By.XPATH, "div/a")
						locked = 0
						if 'lock' in odd_item.get_attribute("class").split():
							locked = 1
						else:
							if odd_index == 0:
								first = odd_item.get_attribute("c_quo")
							elif odd_index == 1:
								draw = odd_item.get_attribute("c_quo")
							elif odd_index == 2:
								second = odd_item.get_attribute("c_quo")
						odd_index = odd_index + 1
					event_odds = match_item.find_elements(By.XPATH, "*[@class='bets']/div[contains(@class, 'odds p2')]//div[contains(@class, 'oddPrematch')]")
					odd_index = 0
					for odd_item in event_odds:
						odd_info = odd_item.find_elements(By.XPATH, "div/a")
						locked = 0
						if 'lock' in odd_item.get_attribute("class").split():
							locked = 1
						else:
							if odd_index == 0:
								gg = odd_item.get_attribute("c_quo")
							elif odd_index == 1:
								ng = odd_item.get_attribute("c_quo")
						odd_index = odd_index + 1
					event_odds = match_item.find_elements(By.XPATH, "*[@class='bets']/div[contains(@class, 'odds p3')]//div[contains(@class, 'oddPrematch')]")
					odd_index = 0
					for odd_item in event_odds:
						odd_info = odd_item.find_elements(By.XPATH, "div/a")
						locked = 0
						if 'lock' in odd_item.get_attribute("class").split():
							locked = 1
						else:
							if odd_index == 0:
								under = odd_item.get_attribute("c_quo")
							elif odd_index == 1:
								over = odd_item.get_attribute("c_quo")
						odd_index = odd_index + 1
					row = (list_title, sub_title, team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "betflag", self.epoch_time)
					# if self.total_counts == 50:
					# 	self.db_manager.insert_data(self.odds_list)
					# 	self.odds_list = []
					# 	self.total_counts = 0
					if team1 != "" and team2 != "":
						print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng + " " + self.epoch_time)
						self.odds_list.append(row)
						# self.db_manager.insert_row(row)
						# self.insert_row(row)
						# temp_list.append(row)
						self.total_counts = self.total_counts + 1
				# self.insert_data(temp_list)
				sub_item.click()
				# self.driver.execute_script("arguments[0].click();", sub_item)

	def main(self):
		start_time = time.time()
		now_time = datetime.fromtimestamp(time.time())
		self.epoch_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
		self.driver.get("https://www.betflag.it/sport")
		if self.epoch == 1:
			cookie_close_btn = self.driver.find_element(By.ID, "LinkButton2")
			cookie_close_btn.click()
		time.sleep(10)
		modal_close_btn = self.driver.find_element(By.XPATH, "//div[@class='btn-close']")
		if modal_close_btn:
			modal_close_btn.click()
		self.epoch = self.epoch + 1
		soccer_sidebar = self.driver.find_element(By.ID, "mhs-1")

		# Get last menu item for expand and click
		soccer_menu = soccer_sidebar.find_element(By.XPATH, "a")
		soccer_menu.click()
		sport_list = soccer_sidebar.find_elements(By.XPATH, "ul/li")
		time.sleep(2)
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
		print("BetFlag =======> ", self.total_counts, "Matches Saved")
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
	betflag = BetFlag()
	betflag.main()