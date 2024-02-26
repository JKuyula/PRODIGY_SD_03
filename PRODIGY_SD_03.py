'''
Author : Joelle Kabaka Kuyula
In this program, we have created a contact management system that allows us to add, view, update and delete contact entries.
'''
from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import re
from idlelib import tree

import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact List")
root.geometry("700x400")

# Declaring variables
NAME = StringVar()
CONTACT = StringVar()
EMAIL= StringVar()


# Fonction for creating the database and the table
def Database():
    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'contacts' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,name  TEXT,  phoneNumber  TEXT, email  TEXT)")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()

#Validate the contact number
def isvalid(contact1):
    pattern = re.compile("^[0-9]{10}$")
    return pattern.match(contact1)
#Function to reset the values
def Reset():
    # clear current data from table
    tree.delete(*tree.get_children())
    # refresh table data
    DisplayData()
    # clear search text
    NAME.set("")
    CONTACT.set("")
    EMAIL.set("")

def SubmitData2():
    # Getting form data
    name1 = NAME.get()
    contact1 = CONTACT.get()
    email1 = EMAIL.get()

    # Applying empty validation
    if name1 == '' or contact1 == '' or email1 == '':
        tkMessageBox.showinfo("Warning", "fill the empty field!!!")
    else:
        if isvalid(contact1):
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            # update query
            conn = sqlite3.connect("contact.db")
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE contacts SET name=?, phoneNumber=?, email=? WHERE oid = ?',
                (name1, contact1, email1, selecteditem[0]))
            conn.commit()
            tkMessageBox.showinfo("Message", "Contact updated successfully")
            # Reset form
            Reset()
            # Refresh table data
            DisplayData()
            conn.close()
        else:
            tkMessageBox.showinfo("Error", "The contact number should have 10 digits and start with 0")
            Reset()

        # def UpdateData():
        # Update()
def UpdateData():

    global NewWindow
    NAME.set("")
    CONTACT.set("")
    EMAIL.set("")
    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    NewWindow.geometry("500x300")

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)

    # Labels
    lbl_title = Label(FormTitle, text="Edit contact", font=('arial', 16), bg="lightblue", width=300)
    lbl_title.pack(fill=X)
    lbl_name = Label(ContactForm, text="Name", font=('arial', 14), bd=5)
    lbl_name.grid(row=0, sticky=W)
    lbl_phoneNumber = Label(ContactForm, text="Phone number", font=('arial', 14), bd=5)
    lbl_phoneNumber.grid(row=4, sticky=W)
    lbl_email = Label(ContactForm, text="Email address", font=('arial', 14), bd=5)
    lbl_email.grid(row=5, sticky=W)

    # Entries
    name = Entry(ContactForm, textvariable=NAME, font=('arial', 14))
    name.grid(row=0, column=1)
    phoneNumber = Entry(ContactForm, textvariable=CONTACT, font=('arial', 14))
    phoneNumber.grid(row=4, column=1)
    email = Entry(ContactForm, textvariable= EMAIL, font=('arial', 14))
    email.grid(row=5, column=1)

    # Creating a button to update a record
    btn_addcon = Button(ContactForm, text="Save", width=50, command=SubmitData2)
    btn_addcon.grid(row=6, columnspan=2, pady=10)


def DeleteRecord():
    if not tree.selection():
        tkMessageBox.showwarning("Warning", "Select data to delete")
    else:
        result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("contact.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE oid = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()


def DisplayData():
    # clear current data
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    # fetch all data from database
    fetch = cursor.fetchall()
    # loop for displaying all data in GUI
    for data in fetch:
        tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()


def validation(phoneNumber):  # Validate the phone number
    p = re.compile("^[0-9]{10}$")
    return p.match(phoneNumber)


def SubmitData1():  # save data into the database
    name = NAME.get()
    contact = CONTACT.get()
    email = EMAIL.get()

    if name == "" or contact == "" or email == "":
        tkMessageBox.showwarning('Error', 'Please complete the required field', icon="warning")
    else:
        if validation(contact):
            tree.delete(*tree.get_children())
            # insert query
            conn = sqlite3.connect("contact.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO 'contacts' (name, phoneNumber, email) VALUES(?, ?, ?)",
                (
                    str(name),
                    str(contact),
                    str(email),))
            conn.commit()
            tkMessageBox.showinfo("Message", "Contact recorded successfully")
            cursor.execute("SELECT * FROM contacts")
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=data)
            cursor.close()
            conn.close()
            NAME.set("")
            CONTACT.set("")
            EMAIL.set("")
        else:
            tkMessageBox.showinfo("Error", "The contact number should have 10 digits and start with 0")
            Reset()

def AddNew():
    global NewWindow
    NAME.set("")
    CONTACT.set("")
    EMAIL.set("")

    NewWindow = Toplevel()
    NewWindow.title("Contact List")
    NewWindow.geometry("500x280")

    # Create a new frame
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)

    # Labels
    lbl_title = Label(FormTitle, text="Add new contact", font=('arial', 16), bg="lightblue", width=300)
    lbl_title.pack(fill=X)
    lbl_name = Label(ContactForm, text="Name", font=('arial', 14), bd=5)
    lbl_name.grid(row=0, sticky=W)
    lbl_phoneNumber = Label(ContactForm, text="Phone Number", font=('arial', 14), bd=5)
    lbl_phoneNumber.grid(row=4, sticky=W)
    lbl_email = Label(ContactForm, text="Email Address", font=('arial', 14), bd=5)
    lbl_email.grid(row=5, sticky=W)

    # Entries
    name = Entry(ContactForm, textvariable=NAME, font=('arial', 14))
    name.grid(row=0, column=1)
    phoneNumber = Entry(ContactForm, textvariable=CONTACT, font=('arial', 14))
    phoneNumber.grid(row=4, column=1)
    email = Entry(ContactForm, textvariable=EMAIL, font=('arial', 14))
    email.grid(row=5, column=1)

    # Create a button to submit values
    btn_save = Button(ContactForm, text="Save", width=50, command=SubmitData1)
    btn_save.grid(row=6, columnspan=2, pady=10)

#Frames
Form = Frame(root, width=600, bd=1, relief=SOLID)
Form.pack(side=TOP, fill=X)
Mid = Frame(root, width=700)
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=400)
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

# label for heading
lbl_text = Label(Form, text="Contact Management System", font=('Arial', 18), width=600,bg="lightblue")
lbl_text.pack(fill=X)

# Create CRUD buttons
btn_add = Button(MidLeft, text="ADD A NEW", command=AddNew, bg="lightblue")
btn_add.grid(row=0, column=0)
btn_view = Button(MidLeft, text="VIEW", command=DisplayData, bg="lightblue")
btn_view.grid(row=0, column=1)
btn_change = Button(MidRight, text="EDIT", command=UpdateData, bg="lightblue")
btn_change.grid(row=0, column=2)
btn_delete = Button(MidRight, text="DELETE", command=DeleteRecord, bg="lightblue")
btn_delete.grid(row=0, column=3)

# Setting scrollbar
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin,
                    columns=("ID", "name", "phoneNumber", "email"),
                    selectmode="extended", height=100, yscrollcommand=scrollbary.set,
                    xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

# Setting headings for the columns for the main window
tree.heading('ID', text="ID", anchor=W)
tree.heading('name', text="Name", anchor=W)
tree.heading('phoneNumber', text="Phone Number", anchor=W)
tree.heading('email', text="Email Address", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.pack()



if __name__ == '__main__':
     Database()
     root.mainloop()


