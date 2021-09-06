from tkinter import *
from tkinter.font import BOLD
import Handlers
import RegisterScreen

#import Handlers
def SignInCallback():
    Handlers.SignInHandler(usernamevalue.get(), passwordvalue.get())

def SignupCallBack():
    RegisterScreen.SignUpHandler(wnd)

#UI code
wnd = Tk()

#name to be changed with newer version release
wnd.title("PasswordVault 1.0")
wnd.geometry('405x405')

#photo
backgroundphoto = PhotoImage(file=".\Logo.png")
image_label = Label(image=backgroundphoto,padx=2,pady=2)
image_label.place(x=0,y=0)


#Username and Password Labels
usernamelabel = Label(wnd, text="UserName",bg = "dark blue" ,fg = "White",font=("Arial", 10,BOLD))
passwordlabel = Label(wnd, text="Password",bg = "dark blue" ,fg = "White",font=("Arial", 10,BOLD))
usernamelabel.place(x=100,y=40)
passwordlabel.place(x=100,y=80)

#Entry values declaration
usernamevalue = StringVar()
passwordvalue = StringVar()

#Username and Password Entry
usernameentry = Entry(wnd, bd =5,textvariable=usernamevalue)
passwordentry = Entry(wnd, bd =5,show='*',textvariable=passwordvalue)
usernameentry.place(x=200,y=42)
passwordentry.place(x=200,y=82)

#Button
#Button(wnd, text ="Sign in", command = SignInCallback).grid(row=14, column=0)
signinbutton = Button(wnd, text ="Sign in", command = SignInCallback)
signupbutton = Button(wnd, text ="Register New User",command = SignupCallBack)

signinbutton.place(x=100,y=130)
signupbutton.place(x=200,y=130)


wnd.mainloop()



