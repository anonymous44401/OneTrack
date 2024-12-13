from App.site_flask_system import SiteFlask
from flask import Flask, render_template, request

import socket

app = Flask(__name__)
main_flask_system = SiteFlask()



@app.route('/')
@app.route('/home')
def home():
    return render_template(main_flask_system._home())


@app.route('/search', methods=["POST"])
def search():
    return render_template(main_flask_system._search(request.form["searchItem"]))
    # Just here for show


@app.route('/departures')
def departure_page():
    departure_items = main_flask_system._departures()

    page = departure_items[0]
    favorites: list = departure_items[1]

    if favorites == "None":
        return render_template(page, send_departures = main_flask_system._get_stations())
    
    else:
        return render_template(page, favorites = favorites, send_departures = main_flask_system._get_stations())

    
@app.route('/departures/', methods=['POST'])
def departures(station_crs = None):
    departure_data = main_flask_system._get_departures(request.form['station_crs'])
    station_crs = departure_data[2]

    send_service = departure_data[3]

    #print(send_service)

    return render_template(str(departure_data[0]), 
                            station_name = (str(departure_data[1])), 
                            station_crs = station_crs, 
                            send_service = send_service, 
                            date_now = departure_data[4])


@app.route('/departures/<station_crs>')
def departures_refresh(station_crs = None):
    departure_data = main_flask_system._get_departures(station_crs)
    station_crs = departure_data[2]

    send_service = departure_data[3]

    #print(send_service)

    return render_template(str(departure_data[0]), 
                            station_name = (str(departure_data[1])), 
                            station_crs = station_crs, 
                            send_service = send_service, 
                            date_now = departure_data[4])


@app.route('/departures/info/<train_UID>')
def departures_train_info(train_UID = None):
    service_data = main_flask_system._get_service_info(train_UID)
    #print(service_data)

    return render_template(service_data[0], service = service_data[1], train_UID = train_UID)


@app.route('/departures/<station_crs>/')
def add_new_favorite(station_crs = None):
    raise NotImplementedError("Service unavailable")

    main_flask_system._add_to_favorites(station_crs)
    return render_template(main_flask_system._departures(), send_departures = main_flask_system._get_stations())


@app.route('/share/<service_uid>')
def share(service_uid = None):
    
    return render_template("share.html", service_uid = service_uid)


@app.route('/info/<station_crs>')
def station_information(station_crs = None):
    information = main_flask_system._station_info(station_crs)

    return render_template(information[0], station_crs = station_crs, station_name = information[1])


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


@app.route('/My-OneTrack/settings')
def settings():
    return render_template(main_flask_system._open_settings())


@app.route('/My-OneTrack/')
def save_settings():
    returned_items = main_flask_system._save_settings()
    return render_template(returned_items[0], username = returned_items[1])



@app.route('/My-OneTrack')
def my_one_track():

    return render_template(main_flask_system._my_one_track())


@app.route('/signIn', methods=['POST'])
def sign_in():

    return render_template(main_flask_system._sign_in(request.form['username'], request.form['password']))


@app.route('/My-OneTrack/createAccount')
def create_account_page():
    
    return render_template(main_flask_system._create_account())


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

    if returned_items[0] == "account.html":
        return render_template(returned_items[0], username = returned_items[1])

    else:
        return render_template(returned_items[0], error = returned_items[1])


@app.route('/signOut')
def sign_out():
    
    return render_template(main_flask_system._sign_out())
    

@app.route('/deleteAccount')
def delete_account():
    
    return render_template(main_flask_system._delete_account_1())


@app.route('/deleteAccount/')
def delete_account2():
    
    return render_template(main_flask_system._delete_account_2())


@app.route('/My-OneTrack/friends')
def friends_page():
    content = main_flask_system._friends()

    return render_template(content[0], friendsList = content[1], friendRequests = content[2], requestsSent = content[3])


@app.route('/My-OneTrack/friends/')
def friends_page_send_request():
    content = main_flask_system._friends()
    
    return render_template(content[0], friendsList = content[1], friendRequests = content[2], requestsSent = content[3])



@app.route('/about')
def about():
    
    return render_template(main_flask_system._about())


@app.route('/about/contact')
def about_contact():
    
    return render_template(main_flask_system._about_contact())


@app.route('/policies/terms-of-use')
def terms_of_use():
    
    return render_template(main_flask_system._terms_of_service())


@app.route('/policies/privacy-policy')
def privacy_policy():
    
    return render_template(main_flask_system._privacy_policy())



@app.errorhandler(400)
def bad_request(e):
    main_flask_system._report_error(e)

    return render_template('error.html', error = 400, errorText = e)


@app.errorhandler(404)
def not_found(e):
    #main.report_error(e) #* Doesn't log intentionally

    return render_template('error.html', error = 404, errorText = e)


@app.errorhandler(405)
def method_not_allowed(e):
    main_flask_system._report_error(e)

    return render_template('error.html', error = 405, errorText = e)


@app.errorhandler(500)
def internal_server_error(e):
    main_flask_system._report_error(e)

    return render_template('error.html', error = 500, errorText = e)


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