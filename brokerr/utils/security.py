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
    # Reverse the password
    reverse = "".join(reversed(password))
    # Hash the reversed password
    hash_reverse = hash_pw(reverse)
    # Store it in memory
    redis_db.set("master_password", hash_reverse)

def validate_password(hash, password):
    try:
        result = nacl.pwhash.verify(hash, password.encode('utf-8'))
        return result
    except nacl.exceptions.InvalidkeyError:
        return False

def encrypt(plaintext: str, master_password: str):
    """
    Encrypts the specified plaintext string using the master password

    :param plaintext: String to be encrypted
    :param master_password: The password used for encrypting/decrypting
    """
    salt = pass_salt()
    
    key = kdf(secret.SecretBox.KEY_SIZE,
              master_password,
              salt,
              opslimit = nacl.pwhash.argon2i.OPSLIMIT_SENSITIVE,
              memlimit = nacl.pwhash.argon2i.MEMLIMIT_SENSITIVE)
    
    box = secret.SecretBox(key)
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    encrypted_pass = box.encrypt(plaintext, nonce)

    return (encrypted_pass, salt, ops, mem)

def decrypt(encrypted_string, master_password, salt):
    """
    Attempts to decrypt the provided string using the provided password and salt

    :param encrypted_string: The string to decrypt
    :param master_password: Password used as encryption key
    :param salt: The encryption salt
    """
    key = kdf(secret.SecretBox.KEY_SIZE,
              master_password,
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