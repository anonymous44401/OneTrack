import base64
import os
import scrypt

class Encryption():
    def __init__(self):
        # Open the files and read the keys
        with open("src/App/keys/hash.txt", "r") as file:
            self._key = file.read()

        with open("src/App/keys/rtt_user.txt", "r") as file:
            self._rtt_user = file.read()

        with open("src/App/keys/rtt_token.txt", "r") as file:
            self._rtt_token = file.read()

    def _encrypt_item(self, item) -> str:
        # Encrypt the item
        b = scrypt.encrypt(item, self._key, maxtime=0.1)

        # Return the encrypted item
        return base64.b64encode(b).decode("utf-8")
    
    def _decrypt_item(self, item) -> str:
        # Convert to base64
        b = base64.b64decode(item)
        
        # Decrypt the item
        return scrypt.decrypt(b, self._key, maxtime=0.1)

    def _validate_items(self, item_to_check, correct_item) -> bool:
        # Check of the items to check is the same as the decrypted item
        if self._decrypt_item(correct_item) == item_to_check:
            return True
        
        return False
    
    def __create_hash():
        # Encode the randomly generated 12-byte string (16 characters) to a base64 string, with only the first 16 characters
        base64_string = base64.b64encode(os.urandom(12)).decode('utf-8')[:16] 

        # Print the generated hash
        print(base64_string)