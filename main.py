#!/bin/env python
from tkinter import *
import json
from tkinter import ttk
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
from mac_say import say
from time import sleep

#-- funtion to issue a bash script to install requirements?--
#create requirements file test 2

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_pw():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    password_list_nsym = password_letters + password_numbers

    shuffle(password_list)

    password = "".join(charac for charac in password_list)
    password_nsym = "".join(charac for charac in password_list_nsym)

    pw_entry.insert(0, password)
    pyperclip.copy(password)

    return password
    #print(f"Your password is: {password_nsym}")

# ---------------------------- PASSWORD GENERATOR (no symbols) ------------------------------- #
#gen w/o symbols
def generate_pw_nym():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    #password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    #password_list = password_letters + password_numbers + password_symbols
    password_list_nsym = password_letters + password_numbers

    shuffle(password_list_nsym)

    #password = "".join(charac for charac in password_list)
    password_nsym = "".join(charac for charac in password_list_nsym)

    
    pw_entry.insert(0, password_nsym)
    pyperclip.copy(password_nsym)
    return password_nsym

# ---------------------------- LOGIN SEARCH ------------------------------- #
def search():
    #check if the provided service is in our mr_p.json data
    #it cant be "got" twice??? data retrieved in save()
    item_to_search = search_entry.get()
    print(item_to_search)
    if len(item_to_search) < 1:
        messagebox.showinfo(title="error", message="Nothing given to search!")
    
    try:
        with open("mr_p.json", "r") as data_file:
            #reading old data
            #length = len(data_file)
            #messagebox.showinfo(title="something", message=f"lenghty: {length}")
            data = json.load(data_file)
    except json.JSONDecodeError:
        messagebox.showinfo(title="No entries found in pw file", message="There are no logins to search through, add a login buddy")
        return

    except FileNotFoundError:
        messagebox.showinfo(title="No existing pw file found", message="There are no logins to search through, add a login buddy")
        return
    
    #try:
    username = data[item_to_search]["user"]
    password = data[item_to_search]["password"]
    messagebox.showinfo(title="login", message=f"Service: {item_to_search}\nUsername: {username}\nPassword: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #
# if pw file is empty, but DOES exist, it crashes
def save():

    service = service_entry.get()
    username = email_entry.get()
    pw = pw_entry.get()
    new_data = {
        service: {
            "user": username,
            "password": pw
        }
    }


    for e in [service, username, pw]:
        if len(e) < 1:
            messagebox.showinfo(title="error", message="Don't leave any of the fields empty!")
            service_entry.delete(0, END)
            email_entry.delete(0, END)
            pw_entry.delete(0, END)
            return
    prompt_ok_user = messagebox.askokcancel(title=service, message=f"These are the details entered:\nusername: {username}\npassword: {pw}\nHit OK to save")

    if prompt_ok_user:
        try:
            with open("mr_p.json", "r") as data_file:
                #reading old data
                data = json.load(data_file)

        except json.JSONDecodeError:
            with open("mr_p.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        except FileNotFoundError:
            messagebox.showinfo(title="No existing pw file found", message="No existing pw file found, creating a new file called mr_p.json")
            # creating new file if no old data
            with open("mr_p.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("mr_p.json", "r") as data_file:
                #reading old data
                data = json.load(data_file)
            # upd file with new data
                data.update(new_data)
            with open("mr_p.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

                # data_file.write(f"{service} | {username} | {pw}\n")
        finally:
            service_entry.delete(0, END)
            email_entry.delete(0, END)
            pw_entry.delete(0, END)
            say("password added! fuck yeah!")
            sleep(.25)



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
canvas = Canvas(width=300, height=280, bd=0, highlightthickness=0)
myimg = PhotoImage(file='mr_pass2.png')
canvas.create_image(140, 140, image=myimg)
canvas.grid(row=0, column=1)

#Labels 
service_label = Label(text="Service: ", bg='#000', fg='#f00')
service_label.grid(row=2, column=0)
email_user_label = Label(text="Email or username: ", bg='#000', fg='#f00')
email_user_label.grid(row=3, column=0)
pw_label = Label(text="Password: ", bg='#000', fg='#f00')
pw_label.grid(row=4, column=0)  

#Entries
service_entry = Entry(width=35, fg='#000')
service_entry.grid(row=2, column=1, columnspan=2)
email_entry = Entry(width=35)
#auto add the username
#email_entry.insert(0, ian@gmail.com)   
email_entry.grid(row=3, column=1, columnspan=2)
pw_entry = Entry(width=35)
pw_entry.grid(row=4, column=1)

search_entry = Entry(width=34)
search_entry.grid(row=1, column=1, columnspan=1)

#Buttons
gen_pw_button = Button(text="Generate password", fg='#f00', highlightbackground="#999", width=36, height=3, command=generate_pw) #highlightbackground="#999")
gen_pw_button.grid(row=5, column=1, columnspan=2)
gen_pw_nsym_button = Button(text="Generate password w/o symbols", fg='#f00', highlightbackground="#999", width=36, height=3, command=generate_pw_nym) #highlightbackground="#000")
gen_pw_nsym_button.grid(row=6, column=1, columnspan=2)
add_button = Button(text="Add login", width=36, height=3, fg='#f00', highlightbackground="#999", command=save)
add_button.grid(row=9, column=1, columnspan=2)
search_button = Button(text="Search logins:\n(by service, i.e. Spotify)", fg='#f00', highlightbackground="#999", width=16, height=3, command=search)
search_button.grid(row=1, column=0, columnspan=1)

#canvas.grid()
window.config(padx=50, pady=50, bg="black")

window.mainloop()