import base64
import os

random_bytes = os.urandom(12)
base64_string = base64.b64encode(random_bytes).decode('utf-8')[:16] 

print(base64_string)