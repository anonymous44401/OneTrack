#####################################
# METHODS FOR UPDATING THE STATIONS #
# IN THE DATABASE AUTOMATICALLY     #
#####################################

import requests
import sqlite3

from bs4 import BeautifulSoup

class UpdateDBContents():    
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

            print(f"Searching for items in '{l}'")
            response = requests.get(f"https://en.wikipedia.org/wiki/UK_railway_stations_-_{l}")
            
            if response.status_code != 200:
                print(f"Failed to retrieve data for '{l}'")
            
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
    def __add_new_stations(self, scraped_stations):
        database = 'src/app/database/OneTrack_database.db' ### Rename DB here to update data.
        # Connect
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        # Commit
        conn.commit()
        # Close
        # For each station and crs in the scraped stations
        f = []
        for station, crs in scraped_stations.items():
            if crs != "":
                try:
                    # Try inserting the station and crs into the database
                    cursor.execute(f"INSERT INTO tblStations (StationName, CRS) VALUES ('{station}', '{crs}');")
                    conn.commit()
                    print(f"Inserted {station} [{crs}] into the database")

                except:
                    f.append(f"Failed to add {station} [{crs}]")
        
        for x in f:
            print(x)

    # Update the stations in the database
    def _update_stations(self):        
        uk_stations = self.__get_web_stations()
        self.__add_new_stations(uk_stations)
        print("Stations updated.")