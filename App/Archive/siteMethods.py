from App.siteAI import AI
from App.siteDatabase import database
from App.siteRTT import RTT, Service, Departures
from App.Archive.siteDarwin import Darwin

from datetime import datetime
#from random import random
import hashlib
#import sys


class SiteInternalSystem():
    def __init__(self):
        self.__artificial_intelligence = AI()
        self._time_created = ("Site created:", self._get_now(3))
        self._shutdown_time = ("Site shutdown: None")
        self.__close_access: bool = False
        self._send_service: list = []
        self.__signed_in: bool = False
        self._send_station: str = ""
        self.__database = database()
        self._send_code: str = ""
        self._username: str = ""
        try:
            self.__nre = Darwin()
            self._nre_departures_failed: bool = False
        except:
            self._report_error("Couldn't connect to NRE Data Service")
            self._nre_departures_failed: bool = True

        try:
            self.__rtt = RTT()
            self._rtt_departures_failed: bool = False
        except:
            self._report_error("Couldn't connect to RTT API Service")
            self._rtt_departures_failed: bool = True
        
        ###########################

        self._all_stations = self.__database._get_all_values_in_order("tblStations", "StationName")
        self._site_version = "V0.1.1 [ALPHA]"
        

    #SECTION - Departures
    def _get_rtt_departures(self, station_name):
        self._reset_departures()
        
        if self._rtt_departures_failed != True:
            date_now = self._get_now(1)
            return_date = date_now
            if 1 != 1:
                self._send_station = station_name.title()

                try:
                    self._send_code = self.__database._get_values("SID", "tblStations", "StationName", (self._send_station.upper()))
                    self._send_service: Departures = self.__rtt._get_advanced_board(self._send_code)

                    if self._send_service == "No services found":
                        return 'departuresNotFound.html', self._send_station.title(), self._send_code, self._send_service, return_date
                    

                except:
                    self._send_code = station_name
                    self._send_station = self.__database._get_values("StationName", "tblStations", "SID", (self._send_code.upper()))
                    self._send_service: Departures = self.__rtt._get_advanced_board(self._send_code)

                    if self._send_service == "No services found":
                        return 'departuresNotFound.html', self._send_station.title(), self._send_code, self._send_service, return_date
                    

                

                return 'departuresAdv.html', self._send_station.title(), self._send_code, self._send_service, return_date

            else:
                self._send_station = station_name.title()

                try:
                    self._send_code = self.__database._get_values("SID", "tblStations", "StationName", (self._send_station.upper()))
                    self._send_service: Departures = self.__rtt._get_station_board(self._send_code)

                    if self._send_service == "No services found":
                        return 'departuresNotFound.html', self._send_station.title(), self._send_code, self._send_service, return_date
                    

                except:
                    self._send_code = station_name
                    self._send_station = self.__database._get_values("StationName", "tblStations", "SID", (self._send_code.upper()))
                    self._send_service: Departures = self.__rtt._get_station_board(self._send_code)

                    if self._send_service == "No services found":
                        return 'departuresNotFound.html', self._send_station.title(), self._send_code, self._send_service, return_date
                    

                #__wtt_departure, __terminus, __platform, __exp_departure, __service_uid

                return 'departureResults.html', self._send_station.title(), self._send_code, self._send_service, return_date
            
        else:
            self._report_error("Failed to connect to RTT API Service")
            return "departuresFailed.html"


    def _get_nre_departures(self, station_name): 
        self._reset_departures()
        #if self.get_operator_status == "1":
        if self._nre_departures_failed != True:
            if 1 != 1:
                self._send_station = station_name.upper()
                self._send_code = self.__database._get_values("SID", "tblStations", "StationName", self._send_station)
                self._send_service = self.__nre.get_advanced_dep_board(self._send_code)
                date_now = self._get_now(1)
                return_date = date_now
                self._send_station = self._send_station.title()

                return 'departuresAdv.html', self._send_station, self._send_code, self._send_service, return_date

            else:
                self._send_station = station_name.upper()
                self._send_code = self.__database._get_values("SID", "tblStations", "StationName", self._send_station)
                self._send_service = self.__nre.get_dep_board(self._send_code)
                date_now = self._get_now(1)
                return_date = date_now
                self._send_station = self._send_station.title()

                #print(self.send_service)
                return 'departureResults.html', self._send_station, self._send_code, self._send_service, return_date
        
        else:
            self._report_error("Failed to connect to NRE Data Service")
            return "departuresFailed.html"


    def _get_stations_list(self):
        return self._all_stations


    def _get_user_favorites(self):
        #print(self._username)
        if self._username != "":
            return_values: list = []
            for i in range (1, 7):
                favorite = self.__database._get_values(("Favorite" + str(i)), "tblUserFavorites", "Username", self._username)

                if str(favorite) != "None":
                    favorite_crs = self.__database._get_values("SID", "tblStations", "StationName", (favorite.upper()))
                    return_values.append([favorite.title(), favorite_crs])
                else:
                    break
                #print(return_values)

            #print("RRRRRRRR ", return_values)
            return return_values

        else:
            return "None"


    def _reset_departures(self):
        self._send_station = ""
        self._send_service = []
        self._send_code = ""


    def _get_rtt_service_info(self, service_uid) -> list[Service]:
        return self.__rtt._get_service_info(service_uid)


    #SECTION Planner
    def _search_planner(self, origin, destination, departure_date, departure_time):
        date_now = self._get_now(2)

        self.__database._insert_values("tblTicketQueries", "Origin, Destination, DepDate, DepTime, RequestDate, RequestTime", 
                                    [origin, destination, departure_date, departure_time, date_now[0], date_now[1]])
    

    #SECTION Search
    def _search_for_item(self, search_request):
        pages: list = self._get_pages_list

        if search_request in pages:
            return search_request, "was found on the search results page."
        
        else:
            return search_request, "was not found. Check your spelling and try again."
    
    
    def _get_pages_list(self):
        return ['About', 'Contact', 'Create Account', 'Departures', 'Home', 'myOneTrack', 'Planner', 'Privacy Policy', 'Terms of Service']

    #SECTION Account handling 
    #!SECTION ERROR WITH ACCOUNT
    def _sign_in(self, username, password):
        password_to_check = self.__database._get_values("Password", "tblUsers", "Username", username)

        password = self.__hash_item(password)

        if password_to_check == password:
            self.__signed_in = True

            self._username: str = str(username)
            #print(self.username)
            return self._username

        else:
            self.__signed_in = False
            return None


    def _create_account(self, first_name: str, surname: str, email: str, username: str, password1: str, password2: str) ->  str | bool:
        continue_search: bool = True
        username_fail: bool = False
        password_fail: bool = False
        email_fail: bool = False

        first_name: str = self.__hash_item(first_name)
        surname: str = self.__hash_item(surname)
        email: str = self.__hash_item(email)

        password_fail = self.__validate_password(password1)

        if password1 == password2 and password_fail == False:
            search_for_username = self.__database._get_values("UserID" , "tblUsers", "Username", username)
            #print(search_for_username)

            if str(search_for_username) != "None":
                username_fail = True
                continue_search = False

            search_for_email = self.__database._get_values("UserID" , "tblUsers", "Email", email)
            #print(search_for_email)
            
            if str(search_for_email) != "None":
                email_fail = True
                continue_search = False
            
            #HASH the password here
            password = self.__hash_item(password1)

            if continue_search == True:
                #print(first_name, surname, username, email, password3)
                try:
                    self.__database._insert_values("tblUsers", "FirstName, Surname, Username, Email, Password", [first_name, surname, username, email, password])
                    user_id = self.__database._get_values("UserID" , "tblUsers", "Email", email)
                    #print(user_id)
                    self.__database._insert_values("tblUserSettings", "UserID, OperatorEnabled, SystemMode", [user_id, "0", "0"])
                    self.__database._insert_values("tblUserFavorites", "UserID, Favorite1, Favorite2, Favorite3, Favorite4, Favorite5, Favorite6", [user_id, "None", "None", "None", "None", "None", "None"])
                    #print("User settings updated successfully.")

                    #print("Bonk")

                    self.__signed_in = True
                    self._username = username

                    return True, self._username
                except:
                    #print("Bonk it crashed")
                    self._report_error("***Database crash detected.")
                    return False, "An unexpected error occurred. Try again."

            else:
                if email_fail == True and username_fail == True:
                    return False, "The username and email you entered appear to be taken. Try a different one."
                
                elif email_fail == True and username_fail == False:
                    return False, "The email you entered appears to be taken. Try a different one."

                elif email_fail == False and username_fail == True:
                    return False, "The username you entered appears to be taken. Try a different one."

                else:
                    return False, "An unexpected error occurred. Try again."

        elif password_fail == True:
            return False, "The password you entered doesn't meet the requirements. Try again."

        else:
            #print("Bonk it didn't work")
            return False, "The passwords you entered don't match. Try again."


    def _update_settings(self):
        raise NotImplementedError("Code not added yet.")
    
        self.__database._update_values("tblUserSettings")
    
        #NOTE Needs to allow user to update settings in the database 

    #FIXME Not implemented
    def _get_operator_status(self):
        get_status = self.__database._get_values("OperatorStatus", "tblUserSettings", "username", self._username)

        return get_status


    def _sign_out(self):
        self.__signed_in = False
        self._username = ""


    def _check_sign_in(self):
        if self.__signed_in == True:
            return self._username

        else:
            return False


    #FIXME Not implemented
    def _update_account(self):
        raise NotImplementedError("Code not added yet.")
        #NOTE See update_settings
        self.__database._update_values()


    def _delete_account(self):
        #print(username)
        username: str = self._username
        if username != "":
            try:
                user_id = self.__database._get_values("UserID", "tblUsers", "Username", username)
                self.__database._delete_values("tblUsers", "Username", username)
                self.__database._delete_values("tblUserSettings", "UserID", user_id)

                deleted = True
                if deleted:
                    self.__signed_in = False
                    self._username: str = ""
                    return True
            
            except:
                self.__signed_in = True
                self._username = username
                return False

        else:
            self.__signed_in = True
            self._username = username
            return False


    #NOTE Reported account errors:
    #       Account not staying signed in
    #       System not able to delete account
    #       Account not being able to update settings

    #SECTION Shutdown server
    def _shutdown(self):
        if self.__close_access == True:
            self._shutdown_time = ("Site shutdown:", self._get_now(3))
            self.__close_access = True
            self._send_station = ""
            self._send_service = []
            self.__signed_in = False
            self._send_code = ""
            self._username = ""

            return self.__close_access
        else:
            return self.__close_access


    #SECTION Report error 
    def _report_error(self, errorInput):
        try:
            with open(".home/Admin/crashLogs.txt", "a") as file:
                error = errorInput
                #print(str(error))
                file.write("\n\n" + str(error) + "\n" + str(self._get_now(3)))
        except:
            pass


    #SECTION Get the current time
    def _get_now(self, type):
        now = datetime.now()
        if type == 1:
            realdate = now.strftime("on %d/%m/%Y at %H:%M")
            
            return realdate
            
        elif type == 2:
            realdate = now.strftime("%d-%m-%Y")
            realtime = now.strftime("%H:%M:%S")

            return realdate, realtime
        
        elif type == 3:
            realdate = now.strftime("on %d/%m/%Y at %H:%M:%S")
            return realdate

        elif type == 4:
            realdate = now.strftime("%d/%m/%Y at %H:%M:%S")
            return realdate

        else:
            return None


    #FIXME Hashing -- Not implemented
    def __hash_item(self, content):           
        #hash_key = "5gz"

        # Adding salt at the last of the password
        new_item = content #+ hash_key
        hashed_item = hashlib.md5(new_item.encode())

        #print(hashed_item.hexdigest())

        return hashed_item.hexdigest()


    def __validate_password(self, content: str) -> bool:
        # Password validation rules
        # 1. Minimum length of 8 characters
        # 2. At least one uppercase letter
        # 3. At least one lowercase letter
        # 4. At least one digit
        # 5. At least one special character (!@#$%^&*)
        # 6. No spaces

        check_content = "".join(content.split())
        print(check_content)

        if check_content == content:
            if len(content) >= 8:
                if any(char.isupper() for char in content):
                    if any(char.islower() for char in content):
                        if any(char.isdigit() for char in content):
                            if any(char in "!@#$%^&*" for char in content):

                                return False
                            else:
                                return True            
                        else:
                            return True                        
                    else:
                        return True                    
                else:
                    return True                
            else:
                return True            
        else:
            return True

    #SECTION Print all self.variables -- used only for debugging
    def __print_all(self):
        # This function prints all global variables at a given time
        print("-------------")
        print("self.time_created:", self._time_created)
        print("-------------")
        print("self.shutdown_time:", self._shutdown_time)
        print("self.close_access:", self.__close_access)
        print("-------------")
        print("self.signed_in:", self.__signed_in)
        print("self.username:", self._username)
        print("-------------")
        print("self.send_station:", self._send_station)
        print("self.send_service:", self._send_service)
        print("self.send_code:", self._send_code)
        print("-------------")
        print("self.variables generated", (self._get_now(3)))
        print("-------------")