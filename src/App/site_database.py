import requests
import sqlite3

from bs4 import BeautifulSoup

class Database():
    def __init__(self):
        # Get the database ready
        self.__database = 'src/app/database/OneTrack_database.db'
        # Connect
        self.__conn = sqlite3.connect(self.__database)
        self.__cursor = self.__conn.cursor()
        # Commit
        self.__conn.commit()
        # Close
        self.__conn.close()

        update = False

        # Update the stations if we need to. There's no point in doing this every time;
        # it'll take too long to start the site.
        if update:
            self.__update_stations()
    
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


    #######################################
    # FUNCTIONS FOR UPDATING THE STATIONS #
    # IN THE DATABASE AUTOMATICALLY       #
    #######################################

    # Get the stations from the database
    def __get_db_stations(self) -> dict:
        # Create dictionary of all stations
        all_stations: dict = {}
        # Get all stations from the database
        stations: list = self._get_all_values_in_order("tblStations", "StationName")
        for att in stations:
            # Add each pair of values to the dictionary
            all_stations[att[0]] = att[1]

        # Return and clear
        stations.clear()
        return all_stations
    
    # Get the stations from the web
    def __get_web_stations(self) -> dict:
        letters = [
            "A", "B", "C", "D", "E", "F", 
            "G", "H", "I", "J", "K", "L", 
            "M", "N", "O", "P", "Q", "R", 
            "S", "T", "U", "V", "W", "Y"
        ] 
        station_dict = {}

        # Iterate over each letter in letters
        for letter in range(0, len(letters)):
            l = letters[letter]
            url = f"https://en.wikipedia.org/wiki/UK_railway_stations_-_{l}"

            print(f"Searching for items in '{l}'")
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"Failed to retrieve data for {l}")
            
            # Get the data
            data = BeautifulSoup(response.text, 'html.parser')
            
            # Find the table
            tables = data.find_all("table", {"class": "wikitable"})
            
            # Check each table
            for table in tables:
                rows = table.find_all("tr")[1:]  # Skip header row
                # Check each row
                for row in rows:
                    # Get all the data from each row
                    cols = row.find_all("td")
                    # Get the info from the columns if there are more than 3
                    if len(cols) >= 3:
                        station_name = cols[0].text.strip().upper() # Get the station name
                        crs_code = cols[2].text.strip() # Get the CRS code
                        station_dict[station_name] = crs_code # Add to the dict
        
        return station_dict
    
    # Compare the stations in the database to the scraped stations
    def __compare_stations(self, scraped_stations, stations_in_db):
        # For each station and crs in the scraped stations
        for station, crs in scraped_stations.items():
            if station not in stations_in_db:
                # If the station is not in the dictionary, check a CRS is provided and add to the database
                if crs != "":
                    try:
                        self._insert_values(
                            "tblStations",
                            "StationName, CRS",
                            [station, crs]
                        )
                        print(f"Inserted {station} [{crs}] into the database")

                    except:
                        print(f"Failed to add {station} [{crs}]")

    # Update the stations in the database
    def __update_stations(self):
        reference_dict = self.__get_db_stations()
        
        uk_stations = self.__get_web_stations()
        self.__compare_stations(uk_stations, reference_dict)