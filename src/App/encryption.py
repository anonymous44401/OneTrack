import scrypt

class Encryption():
    def __init__(self):
        # Open the files and read the keys
        with open("src/App/keys/hash.txt", "r") as file:
            self.__key = file.read()

        with open("src/App/keys/rtt_user.txt", "r") as file:
            self.__rtt_user = file.read()

        with open("src/App/keys/hash.txt", "r") as file:
            self.__rtt_user = file.read()

    def _encrypt_item(self, item):
        # Encrypt the item
        return scrypt.encrypt(item, self.__key, maxtime=0.1)
    
    def _decrypt_item(self, item):
        # Decrypt the item
        return scrypt.decrypt(item, self.__key, maxtime=0.1)

    def _validate_items(self, item_to_check, correct_item):
        # Check of the items to check is the same as the decrypted item
        if self._decrypt_item(correct_item) == item_to_check:
            return True
        
        return False