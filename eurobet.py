from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import mysql.connector
from datetime import datetime
from db_manager import DbManager

class EuroBet:
	options = Options()
	options.add_argument("start-maximized")
	# options.add_argument("--headless")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	def __init__(self, epoch = 1, epoch_time = ""):
		self.epoch = epoch
		self.epoch_time = epoch_time
		self.total_counts = 0
		# self.db_manager = DbManager()
		# self.odds_list = []
		self.host = "45.8.227.145"
		self.user = "oddsmatcher"
		self.password = "~exY([5~fjxN"
		self.database = "oddsmatcher-353030358ce0"
		self.port = "57558"

	def fetch_data(self, item):
		item.click()
		# self.driver.execute_script("arguments[0].click();", item)
		list_title = item.find_element(By.XPATH, "a/h4").text
		# print(list_title)
		time.sleep(3)
		sub_list = item.find_elements(By.XPATH, "ul[@class='sidebar-league']/li")
		for sub_item in sub_list:
			sub_item.click()
			# self.driver.execute_script("arguments[0].click();", sub_item)
			sub_title = sub_item.find_element(By.XPATH, "a/h4").text
			# print("--- " + sub_title)
			time.sleep(3)
			match_list = self.driver.find_elements(By.XPATH, "//div[@class='discipline-football']/div[@class='anti-row']//div[@class='event-row']")
			# print(len(match_list))
			for match_item in match_list:
				time_info = match_item.find_elements(By.XPATH, "*[@class='event-wrapper-info']//div[contains(@class,'time-box')]//p")
				event_date = ""
				event_time = ""
				team1 = ""
				team2 = ""
				equal = ""
				first = ""
				draw = ""
				second = ""
				under = ""
				over = ""
				gg = ""
				ng = ""
				if len(time_info) == 1:
					time_string = time_info[0].text
					if ":" in time_string:
						event_time = time_string
					else:
						event_date = time_string
				if len(time_info) == 2:
					event_date = time_info[0].text
					event_time = time_info[1].text
				event_players = match_item.find_elements(By.XPATH, "*[@class='event-wrapper-info']//*[@class='event-players']/span/div/a/span")
				index = 0
				for player_item in event_players:
					if index == 0:
						team1 = player_item.text
					if index == 2:
						team2 = player_item.text
					index = index + 1
				equal = team1 + " - " + team2
				event_odds = match_item.find_elements(By.XPATH, "*[@class='event-wrapper-odds']//*[@class='quota-new']")
				odd_index = 0
				for odd_item in event_odds:
					odd_info = odd_item.find_elements(By.XPATH, "div/a")
					if len(odd_info) > 0:
						if odd_index == 0:
							first = odd_info[0].text
						elif odd_index == 1:
							draw = odd_info[0].text
						elif odd_index == 2:
							second = odd_info[0].text
						elif odd_index == 3:
							under = odd_info[0].text
						elif odd_index == 4:
							over = odd_info[0].text
						elif odd_index == 5:
							gg = odd_info[0].text
						elif odd_index == 6:
							ng = odd_info[0].text
					odd_index = odd_index + 1
				row = (list_title, sub_title, team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "eurobet", self.epoch_time)
				# self.db_manager.insert_data(row)
				# if self.total_counts == 50:
				# 	self.db_manager.insert_data(self.odds_list)
				# 	self.odds_list = []
				# 	self.total_counts = 0
				if team1 != "" and team2 != "":
					print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng + " " + self.epoch_time)
					# self.odds_list.append(row)
					# self.db_manager.insert_row(row)
					self.insert_row(row)
					self.total_counts = self.total_counts + 1
				# print(self.total_counts, "matches fetched", end="\r")

	def main(self):
		self.driver.get("https://www.eurobet.it/scommesse/")
		if self.epoch == 1:
			time.sleep(3)
			close_btn = self.driver.find_elements(By.CLASS_NAME, "onetrust-close-btn-handler")[0]
			close_btn.click()
		time.sleep(1)
		self.epoch = self.epoch + 1
		soccer_sidebar = self.driver.find_elements(By.CLASS_NAME, "sidebar-competition")[1]

		# Get last menu item for expand and click
		last_menu = soccer_sidebar.find_element(By.XPATH, "div/li[last()]")
		last_menu.click()
		sport_list = soccer_sidebar.find_elements(By.XPATH, "div/li")
		expanded_list = soccer_sidebar.find_elements(By.XPATH, "div/div/li")
		sport_list[1].click()
		# time.sleep(5)
		for i in range(len(sport_list) - 2):
			item = sport_list[i + 1]
			self.fetch_data(item)
		for j in range(len(expanded_list) - 1):
			item = expanded_list[j]
			self.fetch_data(item)
		# print(self.odds_list)
		# self.db_manager.insert_data(self.odds_list)
		# self.odds_list = []
		# self.total_counts = 0
		# self.db_manager.get_data()
		# self.driver.quit()
		# self.driver.close()

	def run(self):
		threading.Timer(3600, self.run).start()
		now_time = datetime.fromtimestamp(time.time())
		print("EuroBet =======> ", self.total_counts, "Matches Saved")
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
		sql = "INSERT INTO `python_odds_table` (`category`, `subcategory`, `team1`, `team2`, `event_date`, `event_time`, `equal`, `first`, `second`, `draw`, `under`, `over`, `gg`, `ng`, `bookmarker`, `epoch_date_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		mycursor = mydb.cursor()
		mycursor.execute(sql, odds_list)
		mydb.commit()
		mycursor.close()

if __name__ == "__main__":
	eurobet = EuroBet()
	eurobet.run()