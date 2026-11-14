# BASIC COMMAND-LINE PASSWORD MANAGER (COLLEGE LEARNING PROJECT)

# STAGE 1: MASTER-PASSWORD AUTHENTICATION (HASH + VERIFY)
# STAGE 2: SEPARATE ENCRYPTION KEY + ENCRYPTED VAULT (data.enc)

import base64
import hashlib
import hmac
import json
import os

from cryptography.fernet import Fernet

CONFIG_FILE = "config.json"
DATA_FILE = "data.enc"

PBKDF2_ITERATIONS = 600_000 # 600_000 ITERATIONS (BRIEF)
SALT_SIZE = 16 # 128 BITS FOR SALTS
HASH_ALGORITHM = "sha256" # SHA-256 STRONG GOOD HASH USED INSIDE PBKDF2
KEY_SIZE = 32 # FERNET NEEDS A 256-BIT KEY
MIN_PASSWORD_LENGTH = 8

### SALT HELPER FUNCTIONS

# RETURN 16 RANDOM BYTES FOR THE SALT
def generate_salt():
    return os.urandom(SALT_SIZE)


# HASHES THE PASSWORD WITH PBKDF2-HMAC-SHA256 AND THE SALT
# RETURNS RAW BYTES
def hash_password(password, salt):
    password_bytes = password.encode("utf-8")
    return hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password_bytes,
        salt,
        PBKDF2_ITERATIONS,
    )


# Fernet ENCRYPTION KEY FROM THE MASTER PASSWORD + kdf_salt
# RETURNS URL-SAFE BASE64-ENCODED 32-BYTE KEY
def derive_key(password, kdf_salt):
    key_bytes = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        kdf_salt,
        PBKDF2_ITERATIONS,
        dklen=KEY_SIZE,
    )
    # Fernet REQUIRES THE KEY AS URL-SAFE BASE64 OF EXACTLY 32 RAW BYTES
    return base64.urlsafe_b64encode(key_bytes)


### INPUT AND OUTPUT CONFIG FILE

# WRITE THE SALTS AND AUTH HASH TO config.json AS HEX STRINGS
def save_config(auth_salt, auth_hash, kdf_salt):
    data = {
        "auth_salt": auth_salt.hex(),
        "auth_hash": auth_hash.hex(),
        "kdf_salt": kdf_salt.hex(),
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# LOAD config.json AND RETURN THE (auth_salt, auth_hash, kdf_salt) AS BYTES
# IF FIRST RUN CASE IT WILL RETURN NONE BECAUSE THE FILE IS MISSING
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return (
        bytes.fromhex(data["auth_salt"]),
        bytes.fromhex(data["auth_hash"]),
        bytes.fromhex(data["kdf_salt"]),
    )


### VAULT INPUT OUTPUT
# data.enc HOLDS THE WHOLE VAULT AS ONE Fernet CIPHERTEXT
# EVERY ADD OR DELETE WILL RE-ENCRYPT AND OVERWRITE data.enc TOODOO!!!!!!
def save_vault(vault, key):
    fernet = Fernet(key)
    plaintext = json.dumps(vault).encode("utf-8") # DICT -> TEXT -> BYTES
    token = fernet.encrypt(plaintext)
    with open(DATA_FILE, "wb") as f:
        f.write(token)


# DECRYPT data.enc AND RETURN THE VAULT AS A DICT
# IF data.enc IS MISSING IT CREATES AN EMPTY VAULT FILE
def load_vault(key):
    if not os.path.exists(DATA_FILE):
        vault = {"entries":[]} #because vault page reads "entries" 
        save_vault(vault, key)
        return vault

    with open(DATA_FILE, "rb") as f:
        token = f.read()

    fernet = Fernet(key)
    plaintext = fernet.decrypt(token)
    return json.loads(plaintext.decode("utf-8"))


### GUI FUNCTIONS
#  for views/register
# FIRST RUN: MASTER PASSWORD SALTS AUTH HASH EMPTY ENCRYPTED VAULT
def register(password, confirm):
    # check if config file/user account has already been created
    if os.path.exists(CONFIG_FILE):
        raise ValueError("An account already exists. Please log in.")
    # check password length
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")
    if password != confirm:
        raise ValueError("Passwords do not match. Please try again.")
    auth_salt = generate_salt()
    kdf_salt = generate_salt()
    auth_hash = hash_password(password, auth_salt)
    save_config(auth_salt, auth_hash, kdf_salt)

    # create empty vault
    key = derive_key(password, kdf_salt)
    vault = {"entries":[]}
    save_vault(vault, key)
    return key, vault

### for views/login
def login(password):
    config = load_config()
    if config is None:
        raise ValueError("No account yet. Register first.")
    auth_salt, auth_hash, kdf_salt = config
    attempt_hash = hash_password(password, auth_salt)
    # WHY hmac.compare_digest NOT == : AVOIDS TIMING LEAKS
    if not hmac.compare_digest(attempt_hash, auth_hash):
        raise ValueError("Wrong password.")    
    # AUTH PASSED SAFE TO GET THE KEY AND OPEN THE VAULT
    key = derive_key(password, kdf_salt)
    vault = load_vault(key)
    return key, vault

### delete config.json and data.enc (the master password/account and all saved entries in vault)
def delete_all():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
