import sqlite3


class BusinessLogic(object): 
    
    def __init__(self):
        self.__dataBaseName = "assets.db"
        self.db_connection = sqlite3.connect(self.__dataBaseName)  # или :memory: чтобы сохранить в RAM
    
        
    def refreshAssetDB(self, assets, exchange):  
        cursor = self.db_connection.cursor()
        cursor.execute("delete from assets where exchange=?", [(exchange)]) 
        cursor.executemany("INSERT INTO assets VALUES (?,?)", assets)
        self.db_connection.commit()

    def getAssetsFromDB(self, exchange):
        cursor = self.db_connection.cursor()
        cursor.execute("select * from assets where exchange=?", [(exchange)])
        return cursor.fetchall()
    
    def deleteBTC(self, exchange):
        cursor = self.db_connection.cursor()
        cursor.execute("delete from assets where asset='BTC' and exchange=?", [(exchange)] )
        self.db_connection.commit()

    def getAssetCount(self, exchange):
        cursor = self.db_connection.cursor()
        cursor.execute("select count(*) from assets where exchange=?", [(exchange)])
        return cursor.fetchone()