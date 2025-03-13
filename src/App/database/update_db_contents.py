#######################################
# FUNCTIONS FOR UPDATING THE STATIONS #
# IN THE DATABASE AUTOMATICALLY       #
#######################################

import requests

from bs4 import BeautifulSoup

from src.app.site_database import Database

class UpdateDBContents(Database):
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
    def _update_stations(self):
        reference_dict = self.__get_db_stations()
        
        uk_stations = self.__get_web_stations()
        self.__compare_stations(uk_stations, reference_dict)