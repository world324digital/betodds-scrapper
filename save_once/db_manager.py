import mysql.connector

class DbManager:

    def __init__(self):
        self.host = "45.8.227.145"
        self.user = "oddsmatcher"
        self.password = "~exY([5~fjxN"
        self.database = "oddsmatcher-353030358ce0"
        self.port = "57558"
        self.mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            port = self.port
        )
        # self.start()

    def create_table(self):
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            port = self.port
        )
        # mycursor = mydb.cursor()
        mycursor = self.mydb.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS `python_odds_table_new` (`id` BIGINT(20) NOT NULL AUTO_INCREMENT,`category` varchar(255),`subcategory` varchar(255),`team1` varchar(255),`team2` varchar(255),`event_date` varchar(255),`event_time` varchar(255),`equal` varchar(255),`first` varchar(255),`second` varchar(255),`draw` varchar(255),`under` varchar(255),`over` varchar(255),`gg` varchar(255),`ng` varchar(255),`bookmarker` varchar(255),`epoch_date_time` varchar(255),`created_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, `deleted_at` TIMESTAMP DEFAULT NULL,PRIMARY KEY (`id`));")

    def check(self):
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            port = self.port
        )
        # mycursor = mydb.cursor()
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW TABLES")
        for x in mycursor:
            print(x)

    def get_data(self):
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            port = self.port
        )
        # mycursor = mydb.cursor()
        mycursor = self.mydb.cursor()
        # mycursor.execute("SELECT * FROM `python_odds_table_new` where `bookmarker` = 'betaland'")
        mycursor.execute("SELECT * FROM `python_odds_table_new`")
        result = mycursor.fetchall()
        print(len(result))
        for x in result:
            print(x)

    def drop_table(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("DROP TABLE `python_odds_table_new`")

    def insert_data(self, odds_list):
        # mydb = mysql.connector.connect(
        #     host = self.host,
        #     user = self.user,
        #     password = self.password,
        #     database = self.database,
        #     port = self.port
        # )
        sql = "INSERT INTO `python_odds_table_new` (`category`, `subcategory`, `team1`, `team2`, `event_date`, `event_time`, `equal`, `first`, `second`, `draw`, `under`, `over`, `gg`, `ng`, `bookmarker`, `epoch_date_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        if len(odds_list) > 0:
            # mycursor = mydb.cursor()
            mycursor = self.mydb.cursor()
            mycursor.executemany(sql, odds_list)
            # mydb.commit()
            self.mydb.commit()
            mycursor.close()
            print(odds_list[0][-2])
            print(mycursor.rowcount, "was inserted")
    
    def insert_row(self, odds_list):
        # mydb = mysql.connector.connect(
        #     host = self.host,
        #     user = self.user,
        #     password = self.password,
        #     database = self.database,
        #     port = self.port
        # )
        sql = "INSERT INTO `python_odds_table_new` (`category`, `subcategory`, `team1`, `team2`, `event_date`, `event_time`, `equal`, `first`, `second`, `draw`, `under`, `over`, `gg`, `ng`, `bookmarker`, `epoch_date_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # mycursor = mydb.cursor()
        mycursor = self.mydb.cursor()
        mycursor.execute(sql, odds_list)
        # mydb.commit()
        self.mydb.commit()
        mycursor.close()
        # print(mycursor.rowcount, "was inserted")

    def start(self):
        self.drop_table()
        self.create_table()
        self.check()
        row = ("list_title", "sub_title", 'team1', "team2", "event_date", "event_time", "equal", "first", "second", "draw", "under", "over", "gg", "ng", "betway", "self.epoch_time")
        self.insert_row(row)
        self.get_data()
        mycursor = self.mydb.cursor()
        sql = "UPDATE `python_odds_table_new` SET `sub_title` = 'sub_title' WHERE `list_title` = 'list_title'"
        mycursor.execute(sql)
        mydb.commit()
        self.get_data()
        # self.check()

if __name__ == "__main__":
    db_manager = DbManager()
    db_manager.start()