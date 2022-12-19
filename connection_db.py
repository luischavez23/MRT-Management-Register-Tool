import sqlite3

class Asset:
    
    def open_db(self):
        connection_db = sqlite3.connect('V:\\HSIO_LabSupport\\SitrackDB.db')
        return connection_db

    def insert_db(self, datas):
        connection_db = self.open_db()
        cursor = connection_db.cursor()
        query = "INSERT INTO SiManagment (BarcodeId, AssetId, LocationID, User, Date) VALUES (?,?,?,?,?)" 
        cursor.execute(query, datas)
        connection_db.commit()
        connection_db.close()

    def category_list(self, data):
        try:
            connection_db =self.open_db()
            cursor=connection_db.cursor()
            query = f"SELECT BarcodeId, LocationID, User, STRFTIME('%Y/%m/%d, %H:%M', Date), AssetId FROM SiManagment WHERE AssetId LIKE '%{data}%'"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        finally:
            connection_db.close()

    def select_db(self, datas, allhistory):
        """
        This method access to database to extract requested data.

        We have 2 different options:
        - Last location: This is the default option, and it displays the last location of the barcode, 
        the most recent user, and the last date used.
        - All history:  To use this function, a Marked Box must be selected. 
        This allows users to view all barcode movements from the beginning.
        """
        try:
            connection_db = self.open_db()
            cursor=connection_db.cursor()
            format_strings = ', '.join("'"+barcode+"'" for barcode in datas) #Make a data set that meets the necessary SQL requirements to be joined to the query: 'M232323','M456789'.... 

            if allhistory:
                all_history_query = "SELECT BarcodeId, LocationID, User, STRFTIME('%Y/%m/%d, %H:%M', Date), AssetId FROM SiManagment WHERE BarcodeId IN ({0}) ORDER BY BarcodeId".format(format_strings)
                cursor.execute(all_history_query)
                rows = cursor.fetchall()
                return rows
            else:
                """
                ---last_location_query---

                This query has the sub-query application, where the inner query we get a table with the requested data,
                and the outer query get the last location from the inner query table. 

                --INNER QUERY--
                SELECT * FROM SiManagment WHERE BarcodeId IN ({0})

                This inner query creates a table with only the requested data set in ({0}).

                --OUTER QUERY---
                SELECT BarcodeId, LocationID, User, MAX(Date), AssetId FROM(--INNER QUERY shoulb be here--) GROUP BY BarcodeId

                This query filters the data by the last date, and groups each requested barcode.

                """
                last_location_query = "SELECT BarcodeId, LocationID, User, MAX(STRFTIME('%Y/%m/%d, %H:%M', Date)), AssetId FROM(SELECT * FROM SiManagment WHERE BarcodeId IN ({0})) GROUP BY BarcodeId".format(format_strings)
                cursor.execute(last_location_query)
                rows = cursor.fetchall()
                return rows       
        finally:
            connection_db.close()
   
   #What's next:

   #Create an special word to get the all the silicons that have not been using for x time.

   #The user nees to type something like this in the search page: noinuse silicons -2m 