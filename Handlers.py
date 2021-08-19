import tkinter.messagebox
import SignIn

def SignInHandler(username, password):
      if len(username) <= 0:
          tkinter.messagebox.showwarning( "Message", "User Name can not be empty")
      elif len(password) <= 0:
          tkinter.messagebox.showwarning( "Message", "password can not be empty")
      else :
          if SignIn.trySigningIn(username, password)==True:
              #Opens a new window
              tkinter.messagebox.showinfo("Error", "Not implemented yet")
          else:
              tkinter.messagebox.showerror("Error", "Error in sign-in")


