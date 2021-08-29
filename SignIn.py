import hashlib
from tinydb import TinyDB, Query

def ConnectToDatabase(dbfile):
    dbconnection=TinyDB(dbfile)
    return dbconnection

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def CheckUsernameExists(db, username):
    try:
       User=Query()
       username = encrypt_string(username)
       result = db.get(User['user']==username)
       return result
    except IndexError:
        return None

def trySigningIn(username, password):
    db=ConnectToDatabase('db.json')
    if db != None:
        userdata=CheckUsernameExists(db, username)
        if userdata == None:
            return (False, 'User {0} doesn\'t exist'.format(username))
        else:
            # the combination of username and password is used as salt
            if userdata['password'] == encrypt_string(username+password):
                return (True, 'Successful login')
            else:
                return (False, 'Wrong password entered')
    else:
        return (False,'Cannot connect to a database')

def DisplayUserInfo(username, password):
    sha_sig=encrypt_string(username+password)