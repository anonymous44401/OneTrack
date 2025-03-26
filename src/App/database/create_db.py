import sqlite3

from app.database.update_db_contents import UpdateDBContents

def create_database():
    print("Creating database...")
    # Get the database ready
    database = 'src/app/database/OneTrack_database.db'
    # Connect
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    # Create the tables
    create_tblStations = """
    CREATE TABLE "tblStations" (
        "StationName" TEXT NOT NULL UNIQUE, 
        "CRS"TEXT NOT NULL UNIQUE, 
        PRIMARY KEY("StationName")
    );
    """

    create_tblUsers = """
    CREATE TABLE "tblUsers" (
        "UserID"	INTEGER NOT NULL UNIQUE,
        "FirstName"	TEXT NOT NULL,
        "Surname"	TEXT NOT NULL,
        "Username"	TEXT NOT NULL UNIQUE,
        "Email"	TEXT NOT NULL UNIQUE,
        "Password"	TEXT NOT NULL,
        PRIMARY KEY("UserID" AUTOINCREMENT)
    );
    """

    create_tblUserFavorites = """
    CREATE TABLE "tblUserFavorites" (
        "UserID"	TEXT NOT NULL,
        "Favorite"	TEXT NOT NULL
    );
    """

    # Excuse the commands
    try:
        print("Creating table 'tblStations'")
        cursor.execute(create_tblStations)
    except:
        print("Unable to create 'tblStations'. It might already exists")
    
    try:
        print("Creating table 'tblUsers'")
        cursor.execute(create_tblUsers)
    except:
        print("Unable to create 'tblUsers'. It might already exists")
    
    try:
        print("Creating table 'tblUserFavorites'")
        cursor.execute(create_tblUserFavorites)
    except:
        print("Unable to create 'tblUserFavorites'. It might already exists")

    conn.commit()

    print("Database created.")

    print("Adding stations to the database...")
    UpdateDBContents()._update_stations()
    
    conn.close()
