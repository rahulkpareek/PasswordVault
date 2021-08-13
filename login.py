from tkinter import *
import Handlers

wnd = Tk()

#name to be changed with newer version release
wnd.title("PasswordVault 1.0")

B = Button(wnd, text ="Sign in", command = Handlers.SignInCallBack)

B.pack()
# Code to add widgets will go here...
wnd.mainloop()



