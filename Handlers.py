import tkinter.messagebox
import SignIn

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


