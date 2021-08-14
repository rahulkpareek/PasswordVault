from tkinter import *
import tkinter.messagebox

#import Handlers

wnd = Tk()

def SignInCallBack():
      
      username1 = usernamevalue.get()
      password1 = passwordvalue.get()

      if len(username1) <= 0:
          tkinter.messagebox.showwarning( "Message", "User Name can not be empty")
      elif len(password1) <= 0:
          tkinter.messagebox.showwarning( "Message", "password can not be empty")
      else :
          tkinter.messagebox.showwarning( "Message", "Not implemented yet..")

#name to be changed with newer version release
wnd.title("PasswordVault 1.0")
wnd.geometry('400x400')

#photo
photo = PhotoImage(file="Logo.png")
image_label = Label(image=photo)
image_label.grid(row=0,column=0)


#Username and Password Labels
username = Label(wnd, text="UserName").grid(row=1, column=0)
password = Label(wnd, text="Password").grid(row=9, column=0)

#Entry values
usernamevalue = StringVar()
passwordvalue = StringVar()

#Username and Password Entry
usernameentry = Entry(wnd, bd =5,textvariable=usernamevalue).grid(row=1, column=11)
passwordentry = Entry(wnd, bd =5,show='*',textvariable=passwordvalue).grid(row=9, column=11)

#Button
signin = Button(wnd, text ="Sign in", command = SignInCallBack).grid(row=14, column=0)

# Code to add widgets will go here...

wnd.mainloop()



