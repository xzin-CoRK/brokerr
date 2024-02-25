from nacl import secret, utils
import nacl.pwhash
from data.dataLayer import redis_db


kdf = nacl.pwhash.argon2i.kdf

def pass_salt():
    """Generates and returns a random salt"""
    return utils.random(nacl.pwhash.argon2i.SALTBYTES)

def hash_pw(plaintext: str):
    return nacl.pwhash.str(plaintext.encode('utf-8'))

def generate_master_key(password: str):
    """
    Generates a master key based on the user's password, storing it in redis memory
    :param password: The user's plaintext password
    """
    # Reverse the password
    reverse = "".join(reversed(password))
    # Hash the reversed password
    hash_reverse = hash_pw(reverse)
    # Store it in memory
    redis_db.set("master_key", hash_reverse)

def validate_password(hash, password):
    try:
        result = nacl.pwhash.verify(hash, password.encode('utf-8'))
        return result
    except nacl.exceptions.InvalidkeyError:
        return False

def encrypt(plaintext: str):
    """
    Encrypts the specified plaintext string using the master password

    :param plaintext: String to be encrypted
    :param master_key: The key used for encrypting/decrypting
    """
    salt = pass_salt()
    
    key = kdf(secret.SecretBox.KEY_SIZE,
              redis_db.get("master_key"),
              salt,
              opslimit = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE,
              memlimit = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE)
    
    box = secret.SecretBox(key)
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    encrypted_pass = box.encrypt(plaintext.encode('utf-8'), nonce)

    return (encrypted_pass, salt)

def decrypt(encrypted_string, master_key, salt):
    """
    Attempts to decrypt the provided string using the provided password and salt

    :param encrypted_string: The string to decrypt
    :param master_key: Key used as encryption key
    :param salt: The encryption salt
    """
    key = kdf(secret.SecretBox.KEY_SIZE,
              master_key,
              salt,
              opslimit = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE,
              memlimit = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE)
    
    try:
        box = secret.SecretBox(key)
        decrypted_text =  box.decrypt(encrypted_string)

        return {
            "success": True,
            "decrypted_text": decrypted_text
        }
    except nacl.exceptions.CryptoError as ex:
        return {
            "success": False
        }