import hashlib

def ConnectToDatabase():
    dbconnection=None
    return dbconnection

#encrytion code
def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def trySigningIn(username, password):
    db=ConnectToDatabase()
    if db != None:
        # this salt is further encrytped and stored in the password column of the tabLogin.
        salt=username+password
        sha_sig=encrypt_string(salt)
        return True
    else:
        return False