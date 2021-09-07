from tkinter import *
from tkinter.font import BOLD
import Handlers
import tkinter.messagebox
def SignUpHandler(wnd):
    
    def SubmitDetails():
        Handlers.SubmitDetails(firstnamevalue.get(),
                           lasttnamevalue.get(),
                           emailvalue.get(),
                           useridvalue.get(),
                           passwordvalue.get(),
                           repasswordvalue.get())
    
    wnd.destroy()
    #UI code
    reg = Tk()

    #name to be changed with newer version release
    reg.title("PasswordVault 1.0")
    reg.geometry('405x405')

#photo
    backgroundphoto = PhotoImage(file="Logo.png")
    image_label = Label(image=backgroundphoto,padx=2,pady=2)
    image_label.place(x=0,y=0)


#Username and Password Labels
    firstnamelabel = Label(reg,text ="First Name",bg = "dark blue" ,fg = "White",font=("Arial", 10,BOLD)).place(x=100,y=40 )
    lastnamelabel = Label(reg,text ="Last Name",bg = "dark blue" ,fg = "White",font=("Arial", 10,BOLD)).place(x=100,y=80 )
    emaillabel = Label(reg,text ="Email-Id",bg = "dark blue" ,fg = "White",font=("Arial", 10,BOLD)).place(x=100,y=120 )
    useridlabel = Label(reg,text ="User Name",bg = "dark blue" ,fg = "White",font=("Arial", 10,BOLD)).place(x=100,y=160 )
    passwordlabel = Label(reg,text ="Password",bg = "dark blue" ,fg = "White",font=("Arial", 10,BOLD)).place(x=100,y=200 )
    repasswordlabel = Label(reg,text ="Re-enter Password",bg = "dark blue" ,fg = "White",font=("Arial", 10,BOLD)).place(x=100,y=240 )

    firstnamevalue = StringVar()        
    lasttnamevalue = StringVar()
    emailvalue = StringVar()
    useridvalue = StringVar()
    passwordvalue = StringVar()
    repasswordvalue = StringVar() 


    firstnameentry = Entry(reg,bd =2,textvariable=firstnamevalue).place(x=225,y=42 )
    lastnameentry = Entry(reg,bd =2,textvariable=lasttnamevalue).place(x=225,y=82 )
    emailentry = Entry(reg,bd =2,textvariable=emailvalue).place(x=225,y=122 )
    useridentry = Entry(reg,bd =2,textvariable=useridvalue).place(x=225,y=162 )
    passwordentry = Entry(reg,bd =2,textvariable=passwordvalue).place(x=225,y=202 )
    repasswordentry = Entry(reg,bd =2,textvariable=repasswordvalue).place(x=225,y=242 )

    firstname  = firstnamevalue.get()
    lasttname  = lasttnamevalue.get()
    email      = emailvalue.get()
    userid     = useridvalue.get()
    password   = passwordvalue.get()
    repassword = repasswordvalue.get()

    signupbutton = Button(reg,text ="Submit",command = SubmitDetails).place(x=205,y=300 )
    reg.mainloop()



