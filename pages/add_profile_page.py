#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import tkinter as tk
from tkinter import ttk, messagebox
import encryption_tools as et


class AddProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        def finish_add_profile(profile: str, username: str, password: str) -> None:
            controller.profiles[profile] = {"UserName": username, "Password": password}
            for entry_field in [self.profile_entry, self.username_entry, self.password_entry]:
                entry_field.delete(0, tk.END)
            controller.show_frame(controller.MainPage)

        def add_profile() -> None:
            profile = self.profile_entry.get()
            username = self.username_entry.get()
            password = self.password_entry.get()
            if len(profile) and profile not in controller.profiles.keys():
                controller.db.add_profile(
                    et.encrypt_data(profile, controller.encryption_key),
                    et.encrypt_data(username, controller.encryption_key),
                    et.encrypt_data(password, controller.encryption_key)
                )
                finish_add_profile(profile, username, password)
            elif not len(profile):
                messagebox.showwarning("Warning", "Profile name field can't be blank.\n"
                                                  "Please write in a profile name and try again.")
            elif profile in controller.profiles.keys():
                if self.profile_entry["state"] == "normal":
                    answer = messagebox.askyesno("Profile exists", "Profile with this name already exists "
                                                                   "and will be overwritten. Do you want "
                                                                   "to continue?")
                    if answer:
                        controller.db.change_profile(profile, username, password)
                        finish_add_profile(profile, username, password)
                else:
                    controller.db.change_profile(profile, username, password)
                    self.profile_entry.config(state="normal")
                    finish_add_profile(profile, username, password)

        def cancel_add_profile() -> None:
            self.profile_entry.config(state="normal")
            for entry_field in [self.profile_entry, self.username_entry, self.password_entry]:
                entry_field.delete(0, tk.END)
            controller.show_frame(controller.MainPage)

        self.profile_entry = ttk.Entry(self)
        self.username_entry = ttk.Entry(self)
        self.password_entry = ttk.Entry(self, show="*")
        confirm_button = ttk.Button(self, text="Confirm", cursor="hand2", width=9, command=add_profile)
        cancel_button = ttk.Button(self, text="Cancel", cursor="hand2", width=9,
                                   command=cancel_add_profile)

        tk.Label(self).grid(row=0, column=0)
        tk.Label(self, text="Profile name").grid(row=1, column=0, sticky="e")
        self.profile_entry.grid(row=1, column=1, columnspan=2)
        tk.Label(self, text="Username").grid(row=2, column=0, sticky="e")
        self.username_entry.grid(row=2, column=1, columnspan=2)
        tk.Label(self, text="Password").grid(row=3, column=0, sticky="e")
        self.password_entry.grid(row=3, column=1, columnspan=2)
        confirm_button.grid(row=4, column=1)
        cancel_button.grid(row=4, column=2)
