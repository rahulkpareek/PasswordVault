import hashlib
from tinydb import TinyDB, Query
import DBhelper

def CheckUsernameExists(db, username):
    return DBhelper.SearchDB(db, 'user', username)

def GetAllUserInfo(db,username):
    return DBhelper.SearchDB(db, 'det', username)

def trySigningIn(username, password):
    db=DBhelper.ConnectToDatabase('db.json')
    if db != None:
        userdata=CheckUsernameExists(db, username)
        if userdata == None:
            return (False, 'User {0} doesn\'t exist'.format(username))
        else:
            # the combination of username as first part and password as second part of the string is used as salt here
            if userdata['password'] == DBhelper.encrypt_string(username+password):
                return (True, 'Successful login')
            else:
                return (False, 'Wrong password entered')
    else:
        return (False,'Cannot connect to a database')

def DisplayUserInfo(username, password):
    db=DBhelper.ConnectToDatabase('dbinfo.json')
    if db != None:
        # the combination of password as first part and username as second part of the string is used as salt here
        sha_sig=DBhelper.encrypt_string(password+username)
        #For now, dump the info in a text file. This can be later sent to a window which displays all the user related input 
        info = GetAllUserInfo(db, sha_sig) 
        file1 = open("info.txt","w")
        file1.write()
        file1.writelines("\n")
        file1.close() #to change file access modes

