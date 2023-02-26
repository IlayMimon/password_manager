import json
from tkinter import *
from tkinter import messagebox
import requests
import pyperclip
import os


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    random_pass = ""
    length = '16'
    api_url = 'https://api.api-ninjas.com/v1/passwordgenerator?length={}'.format(length)
    response = requests.get(api_url, headers={'X-Api-Key': os.environ.get("API_KEY")})
    if response.status_code == requests.codes.ok:
        response = response.json()
        random_pass = response["random_password"]
    else:
        print("Error:", response.status_code, response.text)
    pass_input.delete(0, 'end')
    pass_input.insert(0, random_pass)
    pyperclip.copy(random_pass)
    messagebox.showinfo(title="Copied!", message="Password is copied!")


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_input.get()
    try:
        with open("data.json", "r") as file:
            file.read()
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="There is no data saved yet.")
    else:
        with open("data.json", "r") as file:
            data = json.load(file)
            try:

                messagebox.showinfo(title=website,
                                    message=f'Email/Username: {data[website]["email"]}\n'
                                            f'Password: {data[website]["password"]}\n'
                                            f'The password is copied!')
                pyperclip.copy(data[website]["password"])
            except KeyError:
                messagebox.showinfo(title="Error", message="This website does "
                                                           "not exist in the data base.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    try:
        file = open("data.json", "r")
        file.close()
    except FileNotFoundError:
        file = open("data.json", "w")
        file.close()

    website = website_input.get()
    email = email_input.get()
    password = pass_input.get()

    data_array = [website, email, password]
    valid = True

    for value in data_array:
        if value == NONE or value == "":
            valid = False

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if valid:
        try:
            file = open("data.json", "r")
            data = json.load(file)
        except ValueError:
            file.close()
            file = open("data.json", "w")
            json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            file.close()
            file = open("data.json", "w")
            json.dump(data, file, indent=4)
        finally:
            file.close()
            website_input.delete(0, 'end')
            pass_input.delete(0, 'end')
    else:
        messagebox.showinfo(title="Error", message="Please do not leave "
                                                   "any of the fields empty!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0, sticky="w")

website_input = Entry(window, width=25)
website_input.grid(row=1, column=1, sticky="e")
website_input.focus()

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2, sticky="w")

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0, sticky="w")

email_input = Entry(window, width=43)
email_input.insert(0, "ilaymimon@gmail.com")
email_input.grid(row=2, column=1, columnspan=2, sticky="e", pady=2)

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0, sticky="w")

pass_input = Entry(window, width=25)
pass_input.grid(row=3, column=1, sticky="e")

generate_pass_button = Button(text="Generate Password", width=14, command=generate_pass)
generate_pass_button.grid(row=3, column=2, sticky="w")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="e")

window.mainloop()
