from nacl.pwhash import argon2i, secret, utils

kdf = argon2i.kdf

def pass_salt():
    return utils.random(argon2i.SALTBYTES)

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
              opslimit = argon2i.OPSLIMIT_SENSITIVE,
              memlimit = argon2i.MEMLIMIT_SENSITIVE)
    
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
              opslimit = argon2i.OPSLIMIT_SENSITIVE,
              memlimit = argon2i.MEMLIMIT_SENSITIVE)
    
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