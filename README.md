# OneTrack:Alpha

![License](https://img.shields.io/github/license/anonymous44401/OneTrack)

## Setup

1. Install the requirements by running `py -m pip install -r .\requirements.txt`
2. If you don't have a username or password for the RTT API, head over to the realtime-trains-py setup documentation by [clicking here](https://github.com/realtime-trains-lang/realtime-trains-py/wiki/Setup#i-dont-have-a-username-or-password).
3. Run `create_site.py` (in the `src` folder) and follow the instructions. 
4. Run `main_site.py`.

## Contents

### main_site.py 
The place where everything comes together.

### site_database.py
The database management class.

### [realtime-trains-py 2025.3.0](https://github.com/realtime-trains-lang/realtime-trains-py/tree/v2025.3.0)
A custom-made Python API Wrapper for the RTT API.

### encryption.py
The file for handling encryption.

### site_flask_system.py
The class for managing the internal actions of the flask system.

### site_internal_system.py
The class for handling all the backend boring stuff.

### siteScript.js
The file for making the site do cool stuff.

### siteStyle.css
The file that turns ugly boring html into a beautiful formatted heaven.

### create_db.py
The file that handles creating the database.

### update_db_contents.py
The file that updates the contents of the database with the required station data.

### create_site.py
The file that creates the site.