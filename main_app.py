import threading
import time
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
        threading.Timer(1800, self.run).start()
        now_time = datetime.fromtimestamp(time.time())
        print(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        betway = BetWay(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        eurobet = EuroBet(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        betaland = BetaLand(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        betfair = BetFair(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        betflag = BetFlag(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        goldbet = GoldBet(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        lottomatica = LottoMatica(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        planetwin = PlanetWin(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        snai = Snai(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        # eurobet.main()
        # betaland.main()
        # betfair.main()
        # betflag.main()
        # goldbet.main()
        # lottomatica.main()
        # planetwin.main()
        # snai.main()
        self.epoch = self.epoch + 1

    def test(self):
        threading.Timer(1, self.test).start()
        print(datetime.fromtimestamp(time.time()))
        print(self.epoch)
        self.epoch = self.epoch + 1


if __name__ == "__main__":
    odds_matcher = OddsMatcher()
    odds_matcher.run()