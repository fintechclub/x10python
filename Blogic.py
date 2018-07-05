import sqlite3


class BusinessLogic: 
    
    def __init__(self):
        self.__dataBaseName = "assets.db"
        self.db_connection = sqlite3.connect(self.__dataBaseName)  # или :memory: чтобы сохранить в RAM
        self.__initScheme()
        
    def __initScheme(self):
        create_table = "CREATE TABLE IF NOT EXISTS wallets (address TEXT, title TEXT, balance integer); \
                        CREATE TABLE IF NOT EXISTS assets (asset text, exchange text);"
        cursor = self.__getCursor()
        cursor.executescript(create_table)
        
    def __getCursor(self):
        return self.db_connection.cursor()
    
    def refreshAssetDB(self, assets, exchange):  
        cursor = self.db_connection.cursor()
        cursor.execute("delete from assets where exchange=?", [(exchange)]) 
        cursor.executemany("INSERT INTO assets VALUES (?,?)", assets)
        self.db_connection.commit()

    def getAssetsFromDB(self, exchange):
        cursor = self.__getCursor()
        cursor.execute("select * from assets where exchange=?", [(exchange)])
        return cursor.fetchall()
    
    def deleteBTC(self, exchange):
        self.__getCursor().execute("delete from assets where asset='BTC' and exchange=?", [(exchange)] )
        self.db_connection.commit()

    def getAssetCount(self, exchange):
        cursor = self.__getCursor()
        cursor.execute("select count(*) from assets where exchange=?", [(exchange)])
        return cursor.fetchone()
    
    
    def refreshWalletsTable(self, data):
        cursor = self.db_connection.cursor()
        cursor.execute("delete from wallets") 
        cursor.executemany("INSERT INTO wallets VALUES (?,?,?)", data)
        self.db_connection.commit()
        
    def getWalletsTable(self):
        cursor = self.__getCursor()
        cursor.execute("select address, balance from wallets")
        return cursor.fetchall()
    