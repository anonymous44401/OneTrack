import base64
import os

# Generate a random 12-byte string (16 characters) for hashing
random_bytes = os.urandom(12)
# Encode the random bytes to a base64 string, with only the first 16 characters
base64_string = base64.b64encode(random_bytes).decode('utf-8')[:16] 

# Print the generated hash
print(base64_string)