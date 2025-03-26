import base64
import maskpass
import os

from app.database.create_db import create_database


if __name__ == "__main__":
    # Create the keys directory
    os.mkdir("src/app/keys")

    # Add the hash
    with open("src/app/keys/hash.txt", "x") as file:
        file.write(base64.b64encode(os.urandom(12)).decode('utf-8')[:16])

    print("Hash key created and saved.")

    # Add the RTT Username and Token
    with open("src/app/keys/rtt_user.txt", "x") as file:
        file.write(input("Enter the RTT username: "))

    print("RTT username saved.")

    with open("src/app/keys/rtt_token.txt", "x") as file:
        file.write(maskpass.askpass(prompt="Enter the RTT token: ", mask="•"))

    print("RTT token saved.")
    
    create_database()

    print("Setup complete.")