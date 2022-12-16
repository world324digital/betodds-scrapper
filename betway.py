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

class BetWay:

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

	def convert_date(self, txt):
		result = txt.replace("Gennaio", "January")
		result = result.replace("Febbraio", "February")
		result = result.replace("Marzo", "March")
		result = result.replace("Aprile", "April")
		result = result.replace("Maggio", "May")
		result = result.replace("Giugno", "June")
		result = result.replace("Luglio", "July")
		result = result.replace("Agosto", "August")
		result = result.replace("Settembre", "September")
		result = result.replace("Ottobre", "October")
		result = result.replace("Novembre", "November")
		result = result.replace("Dicembre", "December")
		return result
		splited_txt = txt.split(" ")
		day = splited_txt[0]
		translator = Translator(from_lang="italian", to_lang="english")
		return day + " " + translator.translate(splited_txt[1]) + " " + splited_txt[2]

	def fetch_data(self, item):
		item.click()
		# self.driver.execute_script("arguments[0].click();", item)
		list_title = item.text
		# print(list_title)
		time.sleep(3)
		sub_list = item.find_elements(By.XPATH, "div[contains(@class, 'competizione-sub')]/a")
		for sub_item in sub_list:
			sub_item.click()
			# self.driver.execute_script("arguments[0].click();", sub_item)
			sub_title = sub_item.text
			# print("--- " + sub_title)
			time.sleep(3)
			match_list = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'contenitore-table-grande')]//div[contains(@class, 'contenitore-table')]/div[contains(@class, 'contenitoreRiga')]")
			# print(len(match_list))
			for match_item in match_list:
				time_info = match_item.find_element(By.XPATH, "div[contains(@class, 'tabellaQuoteNew')]/div[contains(@class, 'tabellaQuoteTempo')]")
				date_string = self.convert_date(time_info.find_element(By.XPATH, "//span[contains(@class, 'tabellaQuoteTempo__data')]").get_attribute("innerHTML").split(" ", 1)[1])
				converted_date = datetime.strptime(date_string, "%d %B %Y")
				event_date = converted_date.strftime("%m-%d-%Y")
				event_time = time_info.find_element(By.XPATH, "//span[contains(@class, 'tabellaQuoteTempo__ora')]").text
				team_info = match_item.find_elements(By.XPATH, "div[contains(@class, 'tabellaQuoteNew')]/div[contains(@class, 'tabellaQuoteSquadre')]/p")
				team1 = ""
				team2 = ""
				if len(team_info) > 2:
					team1 = team_info[0].text
					team2 = team_info[2].text
				equal = team1 + " - " + team2
				first = ""
				draw = ""
				second = ""
				under = ""
				over = ""
				gg = ""
				ng = ""
				event_odds = match_item.find_elements(By.XPATH, "div[contains(@class, 'tabellaQuoteNew')]/div[contains(@class, 'tabellaQuoteContenitoreQuotazioni')]//div[contains(@class, 'contenitoreSingolaQuota')]")
				odd_index = 0
				for odd_item in event_odds:
					odd_info = odd_item.find_element(By.XPATH, "p[contains(@class, 'tipoQuotazione_1')]")
					if odd_index == 0:
						first = odd_info.text
					elif odd_index == 1:
						draw = odd_info.text
					elif odd_index == 2:
						second = odd_info.text
					elif odd_index == 3:
						under = odd_info.text
					elif odd_index == 4:
						over = odd_info.text
					elif odd_index == 5:
						gg = odd_info.text
					elif odd_index == 6:
						ng = odd_info.text
					odd_index = odd_index + 1
				row = (list_title, sub_title, team1, team2, event_date, event_time, equal, first, second, draw, under, over, gg, ng, "betway", self.epoch_time)
				# if self.total_counts == 50:
				# 	self.db_manager.insert_data(self.odds_list)
				# 	self.odds_list = []
				# 	self.total_counts = 0
				if team1 != "" and team2 != "":
					print(event_date + " " + event_time + " " + equal + " " + first + " " + draw + " " + second + " " + under + " " + over + " " + gg + " " + ng + " " + self.epoch_time)
					# self.odds_list.append(row)
					self.db_manager.insert_row(row)
					self.total_counts = self.total_counts + 1
			sub_item.click()
			# self.driver.execute_script("arguments[0].click();", sub_item)

	def main(self):
		self.driver.get("https://www.betway.it/scommesse")
		# print(self.epoch)
		time.sleep(5)
		if self.epoch == 1:
			cookie_close_btn = self.driver.find_element(By.ID, "CybotCookiebotDialogBodyButtonDecline")
			cookie_close_btn.click()
			time.sleep(2)
		footer = self.driver.find_element(By.ID, "blocco-tasti-bottom")
		footer = self.driver.execute_script("arguments[0].style.width = '0px'; return arguments[0];", footer)
		cg_footer = self.driver.find_element(By.ID, "cg-footer")
		cg_footer = self.driver.execute_script("arguments[0].style.width = '0px'; return arguments[0];", cg_footer)

		self.epoch = self.epoch + 1
		soccer_menu = self.driver.find_element(By.ID, "sport-1")
		soccer_menu.click()
		soccer_sidebar = self.driver.find_element(By.ID, "menu-sport-1")
		sport_list = soccer_sidebar.find_elements(By.XPATH, "div[contains(@class, 'regione-widget')]")
		time.sleep(2)
		# print(len(sport_list))
		# time.sleep(200)
		for i in range(len(sport_list)):
			item = sport_list[i]
			self.fetch_data(item)
		# self.db_manager.insert_data(self.odds_list)
		# self.odds_list = []
		# self.total_counts = 0
		# self.driver.quit()
		# self.driver.close()
	def run(self):
		threading.Timer(2400, self.run).start()
		now_time = datetime.fromtimestamp(time.time())
		print("BetWay =======> ", self.total_counts, "Matches Saved")
		self.total_counts = 0
		self.epoch_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
		print(self.epoch, self.epoch_time)
		self.main()

if __name__ == "__main__":
	betway = BetWay()
	betway.run()