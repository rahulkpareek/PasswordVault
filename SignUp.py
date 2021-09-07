from tinydb import TinyDB, Query
import DBhelper

def RegisterUser(firstname,lasttname,email,userid,password):
    db = TinyDB('db1.json')
    checkuserid = Query()
    userexist = db.contains(checkuserid.userid == userid)
    print("checking user name exist",userexist)
    if userexist == False:
           encryptedpassword= DBhelper.encrypt_string(password+userid)
           db.insert({"firstname":firstname, "lasttname":lasttname,"email":email,"userid":userid,"password":encryptedpassword})
           return (True, "Successfully Registered")
    else :
           return (False, 'User Id {0} already exist'.format(userid))


