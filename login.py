from tkinter import *
import Handlers

wnd = Tk()

#name to be changed with newer version release
wnd.title("PasswordVault 1.0")
wnd.geometry('500x400')

#Username Entry
L1 = Label(wnd, text="UserName").grid(row=1, column=0)
E1 = Entry(wnd, bd =5).grid(row=1, column=11)


#Password Entry
L2 = Label(wnd, text="Password").grid(row=9, column=0)
E2 = Entry(wnd, bd =5,show='*').grid(row=9, column=11)

#Button
B = Button(wnd, text ="Sign in", command = Handlers.SignInCallBack).grid(row=14, column=0)

# Code to add widgets will go here...

wnd.mainloop()



