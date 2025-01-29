import base64
import os

# Encode the randomly generated 12-byte string (16 characters) to a base64 string, with only the first 16 characters
base64_string = base64.b64encode(os.urandom(12)).decode('utf-8')[:16] 

# Print the generated hash
print(base64_string)