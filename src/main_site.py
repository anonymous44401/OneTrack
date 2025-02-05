# Import modules from flask
from flask import Flask, render_template, request

# Import class from site_flask_system.py
from App.site_flask_system import SiteFlask

# Name app
app = Flask(__name__)
# Name SiteFlask class
main_flask_system = SiteFlask()



# Home page
@app.route('/')
@app.route('/home')
def home():
    # Return the home page
    return render_template(main_flask_system._home(),
                           send_departures = main_flask_system._get_stations())


# Search
@app.route('/search', methods=["POST"])
def search():
    # Just here for show - not functional
    # Return the search results page
    return render_template(main_flask_system._search(request.form["searchItem"]))  


# Departures page
@app.route('/departures')
def departure_page():
    # Get departure items
    departure_items = main_flask_system._departures()

    favorites = departure_items[1]

    # Select page based on favorites
    if favorites == "None":
        return render_template(departure_items[0], # Page
                               send_departures = main_flask_system._get_stations()) # Dict of stations and CRS codes 
    
    else:
        return render_template(departure_items[0], # Page
                               favorites = favorites, # List of favorites
                               send_departures = main_flask_system._get_stations()) # Dict of stations and CRS codes

    
# Departure results (POST)
@app.route('/departures/<station_crs>', methods=['POST', 'GET'])
def departures(station_crs=None):
    if request.method == 'POST':
        departure_data = main_flask_system._get_departures(request.form['station_crs'])
    
    elif request.method == 'GET':
        departure_data = main_flask_system._get_departures(station_crs)
    
    # Return the departures page
    return render_template(str(departure_data[0]), # Page
                            station_name = str(departure_data[1]), # Station name
                            station_crs = departure_data[2], # Station CRS
                            send_service = departure_data[3], # List of services
                            date_now = departure_data[4]) # Date and time of last request


# Service information
@app.route('/departures/info/<train_UID>')
def departures_train_info(train_UID=None):
    # Get service data
    service_data = main_flask_system._get_service_info(train_UID)

    # Return the service info page
    return render_template(service_data[0], service = service_data[1], train_UID = train_UID, stations = service_data[2])


# Add station as favorite
@app.route('/departures/<station_crs>/')
def add_new_favorite(station_crs=None):
    # Add station to favorites
    main_flask_system._add_new_favorite(station_crs)

    # Get departure items
    departure_data = main_flask_system._get_departures(station_crs)
    
    # Return the departures page
    return render_template(
        str(departure_data[0]), # Page
        station_name = str(departure_data[1]), # Station name
        station_crs = departure_data[2], # Station CRS
        send_service = departure_data[3], # List of services
        date_now = departure_data[4] # Date and time of last request
    )

# Share service
@app.route('/share/<service_uid>')
def share(service_uid=None):
    # Return the share page
    return render_template("share.html", service_uid = service_uid)


# Station information
@app.route('/info/<station_crs>')
def station_information(station_crs=None):
    # Not functional
    raise NotImplementedError("Service unavailable")

    information = main_flask_system._station_info(station_crs)

    return render_template(information[0], 
                           station_crs = station_crs, 
                           station_name = information[1])


# Planner page
@app.route('/planner')
def planner():
    # Return the planner page
    return render_template(main_flask_system._planner())


#  Planner search
@app.route('/planner/search')
def planner_search():
    # Not functional
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


# Settings
@app.route('/My-OneTrack/settings')
def settings():
    # Return the settings page
    return render_template(main_flask_system._open_settings())


# My:OneTrack - save settings
@app.route('/My-OneTrack/')
def save_settings():
    # Get items to return
    return_items = main_flask_system._save_settings()
    # Return the settings page and username
    return render_template(return_items[0], username = return_items[1])


# My:OneTrack - main page
@app.route('/My-OneTrack')
def my_one_track():
    # Return the My:OneTrack page - or sign in page if not signed in
    return render_template(main_flask_system._my_one_track())


# My:OneTrack - sign in
@app.route('/signIn', methods=['POST'])
def sign_in():
    # Return the sign in page
    return render_template(main_flask_system._sign_in(request.form['username'], request.form['password']))


# My:OneTrack - create account page
@app.route('/My-OneTrack/createAccount')
def create_account_page():
    # Return the create account page
    return render_template(main_flask_system._create_account())


# My:OneTrack - create account request
@app.route('/My-OneTrack/createAccount/', methods=['POST'])
def create_account():
    # Create a new user with the credentials 
    returned_items = main_flask_system._create_new_user(
        request.form['firstName'],
        request.form['password1'],
        request.form['password2'],
        request.form['username'],
        request.form['surname'],
        request.form['email']
    )
    
    # Return the appropriate page
    if returned_items[0] == "account.html":
        return render_template(returned_items[0], username = returned_items[1])

    else:
        return render_template(returned_items[0], error = returned_items[1])


# My:OneTrack - sign out
@app.route('/signOut')
def sign_out():
    # Return the sign out completed page
    return render_template(main_flask_system._sign_out())
    

# My:OneTrack - delete account (confirmation)
@app.route('/deleteAccount')
def delete_account():
    # Return the confirm delete account page
    return render_template(main_flask_system._delete_account_1())


# My:OneTrack - delete account (confirmed)
@app.route('/deleteAccount/')
def delete_account2():
    # Return the account deleted page
    return render_template(main_flask_system._delete_account_2())


# OneTrack - about
@app.route('/about')
def about():
    # Return the about page
    return render_template(main_flask_system._about())


# OneTrack - contact
@app.route('/about/contact')
def about_contact():
    # Return the contact page
    return render_template(main_flask_system._about_contact())


# OneTrack - terms
@app.route('/policies/terms-of-use')
def terms_of_use():
    # Return the privacy terms of use
    return render_template(main_flask_system._terms_of_service())


# OneTrack - privacy
@app.route('/policies/privacy-policy')
def privacy_policy():
    # Return the privacy policy page
    return render_template(main_flask_system._privacy_policy())



# Error handlers -  they're all the same, so I won't comment each one
@app.errorhandler(400)
def bad_request(e):
    # Report the error 
    main_flask_system._report_error(e)

    return render_template('error.html', error=400, error_text=e)

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error=404, error_text=e)

@app.errorhandler(405)
def method_not_allowed(e):
    main_flask_system._report_error(e)

    return render_template('error.html', error=405, error_text=e)

@app.errorhandler(500)
def internal_server_error(e):
    main_flask_system._report_error(e)

    return render_template('error.html', error=500, error_text=e)

# Run the program
if __name__ == "__main__":
    print("-------------")
    print("Program run started", (main_flask_system._time_created[1])) # Time started
    print("-------------")
    print("OneTrack", main_flask_system._site_version) # Version 
    print("-------------")
    
    # Run the app
    app.run(host = "0.0.0.0")