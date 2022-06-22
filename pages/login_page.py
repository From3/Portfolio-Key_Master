#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import tkinter as tk
from tkinter import ttk, messagebox
import encryption_tools as et


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        def process_login() -> None:
            master = controller.db.get_master().encode()
            provided_master = et.encrypt_master_password(login_entry.get())

            if provided_master == master:
                controller.encryption_key = provided_master
                for profile in controller.db.get_profiles():
                    controller.profiles[et.decrypt_data(profile[1], controller.encryption_key)] = {
                        "UserName": et.decrypt_data(profile[2], controller.encryption_key),
                        "Password": et.decrypt_data(profile[3], controller.encryption_key)
                    }
                controller.show_frame(controller.MainPage)
            else:
                messagebox.showwarning("Warning", "Incorrect password.\nTry again.")
            login_entry.delete(0, tk.END)

        login_message = tk.Label(self, text="Enter the password", padx=18)

        login_entry = ttk.Entry(self, show="*")
        login_entry.bind("<Control-c>", lambda e: "break")

        login_button = ttk.Button(self, text="Login", default="active", command=process_login)

        for w in self.winfo_children():
            w.bind("<Return>", (lambda event: process_login()))

        login_message.grid(row=0, column=3, columnspan=2, sticky="we")

        login_entry.grid(row=1, column=3, columnspan=2, sticky="we")
        login_button.grid(row=2, column=3, columnspan=2)

        for col in range(6):
            tk.Label(self, padx=9).grid(row=3, column=col, sticky="we")
