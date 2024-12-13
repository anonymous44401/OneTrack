import sqlite3

class Database():
    def __init__(self):
        self.__database = 'OneTrack_database.db'
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()
        self.__conn.commit()
        self.__conn.close()
    

    def _get_all_values(self, __from_table: str) -> list | str:
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()

        __dbCmd = "SELECT * FROM " + __from_table
        #print(__dbCmd)
        __value_found = self.__cursor.execute(__dbCmd)
        self.__conn.commit()
        #print(__value_found)

        if __value_found != None:
            try:
                __values_found = []
                for each in __value_found:
                    #print(__values_found[each])
                    __values_found.append(list(each))

                #print(values_found)
                __return_value = __values_found
                return __return_value
            except:
                return None
        else:
            return None

    def _get_all_values_in_order(self, __from_table: str, __order_by_query: str) -> list | str:
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()

        __dbCmd = "SELECT * FROM " + __from_table + " ORDER BY " + __order_by_query
        #print(__dbCmd)
        __value_found = self.__cursor.execute(__dbCmd)
        self.__conn.commit()
        #print(__value_found)

        if __value_found != None:
            try:
                __values_found = []
                for each in __value_found:
                    #print(__values_found[each])
                    __values_found.append(list(each))

                #print(values_found)
                __return_value = __values_found
                return __return_value
            except:
                return None
        else:
            return None


    def _get_values(self, __find_value: str, __from_table: str, __condition_is_true: str, __argument: str) -> list | str:
        # Can only be used to find one or all value(s) at a time so far
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()
        
        __dbCmd = "SELECT " + __find_value + " FROM " + __from_table + " WHERE " + __condition_is_true + " = \"" + __argument + "\""

        #print("DATABASE COMMAND:: " + __dbCmd)

        __value_found = self.__cursor.execute(__dbCmd)
        self.__conn.commit()

        if __value_found != None:
            try:
                __values_found = []
                for each in __value_found:
                    __values_found.append(list(each))

                #print(values_found)
                __return_value = __values_found[0][0]
                return __return_value
            except:
                return None
        else:
            return None


    def _insert_values(self, __into_table: str, __columns: str, __values: list) -> None:
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()
        __find_in_columns = __columns

        #print(find_in_columns)
        
        __dbCmd: str = "INSERT INTO " + __into_table + " (" + __find_in_columns + ") VALUES ("
        #print(dbCmd)
        for i in range(len(__values)-1):
            #print(values[i])
            __dbCmd += "\"" + str(__values[i]) + "\"" + ","
            #print(dbCmd)

        #print("EXIT", dbCmd)
        __dbCmd += "\"" + __values[-1] + "\"" + ");"

        #print(dbCmd)
        self.__cursor.execute(__dbCmd)
        self.__conn.commit()
        

    def _update_values(self, __in_table: str, __att_to_change: str, __val_to_change: str, __attribute: str, __value) -> None:
        # Can only update one value at a time
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()

        __dbCmd = "UPDATE " + __in_table + " SET " + __att_to_change + " = " + __val_to_change + " WHERE " +  __attribute + " = " + __value
        
        #print(dbCmd)
        self.__cursor.execute(__dbCmd)
        self.__conn.commit()


    def _delete_values(self, __table: str, __attribute: str, __input: str) -> None:
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()

        __dbCmd = "DELETE FROM " + __table + " WHERE " + __attribute + " = " "\"" + str(__input) + "\""
        
        #print(dbCmd)
        self.__cursor.execute(__dbCmd)
        self.__conn.commit()
