import mysql.connector

class DbManager:
    mydb = mysql.connector.connect(
        host = "45.8.227.145",
        user = "oddsmatcher",
        password = "~exY([5~fjxN",
        database = "oddsmatcher-353030358ce0",
        port = "53934"
    )

    def __init__(self):
        self.mycursor = self.mydb.cursor()
        # self.start()

    def create_table(self):
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS `python_odds_table` (`id` BIGINT(20) NOT NULL AUTO_INCREMENT,`category` varchar(255),`subcategory` varchar(255),`team1` varchar(255),`team2` varchar(255),`event_date` varchar(255),`event_time` varchar(255),`equal` varchar(255),`first` varchar(255),`second` varchar(255),`draw` varchar(255),`under` varchar(255),`over` varchar(255),`gg` varchar(255),`ng` varchar(255),`bookmarker` varchar(255),`created_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (`id`));")

    def check(self):
        self.mycursor.execute("SHOW TABLES")
        for x in self.mycursor:
            print(x)

    def get_data(self):
        self.mycursor.execute("SELECT * FROM `python_odds_table` where `bookmarker` = 'eurobet'")
        result = self.mycursor.fetchall()
        print(len(result))
        # for x in result:
        #     print(x)

    def drop_table(self):
        self.mycursor.execute("DROP TABLE `python_odds_table`")

    def insert_data(self, odds_list):
        sql = "INSERT INTO `python_odds_table` (`category`, `subcategory`, `team1`, `team2`, `event_date`, `event_time`, `equal`, `first`, `second`, `draw`, `under`, `over`, `gg`, `ng`, `bookmarker`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.executemany(sql, odds_list)
        self.mydb.commit()
        print(self.mycursor.rowcount, "was inserted")

    def start(self):
        # self.drop_table()
        self.create_table()
        self.check()
        self.get_data()
        # self.check()

if __name__ == "__main__":
    db_manager = DbManager()
    db_manager.start()