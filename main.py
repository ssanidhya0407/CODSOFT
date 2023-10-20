import random
import string
import tkinter as tk
from tkinter import ttk
import pyperclip

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_password_clicked():
    try:
        length = int(length_entry.get())

        if length <= 0:
            result_label.config(text="Please enter a valid positive length.", foreground="red")
            return

        password = generate_password(length)
        result_label.config(text="Generated Password: {}".format(password), foreground="green")
        copy_button.config(state="normal")  # Enable the copy button

        # Store the generated password in a global variable for copying
        global generated_password
        generated_password = password

    except ValueError:
        result_label.config(text="Please enter a valid numeric length.", foreground="red")

def copy_password():
    pyperclip.copy(generated_password)
    result_label.config(text="Password copied to clipboard!", foreground="blue")

# Create the main window
window = tk.Tk()
window.title("Password Generator")

# Create and configure widgets
length_label = ttk.Label(window, text="Enter the desired length of the password:")
length_entry = ttk.Entry(window)
generate_button = ttk.Button(window, text="Generate Password", command=generate_password_clicked)
copy_button = ttk.Button(window, text="Copy to Clipboard", command=copy_password, state="disabled")
result_label = ttk.Label(window, text="")

# Place widgets in the grid
length_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
length_entry.grid(row=0, column=1, padx=10, pady=10)
generate_button.grid(row=1, column=0, pady=10)
copy_button.grid(row=1, column=1, pady=10)
result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Start the main event loop
window.mainloop()
