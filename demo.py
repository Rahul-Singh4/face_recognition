from tkinter import *
from tkinter import filedialog
import cv2
import os
#from PIL import ImageTk,Image
import  tkinter.messagebox as MessageBox
import mysql.connector as mysql

def insert():
    name=nameentry.get()
    Univ_id=Univ_entry.get()
    Course=Courseentry.get()
    Phone=Phoneentry.get()

    if (name=="" or Univ_id=="" or Course=="" or Phone==""):
        MessageBox.showinfo("Insert Status ","All Fields are required ")
    else:
        con=mysql.connect(host="localhost",user="root",password="User@1234",database = "Regform", auth_plugin='mysql_native_password')
        cursor=con.cursor()
        cursor.execute("insert into Reg values('"+ name +"','"+ Univ_id +"','"+ Course +"','"+ Phone +"')" )
        cursor.execute("commit")

        nameentry.delete(0,'end')
        Univ_entry.delete(0,'end')
        Courseentry.delete(0,'end')
        Phoneentry.delete(0,'end')

        MessageBox.showinfo("Insert Status ","Inserted Successfully ")
        con.close()

root=Tk()

root.geometry("700x400")
root.title("Registration form")
Label(root,text=" REGISTRATION FORM ",font="comicsansms 15 bold",pady=16).place(x=40,y=10)
name=Label(root,text="Name",font=('bold',10))
name.place(x=20,y=60)
Univ_id=Label(root,text="Univ Id",font=('bold',10))
Univ_id.place(x=20,y=90)
Course=Label(root,text="Course",font=('bold',10))
Course.place(x=20,y=120)
Phone = Label(root,text="Phone",font=('bold',10))
Phone.place(x=20,y=150)


nameentry=Entry()
nameentry.place(x=150,y=60)
Univ_entry=Entry()
Univ_entry.place(x=150,y=90)
Courseentry=Entry()
Courseentry.place(x=150,y=120)
Phoneentry=Entry()
Phoneentry.place(x=150,y=150)

directory = r'C:/Users/Rahul0004/Desktop/Project/Dataset/Images'
os.chdir(directory) 
def webrec():
    webcam=cv2.VideoCapture(0)
    while True:
        value,frame=webcam.read()
        if value==False:
            break;
        else:
            cv2.imshow("Capture",frame)           
            cv2.imwrite(filename=f"{Univ_entry.get()}.png",img=frame)
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
    webcam.release()
    cv2.destroyAllWindows()

button= Button(root,text="Take your Photo",font=("italic",10),bg="white",command=webrec)
button.place(x=100,y=180)

insert=Button(root,text="Submit here ",font=("italic",10),bg="white",command=insert)
insert.place(x=100,y=220)
root.mainloop()