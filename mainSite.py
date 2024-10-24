from flask import Flask, render_template, request

from App.siteFlaskSystem import SiteFlask

import socket

app = Flask(__name__)
main_flask_system = SiteFlask()



#? PAGES ###############################################
##* Home/Launch Server
@app.route('/')
@app.route('/home')
def home():
    return render_template(main_flask_system._home())


##* Search
@app.route('/search', methods=["POST"])
def search():
    return render_template(main_flask_system._search(request.form["searchItem"]))
    #FIXME - Not implemented fully


##* Departures
###? Departures page
@app.route('/departures')
def departure_page():
    departure_items = main_flask_system._departures()

    page = departure_items[0]
    #print(page)
    favorites: list = departure_items[1]

    if favorites == "None":
        #print("DI None")
        return render_template(page, send_departures = main_flask_system._extract_stations())
    
    else:
        #print("DI --")
        return render_template(page, favorites = favorites, send_departures = main_flask_system._extract_stations())

    

###? Departures request
@app.route('/departures/', methods=['POST'])
def departures(station_crs = None):
    departure_data = main_flask_system._get_departures(request.form['station_crs'])
    station_crs = departure_data[2]

    send_service = departure_data[3]

    for each in send_service:
        #print(send_service.wtt_departure)
        #print(each)
        pass

    #print(send_service)

    return render_template(str(departure_data[0]), 
                            station_name = (str(departure_data[1])), 
                            station_crs = station_crs, 
                            send_service = departure_data[3], 
                            date_now = departure_data[4])


###? Departures refresh
@app.route('/departures/<station_crs>')
def departures_refresh(station_crs = None):
    departure_data = main_flask_system._get_departures(station_crs)
    station_crs = departure_data[2]

    send_service = departure_data[3]

    for each in send_service:
        #print(send_service.wtt_departure)
        #print(each)
        pass

    #print(send_service)

    return render_template(str(departure_data[0]), 
                            station_name = (str(departure_data[1])), 
                            station_crs = station_crs, 
                            send_service = send_service, 
                            date_now = departure_data[4])


###? Departures Train Information
@app.route('/departures/info/<train_UID>')
def departures_train_info(train_UID = None):
    service_data = main_flask_system._get_service_info(train_UID)
    #print(service_data)

    return render_template(service_data[0], service = service_data[1])


@app.route('/departures/<station_crs>/')
def add_new_favorite(station_crs = None):
    raise NotImplementedError("Service unavailable")

    main_flask_system._add_to_favorites(station_crs)
    return render_template(main_flask_system._departures(), send_departures = main_flask_system._extract_stations())


###? Information
@app.route('/info/<station_crs>')
def information(station_crs = None):
    pass


##* Planner
@app.route('/planner')
def planner():
    return render_template(main_flask_system._planner())


@app.route('/planner/search')
def planner_search():

    raise NotImplementedError("Planner search is unavailable")
    
    if system._shutdown() == True:
        return render_template('siteClosed.html')
    
    else:
        origin = (str(request.form['origin'])).upper()
        dest = (str(request.form['dest'])).upper()
        reqdate = str(request.form['date'])
        reqtime = str(request.form['time'])
        
        system._search_planner(origin, dest, reqdate, reqtime)

        return render_template('plannerSearch.html')


##* Settings
@app.route('/My-OneTrack/settings')
def settings():
    return render_template(main_flask_system._open_settings())


@app.route('/My-OneTrack/')
def save_settings():
    returned_items = main_flask_system._save_settings()
    return render_template(returned_items[0], username = returned_items[1])


#? Account Handling ####################################
##* Open My:OneTrack
@app.route('/My-OneTrack')
def my_one_track():
    return_item = main_flask_system._my_one_track()

    page = return_item[0]
    try:
        username = str(return_item[1])

        return render_template(page, username = username)
    except:
        return render_template(page)


##* Sign in request
@app.route('/signIn', methods=['POST'])
def sign_in():
    username = request.form['username']
    password = request.form['password']
    
    details = main_flask_system._sign_in(username, password)
    
    page = details[0]
    username = details[1]

    return render_template(page, username = username)


##* Create account page
@app.route('/My-OneTrack/createAccount')
def create_account_page():
    
    return render_template(main_flask_system._create_account())


##* Create account request
@app.route('/My-OneTrack/createAccount/', methods=['POST'])
def create_account():

    returned_items = main_flask_system._create_new_user(
        request.form['firstName'],
        request.form['password1'],
        request.form['password2'],
        request.form['username'],
        request.form['surname'],
        request.form['email']
    )

    page = returned_items[0]
    content = returned_items[1]
    if page == "account.html":
        return render_template(page, username = content)

    else:
        return render_template(page, error = content)


##* Sign out request
@app.route('/signOut')
def sign_out():
    
    return render_template(main_flask_system._sign_out())
    

##* Delete account confirmation
@app.route('/deleteAccount')
def delete_account():
    
    return render_template(main_flask_system._delete_account_1())


##* Delete account confirmed
@app.route('/deleteAccount/')
def delete_account2():
    
    return render_template(main_flask_system._delete_account_2())



#? About pages #########################################
##* About
@app.route('/about')
def about():
    
    return render_template(main_flask_system._about())


##* Contact
@app.route('/about/contact')
def about_contact():
    
    return render_template(main_flask_system._about_contact())


##* Terms of Use
@app.route('/policies/terms-of-use')
def terms_of_use():
    
    return render_template(main_flask_system._terms_of_service())


##* Privacy Policy
@app.route('/policies/privacy-policy')
def privacy_policy():
    
    return render_template(main_flask_system._privacy_policy())



#? ERROR HANDLING ######################################
##* 400
@app.errorhandler(400)
def bad_request(e):
    main_flask_system._report_error(e)

    return render_template('error400.html')


##* 404
@app.errorhandler(404)
def not_found(e):
    #main.report_error(e) #* Doesn't log intentionally

    return render_template('error404.html')


##* 405
@app.errorhandler(405)
def method_not_allowed(e):
    main_flask_system._report_error(e)

    return render_template('error405.html')


##* 500
@app.errorhandler(500)
def internal_server_error(e):
    main_flask_system._report_error(e)

    return render_template('error500.html')


##* 503
@app.errorhandler(503)
def service_unavailable(e):
    main_flask_system._report_error(e)

    return render_template('error503.html')



#? SOCKET ##############################################
if __name__ == "__main__":
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(('8.8.8.8', 1)) 
   local_ip_address = s.getsockname()[0]
   print("-------------")
   print("Local IP:",local_ip_address)
   print("Program run time:", main_flask_system._time_created)
   print("-------------")
   print("OneTrack", main_flask_system._site_version)
   print("-------------")

   app.run(host = "0.0.0.0")
   #app.run()