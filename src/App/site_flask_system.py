from app.site_internal_system import SiteInternalSystem

# Class for the site flask system
class SiteFlask():
    # Initialise
    def __init__(self):
        self.__internal_system = SiteInternalSystem()

        self._site_version = self.__internal_system._site_version
        self._time_created = self.__internal_system._time_created

    # Get the search page
    def _search_page(self, search_item) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            # Search for items
            self.__internal_system._search_for_item(search_item)

            return 'searchResults.html'

    # Get the home page
    def _home_page(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'home.html'

    # Return the planner page
    def _planner_page(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'planner.html'

    # Return the dictionary of all stations
    def _get_stations(self) -> dict:
        # Return the dict of stations
        return self.__internal_system._get_stations_dict()

    # Get the departures page
    def _departures_page(self) -> tuple:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html', None, None
        
        else:
            # Reset departures
            self.__internal_system._reset_departures()

            # Check if the departure service failed and run appropriate actions
            if self.__internal_system._rtt_departures_failed != True:
                user_favorites = self.__internal_system._get_user_favorites()

                if user_favorites == None:
                    return 'departuresV1.html', None, None
            
                else:
                    return 'departuresV2.html', user_favorites, self.__internal_system._all_stations_reversed
            
            else:
                return 'departuresFailed.html', None, None

    # Get the departures
    def _get_departures(self,station_crs) -> tuple:
        return self.__internal_system._get_departures(station_crs)

    # Get the service information
    def _get_service_info(self, service_uid) -> tuple:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown():
            return 'siteClosed.html', None, None
        
        else:
            # Return the service info page, the service information and the dictionary of all stations
            return "serviceInfo.html", self.__internal_system._get_service_info(service_uid), self.__internal_system._all_stations, self.__internal_system._get_now(1)

    # Get the station info
    def _station_info(self, station_crs) -> tuple:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return "siteClosed.html", None

        else:
            # Try to get the station name from the database
            try:
                station_name = self.__internal_system._get_station_name(station_crs).title()

            except:
                station_name = None

            return "stationInfo.html", station_name
        
    # Get the privacy policy page
    def _privacy_policy_page(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'privPol.html'
    
    # Get the ToS page
    def _terms_of_service_page(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'terms.html'

    # Get the about page
    def _about_page(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'about.html'
    
    # Get the about (contact) page
    def _about_contact_page(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'contact.html'

    # Get the My:OneTrack page
    def _my_one_track_page(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            sign_in_check = self.__internal_system._check_sign_in()
            if sign_in_check != False:
                return 'account.html'

            else:
                return 'signIn.html'
    
    # Get the create account page
    def _create_account_page(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'createAccount.html'
    
    # Sign out the user
    def _sign_out_request(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            self.__internal_system._sign_out() 
            return 'signedOut.html'

    # Sign the user in
    def _sign_in_request(self, username, password) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html', None
        
        else:
            sign_in_request = self.__internal_system._sign_in(username, password) 

            if sign_in_request != None:
                return 'account.html'
            
            else:
                return 'signInFail.html', None

    # Add a new user favorite
    def _add_new_favorite(self, station) -> None:
        # Check if the user is signed in
        if self.__internal_system._check_sign_in() != False:
            self.__internal_system._add_favorite(station)

    # Delete account confirmation        
    def _delete_account_conf(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'deleteAccount.html'

    # Delete account request
    def _delete_account_request(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            # Delete the user account
            if self.__internal_system._delete_account() == True:
                
                return 'accountDeleted.html'
            
            else:
                # If it fails, report an error
                self.__internal_system._report_error("Failed to delete a user account.")
                return 'account.html'

    # Create a new user
    def _create_new_user(self, first_name, password1, password2, username, surname, email) -> tuple:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html', None
        
        else:
            account_created = self.__internal_system._create_account(first_name, surname, email, username, password1, password2)
            account_created_status = account_created[0]
            username = account_created[1]    
                
            if account_created_status == True:
                return 'account.html', username

            else:
                error = username
                return 'createFailed.html', error 

    # Open the settings page
    def _open_settings_page(self) -> str:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            sign_in_check = self.__internal_system._check_sign_in()
            if sign_in_check != False:
                return 'settings.html'
            
            else:
                return 'signIn.html'

    # Save the user settings
    def _save_settings(self) -> tuple:
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html', None
        
        else:
            sign_in_check = self.__internal_system._check_sign_in()
            if sign_in_check != False:
                # TODO implement
                return 'settings.html', sign_in_check
            
            else:
                return 'signIn.html', None
            
    # Report an error
    def _report_error(self, error) -> None:
        self.__internal_system._report_error(error=error)