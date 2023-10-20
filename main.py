import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import os

class Contact:
    def __init__(self, name, phone, email, address, image_path=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.image_path = image_path

class ContactManager:
    def __init__(self):
        self.contacts = []

        self.window = ThemedTk(theme="arc")
        self.window.title("Contact Manager")

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_label = ttk.Label(self.window, text="Contact Manager", font=('Helvetica', 20, 'bold'))
        header_label.grid(row=0, column=0, columnspan=5, pady=10, sticky="n")

        # Center the header label
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Contact Details
        ttk.Label(self.window, text="Name:").grid(row=1, column=0, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.window)
        self.name_entry.grid(row=1, column=1, pady=5, columnspan=3)

        ttk.Label(self.window, text="Phone:").grid(row=2, column=0, pady=5, sticky="e")
        self.phone_entry = ttk.Entry(self.window)
        self.phone_entry.grid(row=2, column=1, pady=5, columnspan=3)

        ttk.Label(self.window, text="Email:").grid(row=3, column=0, pady=5, sticky="e")
        self.email_entry = ttk.Entry(self.window)
        self.email_entry.grid(row=3, column=1, pady=5, columnspan=3)

        ttk.Label(self.window, text="Address:").grid(row=4, column=0, pady=5, sticky="e")
        self.address_entry = ttk.Entry(self.window)
        self.address_entry.grid(row=4, column=1, pady=5, columnspan=3)

        # Image
        self.image_path = tk.StringVar()
        ttk.Label(self.window, text="Image:").grid(row=5, column=0, pady=5, sticky="e")
        self.image_entry = ttk.Entry(self.window, textvariable=self.image_path, state="readonly")
        self.image_entry.grid(row=5, column=1, pady=5, columnspan=2)
        ttk.Button(self.window, text="Browse", command=self.browse_image).grid(row=5, column=3, pady=5)

        # Buttons for actions
        ttk.Button(self.window, text="Add Contact", command=self.add_contact).grid(row=6, column=0, pady=10)
        ttk.Button(self.window, text="View Contacts", command=self.view_contacts).grid(row=6, column=1, pady=10)
        ttk.Button(self.window, text="Search Contact", command=self.search_contact).grid(row=6, column=2, pady=10)
        ttk.Button(self.window, text="Update Contact", command=self.update_contact).grid(row=6, column=3, pady=10)
        ttk.Button(self.window, text="Delete Contact", command=self.delete_contact).grid(row=6, column=4, pady=10)

        # Contact List
        self.contact_listbox = tk.Listbox(self.window, selectbackground="#546e7a", selectforeground="#ffffff", font=('Helvetica', 12), height=10)
        self.contact_listbox.grid(row=7, column=0, columnspan=5, pady=10)
        self.contact_listbox.bind('<Double-Button-1>', self.view_contact_details)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.image_path.set(file_path)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        image_path = self.image_path.get()

        if name and phone:
            contact = Contact(name, phone, email, address, image_path)
            self.contacts.append(contact)
            self.update_contact_listbox()
            self.clear_entries()
            messagebox.showinfo("Success", "Contact added successfully.")
        else:
            messagebox.showwarning("Error", "Name and Phone are required.")

    def view_contacts(self):
        view_window = tk.Toplevel(self.window)
        view_window.title("Contact List")

        for i, contact in enumerate(self.contacts, 1):
            contact_info = f"{i}. Name: {contact.name}, Phone: {contact.phone}"
            ttk.Label(view_window, text=contact_info).pack(pady=5)

    def search_contact(self):
        search_window = tk.Toplevel(self.window)
        search_window.title("Search Contact")

        ttk.Label(search_window, text="Search by Name or Phone:").pack(pady=5)
        search_entry = ttk.Entry(search_window)
        search_entry.pack(pady=5)

        ttk.Button(search_window, text="Search", command=lambda: self.display_search_result(search_entry.get())).pack(pady=10)

    def display_search_result(self, query):
        search_result_window = tk.Toplevel(self.window)
        search_result_window.title("Search Result")

        found = False
        for i, contact in enumerate(self.contacts, 1):
            if query.lower() in contact.name.lower() or query in contact.phone:
                contact_info = f"{i}. Name: {contact.name}, Phone: {contact.phone}, Email: {contact.email}, Address: {contact.address}"
                ttk.Label(search_result_window, text=contact_info).pack(pady=5)
                found = True

        if not found:
            messagebox.showinfo("Search Result", "No matching contacts found.")

    def update_contact(self):
        update_window = tk.Toplevel(self.window)
        update_window.title("Update Contact")

        ttk.Label(update_window, text="Enter Phone Number of Contact to Update:").pack(pady=5)
        update_entry = ttk.Entry(update_window)
        update_entry.pack(pady=5)

        ttk.Button(update_window, text="Update", command=lambda: self.perform_update(update_entry.get())).pack(pady=10)

    def perform_update(self, phone):
        for contact in self.contacts:
            if phone == contact.phone:
                update_window = tk.Toplevel(self.window)
                update_window.title("Update Contact")

                ttk.Label(update_window, text=f"Updating Contact: {contact.name}").pack(pady=5)

                ttk.Label(update_window, text="New Name:").pack(pady=5)
                new_name_entry = ttk.Entry(update_window)
                new_name_entry.pack(pady=5)

                ttk.Label(update_window, text="New Phone:").pack(pady=5)
                new_phone_entry = ttk.Entry(update_window)
                new_phone_entry.pack(pady=5)

                ttk.Label(update_window, text="New Email:").pack(pady=5)
                new_email_entry = ttk.Entry(update_window)
                new_email_entry.pack(pady=5)

                ttk.Label(update_window, text="New Address:").pack(pady=5)
                new_address_entry = ttk.Entry(update_window)
                new_address_entry.pack(pady=5)

                ttk.Button(update_window, text="Confirm Update", command=lambda: self.confirm_update(contact, new_name_entry.get(),
                                                                                                new_phone_entry.get(), new_email_entry.get(),
                                                                                                new_address_entry.get())).pack(pady=10)
                return
        messagebox.showinfo("Error", "Contact not found.")

    def confirm_update(self, contact, new_name, new_phone, new_email, new_address):
        contact.name = new_name if new_name else contact.name
        contact.phone = new_phone if new_phone else contact.phone
        contact.email = new_email if new_email else contact.email
        contact.address = new_address if new_address else contact.address

        messagebox.showinfo("Success", "Contact updated successfully.")
        self.update_contact_listbox()

    def delete_contact(self):
        delete_window = tk.Toplevel(self.window)
        delete_window.title("Delete Contact")

        ttk.Label(delete_window, text="Enter Phone Number of Contact to Delete:").pack(pady=5)
        delete_entry = ttk.Entry(delete_window)
        delete_entry.pack(pady=5)

        ttk.Button(delete_window, text="Delete", command=lambda: self.perform_delete(delete_entry.get())).pack(pady=10)

    def perform_delete(self, phone):
        for i, contact in enumerate(self.contacts):
            if phone == contact.phone:
                del self.contacts[i]
                messagebox.showinfo("Success", "Contact deleted successfully.")
                self.update_contact_listbox()
                return
        messagebox.showinfo("Error", "Contact not found.")

    def view_contact_details(self, event):
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            contact = self.contacts[index]

            details_window = tk.Toplevel(self.window)
            details_window.title("Contact Details")

            ttk.Label(details_window, text=f"Name: {contact.name}", font=('Helvetica', 14, 'bold')).pack(pady=5)

            ttk.Label(details_window, text=f"Phone: {contact.phone}").pack(pady=5)
            ttk.Label(details_window, text=f"Email: {contact.email}").pack(pady=5)
            ttk.Label(details_window, text=f"Address: {contact.address}").pack(pady=5)

            if contact.image_path:
                image = Image.open(contact.image_path)
                image = image.resize((150, 150), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)
                ttk.Label(details_window, image=photo).pack(pady=10)
                ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
            else:
                ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)

    def update_contact_listbox(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_listbox.insert(tk.END, f"{contact.name} - {contact.phone}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.image_path.set("")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    contact_manager = ContactManager()
    contact_manager.run()
