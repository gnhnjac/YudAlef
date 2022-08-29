import sqlite3
import random


class OrganRequestManager():

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.id = 0
        self.open_DB()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Organs (
                                Id int PRIMARY KEY NOT NULL,
                                DealerName varchar(255) NOT NULL,
                                Type varchar(30) NOT NULL,
                                Price int NOT NULL,
                                ExpirationYear int(4) NOT NULL,
                                ExpirationMonth int(2) NOT NULL
                                );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Dealers (
                                DealerName varchar(255) NOT NULL,
                                Balance int NOT NULL
                                );""")

        max_id = list(self.cursor.execute("SELECT Id FROM Organs WHERE Id = (SELECT max(Id) FROM Organs)"))
        if max_id:
            self.id = max_id[0][0] + 1

        self.close_DB()

    def open_DB(self) -> None:
        self.conn = sqlite3.connect('TheSilkRoad.db')
        self.cursor = self.conn.cursor()

    def close_DB(self) -> None:
        self.conn.close()

    def commit(self) -> None:
        self.conn.commit()

    def get_all_organs(self):
        self.open_DB()
        organs = list(self.cursor.execute("SELECT * FROM Organs"))
        self.close_DB()
        return organs
    
    def get_organs_by_type(self, organ_type):
        self.open_DB()
        organs = []

        for row in self.cursor.execute("SELECT * FROM Organs WHERE Type = ?", (organ_type,)):
            organs.append(row)
        
        self.close_DB()
        return organs

    
    def get_organ_by_id(self, organ_id):

        res = self.cursor.execute("SELECT * FROM Organs WHERE Id = ?", (organ_id,))

        return res

    def add_new_organ(self, dealer_name, organ_type, organ_price, organ_expiration_date):
        """
        
        Inserts a new organ into the database.
        
        dealer_name -> The name of the dealer.
        organ_type -> The type of the organ.
        organ_price -> The price of the organ.
        organ_expiration_date -> The expiration date of the organ. format --> MM-YYYY

        """

        expiration_year = int(organ_expiration_date.split('-')[1])
        expiration_month = int(organ_expiration_date.split('-')[0])

        self.open_DB()
        self.cursor.execute("INSERT INTO Organs VALUES (?, ?, ?, ?, ?, ?);", (self.id, dealer_name, organ_type, organ_price, expiration_year, expiration_month))
        self.id += 1
        self.commit()
        self.close_DB()

    def buy_organ(self, organ_id, buyer_name):
        self.open_DB()
        
        organ = list(self.get_organ_by_id(organ_id))[0]

        self.cursor.execute("UPDATE Dealers SET Balance = BALANCE + ? WHERE DealerName = ?", (organ[3], organ[1]))
        self.cursor.execute("UPDATE Dealers SET Balance = BALANCE - ? WHERE DealerName = ?", (organ[3], buyer_name))
        self.cursor.execute("DELETE FROM Organs WHERE Id = ?", (organ_id,))
        self.id -= 1
        
        self.commit()
        self.close_DB()

        return organ
    
    def add_new_dealer(self, dealer_name, dealer_balance):
        self.open_DB()
        self.cursor.execute("INSERT INTO Dealers VALUES (?, ?);", (dealer_name, dealer_balance))
        self.commit()
        self.close_DB()
    
    def get_dealer_balance(self, dealer_name):
        self.open_DB()
        balance = list(self.cursor.execute("SELECT Balance FROM Dealers WHERE DealerName = ?", (dealer_name,)))
        self.close_DB()
        return balance[0][0]

if __name__ == '__main__':
    orm = OrganRequestManager()
    # organ_list = ['Heart', 'Liver', 'Kidney', 'Lung', 'Intestine', 'Pancreas', 'Stomach', 'Bladder', 'Gallbladder', 'SmallIntestine', 'Spleen', 'Thymus']
    # orm.add_new_dealer('John', 1000)
    # orm.add_new_dealer('Paul', 1000)
    # orm.add_new_dealer('George', 1000)
    # orm.add_new_dealer('Ringo', 1000)
    # for i in range(1000):
    #     orm.add_new_organ(random.choice(['John', 'Paul', 'George', 'Ringo']), random.choice(organ_list), random.randint(0,10000), f'{str(random.randint(1,12)).zfill(2)}-{str(random.randint(0,2100)).zfill(4)}')
