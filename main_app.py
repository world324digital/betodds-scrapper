import threading
import time
from datetime import datetime
from betway import BetWay

class OddsMatcher:

    def __init__(self):
        self.epoch = 1

    def run(self):
        threading.Timer(60, self.run).start()
        now_time = datetime.fromtimestamp(time.time())
        print(self.epoch)
        betway = BetWay(self.epoch, now_time.strftime("%Y-%m-%d %H:%M:%S"))
        betway.main()
        self.epoch = self.epoch + 1

    def test(self):
        threading.Timer(1, self.test).start()
        print(datetime.fromtimestamp(time.time()))
        print(self.epoch)
        self.epoch = self.epoch + 1


if __name__ == "__main__":
    odds_matcher = OddsMatcher()
    odds_matcher.run()