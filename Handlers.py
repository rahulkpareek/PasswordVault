import tkinter.messagebox
import SignIn
import SignUp

def SignInHandler(username, password):
      if len(username) <= 0:
          tkinter.messagebox.showwarning( "Error", "User Name can not be empty")
      elif len(password) <= 0:
          tkinter.messagebox.showwarning( "Error", "password can not be empty")
      else :
          res = SignIn.trySigningIn(username, password)
          if res[0]==True:
              #Opens a new window
              tkinter.messagebox.showinfo("Success",res[1])
              SignIn.DisplayUserInfo(username, password)
          else:
              tkinter.messagebox.showerror("Error",res[1])



def SubmitDetails(firstname,lasttname,email,userid,password,repassword):

    if len(firstname) == 0 :
        tkinter.messagebox.showwarning( "Message", "First-name can not be empty")
    elif len(lasttname) == 0 :
        tkinter.messagebox.showwarning( "Message", "Last-name can not be empty")
    elif len(email) == 0 :
        tkinter.messagebox.showwarning( "Message", "Email id can not be empty")
    elif len(userid) == 0 :
        tkinter.messagebox.showwarning( "Message", "User id can not be empty")
    elif len(password) == 0 :
        tkinter.messagebox.showwarning( "Message", "Password can not be empty")    
    elif len(repassword) == 0 :
        tkinter.messagebox.showwarning( "Message", "Please re-enter the Password")
    elif password != repassword :
        tkinter.messagebox.showwarning( "Message", "Passwords does not match")
    else:
          res = SignUp.RegisterUser(firstname,lasttname,email,userid,password)
          if res[0]==True:
              #Opens a new window
              tkinter.messagebox.showinfo("Success",res[1])
          else:
              tkinter.messagebox.showerror("Error",res[1])      
    
   


