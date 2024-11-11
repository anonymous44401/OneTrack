from App.siteInternalSystem import SiteInternalSystem

class SiteFlask():
    #SECTION - Init
    def __init__(self):
        self.__internal_system = SiteInternalSystem()

        self._site_version = self.__internal_system._site_version
        self._time_created = self.__internal_system._time_created


    #SECTION - Search
    def _search(self, search_item):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            self.__internal_system._search_for_item(search_item)

            return 'searchResults.html'


    #SECTION - Main pages
    def _home(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            #return 'home.html'
            return 'home.html'


    def _planner(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'planner.html'


    #SECTION - Departures
    def _extract_stations(self):
        return self.__internal_system._get_stations_list()


    def _departures(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html', None
        
        else:
            self.__internal_system._reset_departures()
            if self.__internal_system._rtt_departures_failed != True:
                user_favorites: list = self.__internal_system._get_user_favorites()
                #print(user_favorites)
                #user_favorites = "None"

                if user_favorites == "None":
                    #print("")
                    return 'departuresV1.html', "None"
            
                else:
                    return_user_favorites: list = []

                    return_user_favorites.append(user_favorites)
                    #for i in range(0, len(return_user_favorites)):
                        #print(return_user_favorites[i].title())
                    return 'departuresV2.html', user_favorites
            
            else:
                return 'departuresFailed.html'


    def _get_departures(self,station_crs):
        return self.__internal_system._get_rtt_departures(station_crs)


    def _get_service_info(self, service_uid):
        return "serviceInfo.html", self.__internal_system._get_rtt_service_info(service_uid)


    #SECTION - Policies and info pages
    def _privacy_policy(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'privPol.html'

    
    def _terms_of_service(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'terms.html'


    def _about(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'about.html'
    

    def _about_contact(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'contact.html'


    #SECTION - Account handling
    def _my_one_track(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            sign_in_check = self.__internal_system._check_sign_in()
            #print(sign_in_check)
            if sign_in_check != False:
                return 'account.html', sign_in_check

            else:
                return 'signIn.html', None
    

    def _create_account(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'createAccount.html'
    

    def _sign_out(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            self.__internal_system._sign_out() 
            return 'signedOut.html'


    def _sign_in(self, username, __password):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html', None
        
        else:
            sign_in_request = self.__internal_system._sign_in(username, __password)
            username = sign_in_request  

            if sign_in_request != None:
                return 'account.html', username
            
            else:
                return 'signInFail.html', None


    def _delete_account_1(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            return 'deleteAccount.html'


    def _delete_account_2(self):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            if self.__internal_system._delete_account() == True:
                
                return 'accountDeleted.html'
            
            else:
                self.__internal_system._report_error("Failed to delete user account. (" +  + ")")
                return 'account.html'


    def _create_new_user(self, first_name, __password1, __password2, username, surname, email):
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            account_created = self.__internal_system._create_account(first_name, surname, email, username, __password1, __password2)
            account_created_status = account_created[0]
            username = account_created[1]    
                
            if account_created_status == True:
                return 'account.html', username

            else:
                error = username
                return 'createFailed.html', error 


    def _open_settings(self):
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
        if self.__internal_system._shutdown() == True:
            return 'siteClosed.html'
        
        else:
            sign_in_check = self.__internal_system._check_sign_in()
            if sign_in_check != False:
                # TODO implement
                return 'settings.html', sign_in_check
            
            else:
                return 'signIn.html', None
            
            
    #SECTION - Error reporting
    def _report_error(self, errorInput):
        try:
            with open(".home/Admin/crashLogs.txt", "a") as file:
                error = errorInput
                #print(str(error))
                file.write("\n\n" + str(error) + "\n" + str(self.__internal_system._get_now(3)))
        except:
            pass