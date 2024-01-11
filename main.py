from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_button():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
               'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    # password_list = []
    # for char in range(nr_letters):
    #     password_list.append(random.choice(letters))

    password_symbol = [random.choice(symbols) for _ in range(nr_symbols)]
    # password_list = []
    # for char in range(nr_symbols):
    #     password_list += random.choice(symbols)

    password_number = [random.choice(numbers) for _ in range(nr_numbers)]
    # password_list = []
    # for char in range(nr_numbers):
    #     password_list += random.choice(numbers)
    #
    password_list = password_letter + password_symbol + password_number

    random.shuffle(password_list)

    # 1
    password = "".join(password_list)
    # 2
    # password = ""
    # for char in password_list:
    #     password += char

    password_textbox.insert(index=0, string=password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    web_ans = web_textbox.get()
    user_ans = user_textbox.get()
    password_ans = password_textbox.get()
    new_dict = {
        web_ans: {
            "email": user_ans,
            "password": password_ans
        }
    }

    if len(web_ans) == 0 or len(password_ans) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            data_file = open("data.json", "r")
            # reading old data
            data = json.load(data_file)
        except FileNotFoundError:
            # writing new data
            with open("data.json", "w") as data_file:
                json.dump(new_dict, data_file, indent=4)
        else:
            # updating old data with new data
            data.update(new_dict)

            with open("data.json", "w") as data_file:
                # saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            web_textbox.delete(0, END)
            password_textbox.delete(0, END)

# ------------------------- SEARCHED PASSWORD -------------------------- #
def find_password():

    website = web_textbox.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=100)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(145, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
web_label = Label(text="Website:")
web_label.grid(column=0, row=1)
user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
web_textbox = Entry(width=18)
web_textbox.grid(column=1, row=1)
web_textbox.focus()

user_textbox = Entry(width=35)
user_textbox.grid(column=1, row=2, columnspan=2)
user_textbox.insert(0, "bbt7281@gmail.com")

password_textbox = Entry(width=18)
password_textbox.grid(column=1, row=3)

# Buttons
password_button = Button(text="Generate Password", command=generate_button, width=11)
password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=find_password, width=11)
search_button.grid(column=2, row=1)

window.mainloop()
