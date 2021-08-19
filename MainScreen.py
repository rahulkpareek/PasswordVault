from tkinter import *
import Handlers

#import Handlers
def SignInCallback():
    Handlers.SignInHandler(usernameVal.get(), passwordVal.get())


#UI code
wnd = Tk()

#name to be changed with newer version release
wnd.title("PasswordVault 1.0")
wnd.geometry('400x400')

#photo
photo = PhotoImage(file=".\PasswordVault-main\PasswordVault-main\Logo.png")
image_label = Label(image=photo)
image_label.grid(row=0,column=0)


#Username and Password Labels
Label(wnd, text="UserName").grid(row=1, column=0)
Label(wnd, text="Password").grid(row=9, column=0)

#Username and Password Entry
usernameVal=StringVar()
passwordVal=StringVar()
usernameentry = Entry(wnd, bd =5,textvariable=usernameVal).grid(row=1, column=11)
passwordentry = Entry(wnd, bd =5,show='*',textvariable=passwordVal).grid(row=9, column=11)

#Button
Button(wnd, text ="Sign in", command = SignInCallback).grid(row=14, column=0)

# Code to add widgets will go here...

wnd.mainloop()



