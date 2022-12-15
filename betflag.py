from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
from db_manager import DbManager

class BetFlag:

	options = Options()
	sub_list = []
	match_list = []
	options.add_argument("start-maximized")
	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

	def __init__(self, epoch = 1, epoch_time = ""):
		self.epoch = epoch
		self.epoch_time = epoch_time
		self.total_counts = 0
		self.db_manager = DbManager()
		self.odds_list = []

	def fetch_data(self, item):
		item.click()
		# self.driver.execute_script("arguments[0].click();", item)
		list_title = item.find_element(By.XPATH, "a").text
		# print(list_title)
		time.sleep(3)
		sub_list = item.find_elements(By.XPATH, "ul/li")
		for sub_item in sub_list:
			sub_item.click()
			# self.driver.execute_script("arguments[0].click();", sub_item)
			sub_title = sub_item.find_element(By.XPATH, "a").text
			# print("--- " + sub_title)
			time.sleep(3)
			match_list = self.driver.find_elements(By.XPATH, "//div[@class='containerEvents']/div")
			# print(len(match_list))
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
				if self.total_counts == 200:
					self.db_manager.insert_data(self.odds_list)
					self.odds_list = []
					self.total_counts = 0
				if team1 != "" and team2 != "":
					# print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng + " " + self.epoch_time)
					self.odds_list.append(row)
					self.total_counts = self.total_counts + 1
			sub_item.click()
			# self.driver.execute_script("arguments[0].click();", sub_item)

	def main(self):
		self.driver.get("https://www.betflag.it/sport")
		if self.epoch == 1:
			cookie_close_btn = self.driver.find_element(By.ID, "LinkButton2")
			cookie_close_btn.click()
			time.sleep(10)
			modal_close_btn = self.driver.find_element(By.XPATH, "//div[@class='btn-close']")
			modal_close_btn.click()
		soccer_sidebar = self.driver.find_element(By.ID, "mhs-1")

		# Get last menu item for expand and click
		soccer_menu = soccer_sidebar.find_element(By.XPATH, "a")
		soccer_menu.click()
		sport_list = soccer_sidebar.find_elements(By.XPATH, "ul/li")
		time.sleep(2)
		for i in range(len(sport_list)):
			item = sport_list[i]
			self.fetch_data(item)
		self.db_manager.insert_data(self.odds_list)
		# self.driver.quit()
		# self.driver.close()

    def run(self):
        threading.Timer(1800, self.run).start()
        now_time = datetime.fromtimestamp(time.time())
        self.epoch_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
        print(self.epoch, self.epoch_time)
        self.main()
        self.epoch = self.epoch + 1

if __name__ == "__main__":
	betflag = BetFlag()
	betflag.run()