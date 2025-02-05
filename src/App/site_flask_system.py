from App.site_internal_system import SiteInternalSystem

##### THIS FILE IS NOT FULLY COMMENTED YET #####

class SiteFlask():
    def __init__(self):
        self.__internal_system = SiteInternalSystem()

        self._site_version = self.__internal_system._site_version
        self._time_created = self.__internal_system._time_created

    def _search(self, search_item):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            # Search for items
            self.__internal_system._search_for_item(search_item)

            return 'searchResults.html'

    def _home(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'home.html'

    def _planner(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'planner.html'

    def _get_stations(self):
        # Return the dict of stations
        return self.__internal_system._get_stations_dict()

    def _departures(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html', None
        
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

    def _get_departures(self,station_crs):
        return self.__internal_system._get_departures(station_crs)

    # TODO: this
    def _get_service_info(self, service_uid):
        return "serviceInfo.html", self.__internal_system._get_service_info(service_uid), self.__internal_system._all_stations

    def _station_info(self, station_crs):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return "siteClosed.html", None

        else:
            try:
                station_name = (self.__internal_system._get_station_name(station_crs)).title()
                #print(station_name)

            except:
                station_name = None

            return "stationInfo.html", station_name
        
    def _privacy_policy(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'privPol.html'
    
    def _terms_of_service(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'terms.html'

    def _about(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'about.html'
    
    def _about_contact(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'contact.html'

    def _my_one_track(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            sign_in_check = self.__internal_system._check_sign_in()
            #print(sign_in_check)
            if sign_in_check != False:
                return 'account.html'

            else:
                return 'signIn.html'
    
    def _create_account(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'createAccount.html'
    
    def _sign_out(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            self.__internal_system._sign_out() 
            return 'signedOut.html'

    def _sign_in(self, username, password):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html', None
        
        else:
            sign_in_request = self.__internal_system._sign_in(username, password) 

            if sign_in_request != None:
                return 'account.html'
            
            else:
                return 'signInFail.html', None

    def _add_new_favorite(self, station):
        # Check if the user is signed in
        if self.__internal_system._check_sign_in() != False:
            self.__internal_system._add_favorite(station)
                

    def _delete_account_1(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'deleteAccount.html'

    def _delete_account_2(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            if self.__internal_system._delete_account() == True:
                
                return 'accountDeleted.html'
            
            else:
                self.__internal_system._report_error("Failed to delete user account. (" +  + ")")
                return 'account.html'

    def _create_new_user(self, first_name, password1, password2, username, surname, email):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            account_created = self.__internal_system._create_account(first_name, surname, email, username, password1, password2)
            account_created_status = account_created[0]
            username = account_created[1]    
                
            if account_created_status == True:
                return 'account.html', username

            else:
                error = username
                return 'createFailed.html', error 

    def _open_settings(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            sign_in_check = self.__internal_system._check_sign_in()
            #print(sign_in_check)
            if sign_in_check != False:
                return 'settings.html'
            
            else:
                return 'signIn.html'
            
    def _save_settings(self):
        # Check if the system is shutdown and run appropriate actions
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            sign_in_check = self.__internal_system._check_sign_in()
            if sign_in_check != False:
                # TODO implement
                return 'settings.html', sign_in_check
            
            else:
                return 'signIn.html', None
            
    def _report_error(self, error):
        self.__internal_system._report_error(error=error)