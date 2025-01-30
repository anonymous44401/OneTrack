from datetime import datetime


from App.encryption import Encryption
from App.site_database import Database
from realtime_trains_py import RealtimeTrainsPy


class SiteInternalSystem():
    def __init__(self) -> None:
        self._time_created: tuple = ("Site created:", self._get_now(3))
        self.__close_access: bool = False
        self.__database: Database = Database() # Database
        self.__encryption: Encryption = Encryption() # Encryption
        self.__fail_count: int = 0
        self.__signed_in: bool = False
        self._username: str = ""
        
        try:
            # Initialise RealtimeTrainsPy using the credentials from the .txt files            
            self.__rtt: RealtimeTrainsPy = RealtimeTrainsPy(complexity = "s.n", username = self.__encryption._rtt_user, password = self.__encryption._rtt_token)
            # Test the connection
            self.__rtt.get_departures(tiploc = "WAT")

            self._rtt_departures_failed: bool = False
        except:
            # If an error occurs, report it
            self._report_error("Couldn't connect to RTT API Service in __init__")
            self._rtt_departures_failed: bool = True
        

        # Create dictionary of all stations
        self._all_stations: dict = {}
        # Get all stations from the database
        all_stations: list = self.__database._get_all_values_in_order("tblStations", "StationName")
        for att in all_stations:
            # Add each pair of values to the dictionary
            self._all_stations[att[0]] = att[1]

        self._site_version: str = "V2.1.1 [ALPHA]"
        

    #SECTION - Departures
    def _get_departures(self, station_name) -> str | tuple:
        # Reset the departures to prevent any conflicts
        self._reset_departures()
        
        # Check if an error occurred initialising realtime-trains-py
        if self._rtt_departures_failed != True:
            return_date = self._get_now(1) # Date now
            self._send_station = station_name.title() # Convert station name to title case

            try:
                # Try to get the station CRS code from the database and get its departure board
                self._send_code = self.__database._get_values("SID", "tblStations", "StationName", (self._send_station.upper()))
                self._send_service = self.__rtt.get_station(tiploc = self._send_code)
                

            except:
                self._send_code = station_name
                # Use the station CRS code to get its departure board
                self._send_station = self.__database._get_values("StationName", "tblStations", "SID", (self._send_code.upper()))
                self._send_service = self.__rtt.get_station(tiploc = self._send_code)
                
            # Return the return information
            return 'departureResults.html', self._send_station.title(), self._send_code, self._send_service, return_date
        
        else:
            # Report the error and return departuresFailed
            self._report_error("Failed to connect to RTT API Service in _get_rtt_departures")
            return "departuresFailed.html", None, None, None, None

    def _get_stations_dict(self) -> dict:
        # Return all stations
        return self._all_stations

    def _get_station_name(self, station_crs) -> None | str:
        # Get the station name from the database
        return self.__database._get_values("StationName", "tblStations", "SID", station_crs)

    def _get_user_favorites(self) -> list | str:
        # Check if the username is null
        if self._username != "":
            return_values: list = []
            for i in range (1, 7):
                # Get 6 favorites from the database
                favorite = self.__database._get_values(("Favorite" + str(i)), "tblUserFavorites", "UserID", self.__userID)

                # Check if the favorite is None
                if str(favorite) != "None":
                    # Get the CRS of the station
                    favorite_crs = self.__database._get_values("SID", "tblStations", "StationName", (favorite.upper()))
                    return_values.append([favorite.title(), favorite_crs])
                else:
                    # Break if none
                    break
                
            return return_values

        else:
            return "None"

    def _reset_departures(self) -> None:
        # Set departures related variables to empty
        self._send_station = ""
        self._send_service = []
        self._send_code = ""

    def _get_service_info(self, service_uid) -> list:
        # Return the service info
        return self.__rtt.get_service(service_uid = service_uid)


    #SECTION Planner
    def _search_planner(self, origin, destination, departure_date, departure_time) -> None:
        date_now = self._get_now(2)

        self.__database._insert_values("tblTicketQueries", "Origin, Destination, DepDate, DepTime, RequestDate, RequestTime", 
                                    [origin, destination, departure_date, departure_time, date_now[0], date_now[1]])
    

    #SECTION Search
    def _search_for_item(self, search_request) -> str:
        pages: list = self._get_pages_list # List of pages

        # Check if the search request is in pages
        if search_request in pages:
            return f"{search_request} was found on the search results page."
        
        else:
            return f"{search_request} was not found. Check your spelling and try again."
        
    def _get_pages_list(self) -> list:
        # Return a list of pages
        return ['About', 'Contact', 'Create Account', 'Departures', 'Home', 'myOneTrack', 'Planner', 'Privacy Policy', 'Terms of Service']


    #SECTION Account handling 
    def _sign_in(self, username, check_password) -> str:
        # Get the user password
        username = self.__hash_item(username)
        correct_password = self.__database._get_values(
            "Password", 
            "tblUsers", 
            "Username", 
            username
        )

        # Check if the provided password matches the password in the db
        if self.__encryption._validate_items(check_password, correct_password):
            # Set the user ID, username and state
            self.__signed_in = True
            self._username: str = username
            self.__userID: str = str(self.__database._get_values("UserID", "tblUsers", "Username", username))
            return self._username

        else:
            # Iterate the fail count
            self.__fail_count += 1
            self.__signed_in = False

            # If fail count is 3, reset fail count and apply an infinite server lock
            if self.__fail_count == 3:
                self.__fail_count = 0    
                self.__close_access = True

            return None

    def _create_account(self, first_name: str, surname: str, email: str, username: str, password1: str, password2: str) ->  bool | str:
        continue_search: bool = True
        username_fail: bool = False
        password_valid: bool = False
        email_fail: bool = False

        # Hash each item
        first_name: str = self.__hash_item(first_name)
        surname: str = self.__hash_item(surname)
        email: str = self.__hash_item(email)
        username: str = self.__hash_item(username)

        # Check if the password meets validation requirements
        password_valid: bool = self.__validate_password(password1)

        # Check if the passwords are equal
        if password1 == password2 and password_valid:
            # Check if the username already exists
            search_for_username = self.__database._get_values("UserID" , "tblUsers", "Username", username)
            if search_for_username != None:
                username_fail = True
                continue_search = False

            # Check if the email already exists
            search_for_email = self.__database._get_values("UserID" , "tblUsers", "Email", email)
            if search_for_email != None:
                email_fail = True
                continue_search = False
            
            # Hash the password
            password: str = self.__hash_item(password1)

            if continue_search:
                try:
                    # Insert user details
                    self.__database._insert_values(into_table="tblUsers", columns="FirstName, Surname, Username, Email, Password", values=[first_name, surname, username, email, password])
                    # Get user ID
                    self._user_id = self.__database._get_values("UserID" , "tblUsers", "Email", email)
                    # Add their favorites
                    self.__database._insert_values("tblUserFavorites", "UserID, Favorite1, Favorite2, Favorite3, Favorite4, Favorite5, Favorite6", [self._user_id, None, None, None, None, None, None])

                    self.__signed_in = True
                    self._username = username

                    return True, self._username
                except:
                    # Report an error if an error occurs
                    self._report_error("***Database crash detected.")
                    return False, "An unexpected error occurred in the database. Try again."

        # Return errors based on failure types
            elif email_fail and username_fail:
                return False, "The username and email you entered appear to be taken. Try a different one."
            
            elif email_fail and not username_fail:
                return False, "The email you entered appears to be taken. Try a different one."

            elif not email_fail and username_fail:
                return False, "The username you entered appears to be taken. Try a different one."

            else:
                return False, "An unexpected error occurred. Try again."

        elif not password_valid:
            return False, "The password you entered doesn't meet the requirements. Try again."

        else:
            return False, "The passwords you entered don't match. Try again."

    def _update_settings(self) -> None:
        raise NotImplementedError("Code not added yet.")
    
        self.__database._update_values("tblUserSettings")
    
        #NOTE Needs to allow user to update settings in the database 

    #FIXME Not implemented
    def _get_operator_status(self) -> str:
        get_status = self.__database._get_values("OperatorStatus", "tblUserSettings", "username", self._username)

        return get_status

    def _sign_out(self) -> None:
        # Set username to null and state to false
        self.__signed_in = False
        self._username = ""

    def _check_sign_in(self) -> bool | str:
        # Check if the user is signed in
        if self.__signed_in == True:
            return self._username

        else:
            return False

    def _get_friend_items(self) -> list:
        # Get the user's friends
        friends = self.__database._get_values("UserFriend", "tblFriends", "UserID", self._user_id)
        friend_requests = self.__database._get_values("RequesterID", "tblFriendRequests", "UserID", self._user_id)

        return friends, friend_requests

    #FIXME Not implemented
    def _update_account(self) -> None:
        raise NotImplementedError("Code not added yet.")
        #NOTE See update_settings
        self.__database._update_values()

    def _delete_account(self) -> bool:
        # Check if the username is null
        try:
            # Try removing the values from the database
            self.__database._delete_values("tblUsers", "Username", self._username)
            self.__database._delete_values("tblUserSettings", "UserID", self._user_id)

            # Set the username and state
            self.__signed_in = False
            self._username = None
            self._user_id = None
            return True
        
        except:
            # Set the username and state
            self.__signed_in = True
            return False

    def _shutdown(self) -> bool:
        # Check if shutdown
        if self.__close_access == True:
            # Set all vars to default state
            self._shutdown_time = ("Site shutdown:", self._get_now(3))
            self.__close_access = True
            self._send_station = ""
            self._send_service = []
            self.__signed_in = False
            self._send_code = ""
            self._username = ""

        return self.__close_access

    # Report error 
    def _report_error(self, error) -> None:
        try:
            # Open the file
            with open("home/crash_logs.txt", "a") as file:
                # Write the error to the file
                file.write("\n\n" + str(error) + "\n" + str(self._get_now(3)))
        except:
            pass

    # Get the current time
    def _get_now(self, type) -> bool | str | tuple:
        now = datetime.now()

        # Format based on selection type
        if type == 1:
            # 31/12/2024 at 23:59
            realdate = now.strftime("on %d/%m/%Y at %H:%M")
            
            return realdate
            
        elif type == 2:
            # 31-12-2024
            realdate = now.strftime("%d-%m-%Y")
            # 23:59:59
            realtime = now.strftime("%H:%M:%S")

            return realdate, realtime
        
        elif type == 3:
            # on 31/12/2024 at 23:59:59
            realdate = now.strftime("on %d/%m/%Y at %H:%M:%S")
            return realdate

        elif type == 4:
            # 31/12/2024 at 23:59:50
            realdate = now.strftime("%d/%m/%Y at %H:%M:%S")
            return realdate

        else:
            return None

    # Hashing 
    def __hash_item(self, content) -> str:    
        # Hash and return the item    
        return self.__encryption._encrypt_item(content)

    # Password validation
    def __validate_password(self, content: str) -> bool:
        # Password validation rules
        # 1. Minimum length of 8 characters
        # 2. At least one uppercase letter
        # 3. At least one lowercase letter
        # 4. At least one digit
        # 5. At least one special character (!@#$%^&*)
        # 6. No spaces

        # Check if the password contains spaces
        if content == ("".join(content.split())):
            # Check if the password is greater than 8 characters
            if len(content) >= 8:
                # Check if there is an uppercase character in the password
                if any(char.isupper() for char in content):
                    # Check if there is a lowercase character in the password
                    if any(char.islower() for char in content):
                        # Check if there is a digit in the password
                        if any(char.isdigit() for char in content):
                            # Check if there is a special char in the password
                            if any(char in "!@#$%^&*" for char in content):
                                return True
        return False