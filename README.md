# OneTrack:Alpha

![License](https://img.shields.io/github/license/anonymous44401/OneTrack)

## Setup

1. Create a folder called `keys` inside of `app`. 
2. Create a file called `hash.txt` for your database hash.
3. Create a file called `rtt_user.txt` for your RTT API username.
4. Create a file called `rtt_token.txt` for your RTT API password.
5. Run `create_db.py` (in the `database` folder). 
6. Run `main_site.py`.

## Contents

### main_site.py 
The place where everything comes together.

### site_database.py
The database management class.

### [realtime-trains-py 2025.2.2](https://github.com/realtime-trains-lang/realtime-trains-py/tree/v2025.2.2)
A custom-made Python API Wrapper for the RTT API.

### site_flask_system.py
The class for managing the internal actions of the flask system.

### site_internal_system.py
The class for handling all the backend boring stuff.

### siteScript.js
The file for making the site do cool stuff.

### siteStyle.css
The file that turns ugly boring html into a beautiful formatted heaven.

### create_hash.py
The file for creating a hash for the site. 

> This file isn't used in deployment of the site. 