#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import tkinter as tk
from tkinter import ttk, messagebox
import encryption_tools as et


class ChangePasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        def change_password() -> None:
            current_password = current_password_entry.get()
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()

            master = controller.db.get_master().encode()
            provided_master = et.encrypt_master_password(current_password)

            if master == provided_master and new_password and new_password == confirm_password:
                controller.encryption_key = et.encrypt_master_password(new_password)
                controller.db.change_master(controller.encryption_key.decode())

                controller.db.db_operation("DELETE FROM profiles")
                for profile_name in controller.profiles.keys():
                    controller.db.add_profile(
                        et.encrypt_data(profile_name, controller.encryption_key),
                        et.encrypt_data(controller.profiles[profile_name]["UserName"], controller.encryption_key),
                        et.encrypt_data(controller.profiles[profile_name]["Password"], controller.encryption_key)
                    )

                controller.show_frame(controller.MainPage)
                for entry_field in [current_password_entry, new_password_entry, confirm_password_entry]:
                    entry_field.delete(0, tk.END)
                messagebox.showinfo("Success", "Your password was changed successfully!")
            elif master != provided_master:
                messagebox.showwarning("Warning", "Please write in your current password correctly and try again.")
            elif not new_password:
                messagebox.showwarning("Warning", "Please write in your new password and try again.")
            elif master == new_password:
                messagebox.showwarning("Warning", "Please write in a different new password and try again.")
            elif new_password != confirm_password:
                messagebox.showwarning("Warning", "Passwords doesn't match.\n"
                                                  "Please write in matching passwords and try again.")

        current_password_entry = ttk.Entry(self, show="*")
        new_password_entry = ttk.Entry(self, show="*")
        confirm_password_entry = ttk.Entry(self, show="*")
        confirm_button = ttk.Button(self, text="Confirm", cursor="hand2", width=9, command=change_password)
        cancel_button = ttk.Button(self, text="Cancel", cursor="hand2", width=9,
                                   command=lambda: controller.show_frame(controller.MainPage))

        tk.Label(self).grid(row=0, column=0)
        tk.Label(self, text="Current Password").grid(row=1, column=0, sticky="e")
        current_password_entry.grid(row=1, column=1, columnspan=2)
        tk.Label(self, text="New Password").grid(row=2, column=0, sticky="e")
        new_password_entry.grid(row=2, column=1, columnspan=2)
        tk.Label(self, text="Confirm Password").grid(row=3, column=0, sticky="e")
        confirm_password_entry.grid(row=3, column=1, columnspan=2)
        confirm_button.grid(row=4, column=1)
        cancel_button.grid(row=4, column=2)
