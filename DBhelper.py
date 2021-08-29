from tinydb import TinyDB, Query
import hashlib

def ConnectToDatabase(dbfile):
    dbconnection=TinyDB(dbfile)
    return dbconnection

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def SearchDB(db, field, value):
    try:
       qry=Query()
       result = db.get(qry[field]==value)
       return result
    except IndexError:
        return None

def InsertinDB(db, val):
    try:
        db.insert(val)
        return True
    except IndexError:
        return False

def DeleteFromDB(db, query):
    try:
        db.remove(query)
        return True
    except IndexError:
        return False

def DeleteAllFromDB(db):
    try:
        db.truncate()
        return True
    except IndexError:
        return False

def MakeQuery():
    return Query()

