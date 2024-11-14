# OneTrack:Alpha

## Required modules:

To run OneTrack, the modules listed in `requirements.txt` should be installed. These can be installed simultaneously by running

```
pip install /requirements.txt
```

> [!TIP]
> If dotenv doesn't work, try importing pydotenv, and replace all imports in files.

## RealTime Trains API

> [!IMPORTANT]
> To access OneTrack, an API key and username can be created [here](https://api.rtt.io/accounts/register)
>
> Once you have an account, change your username and token in a `.env` file. This should be added into the `App` folder

## Hashing

OneTrack uses hashing for saving data into the database. A hashing key is generated and saved in a file called `hash.txt`. This file should contain data as shown below:

```
hash_key = [your_hash_key]
```

It is recommended that the hash key contains 16 (sixteen) base 64 characters. The file `createHash.py` can be used to create a 16-character random hash. Using your own hash will mean that signing into OneTrack with any password already in the database will not work, so all current passwords should be reset for this to work.

> [!WARNING]
> It is not recommended to reset the hash key during public deployment. Resetting your hash key will cause all data in the database to be invalid as passwords will not verify correctly.
