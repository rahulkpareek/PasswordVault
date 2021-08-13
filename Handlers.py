import tkinter.messagebox
import login


def SignInCallBack():
      
      username1 = login.usernamevalue.get()
      password1 = login.passwordvalue.get()

      if len(username1) <= 0:
          tkinter.messagebox.showwarning( "Message", "User Name can not be empty")
      elif len(password1) <= 0:
          tkinter.messagebox.showwarning( "Message", "password can not be empty")
      else :
          tkinter.messagebox.showwarning( "Message", "Not implemented yet..")


