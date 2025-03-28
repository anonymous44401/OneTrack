import sqlite3

class Database():
    def __init__(self, database: str):
        self.__database = database
        # Connect
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()
        # Commit
        self.__conn.commit()
        # Close
        self.__conn.close()
    
    def _get_all_values(self, from_table: str) -> list | None:
        # Connect
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()

        # Get value(s) from the database with command
        value_found = self.__cursor.execute(f"SELECT * FROM {from_table}")
        self.__conn.commit()

        try:
            # Empty list for the values
            values_found = []
            # Iterate over each value and append it to the list
            for each in value_found:
                values_found.append(list(each))

            return values_found
        
        except:
            return None

    def _get_all_values_in_order(self, from_table: str, order_by_query: str) -> list | None:
        # Connect
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()

        # Get value(s) from the database with command
        value_found = self.__cursor.execute(f"SELECT * FROM {from_table} ORDER BY {order_by_query}")
        self.__conn.commit()

        try:
            # Empty list for the values
            values_found = []
            # Iterate over each value and append it to the list
            for each in value_found:
                values_found.append(list(each))

            return values_found
        
        except:
            return None

    def _get_values(self, find_value: str, from_table: str, condition_is_true: str, argument: str) -> list | None | str:
        # Connect
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()    

        # Get value from the database with command
        value_found = self.__cursor.execute(f"SELECT {find_value} FROM {from_table} WHERE {condition_is_true} = '{argument}'")
        self.__conn.commit()

        try:
            # Empty list for the values
            values_found = []
            # Iterate over each value and append it to the list
            for each in value_found:
                values_found.append(list(each))

            return values_found[0][0]
    
        except:
            return None

    def _get_values_in_order(self, find_value: str, from_table: str, condition_is_true: str, argument: str, order_by_query: str) -> list | None | str:
        # Connect
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()    

        # Get value from the database with command
        values_found = self.__cursor.execute(f"SELECT {find_value} FROM {from_table} WHERE {condition_is_true} = '{argument}' ORDER BY {order_by_query}")
        self.__conn.commit()

        try:
            # Empty list for the values
            values = []
            # Iterate over each value and append it to the list
            for each in values_found:
                values.append((list(each))[0])

            return values
        
        except:
            return None

    def _insert_values(self, into_table: str, columns: str, values: list) -> None:
        # Connect
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()

        # Create first half of the database command 
        db_cmd = f"INSERT INTO {into_table} ({columns}) VALUES ("

        for i in range(len(values)-1):
            # Add values to the end of the command
            db_cmd += f"'{str(values[i])}',"
        
        # Add final value to the end of the command
        db_cmd += f"'{str(values[-1])}');"

        self.__cursor.execute(db_cmd)
        self.__conn.commit()
        
    def _update_values(self, in_table: str, att_to_change: str, val_to_change: str, attribute: str, value: str) -> None:
        # Connect
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()

        # Update values with the command
        self.__cursor.execute(f"UPDATE {in_table} SET {att_to_change} = {val_to_change} WHERE {attribute} = {value}")
        self.__conn.commit()

    def _delete_values(self, table: str, attribute: str, input: str, attribute2: str=None, input1: str=None) -> None:
        # Connect
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()

        # Delete values with command
        if attribute2 != None and input1 != None:
            self.__cursor.execute(f"DELETE FROM {table} WHERE {attribute} = '{input}' AND {attribute2} = '{input1}'")
        else:
            self.__cursor.execute(f"DELETE FROM {table} WHERE {attribute} = '{input}'")
        
        self.__conn.commit()
