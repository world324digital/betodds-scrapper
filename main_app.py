from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from betway import BetWay
from eurobet import EuroBet
from betaland import BetaLand
from betfair import BetFair
from betflag import BetFlag
from goldbet import GoldBet
from lottomatica import LottoMatica
from planetwin import PlanetWin
from snai import Snai

class OddsMatcher:

    def __init__(self):
        self.epoch = 1

    def run(self):
        goldbet = GoldBet()
        scheduler = BlockingScheduler()
        scheduler.add_job(goldbet.main, 'interval', hours=1)
        scheduler.start()


if __name__ == "__main__":
    odds_matcher = OddsMatcher()
    odds_matcher.run()