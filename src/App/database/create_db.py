import sqlite3

from src.app.database.update_db_contents import UpdateDBContents

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
    cursor.execute(create_tblStations)
    print("Creating table 'tblStations'")

    cursor.execute(create_tblUsers)
    print("Creating table 'tblUsers'")
    
    cursor.execute(create_tblUserFavorites)
    print("Creating table 'tblUserFavorites'")

    conn.commit()

    conn.close()

    UpdateDBContents()._update_stations()

if __name__ == "__main__":
    create_database()