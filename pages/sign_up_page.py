#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import tkinter as tk
from tkinter import ttk, messagebox
import encryption_tools as et


class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        def process_sign_up() -> None:
            sign_up_password = sign_up_entry.get()
            confirm_sign_up_password = confirm_sign_up_entry.get()

            if len(sign_up_password) > 0 and sign_up_password == confirm_sign_up_password:
                controller.encryption_key = et.encrypt_master_password(sign_up_password)
                controller.db.add_master(controller.encryption_key.decode())
                controller.show_frame(controller.MainPage)
                sign_up_entry.delete(0, tk.END)
                confirm_sign_up_entry.delete(0, tk.END)
            elif len(sign_up_password) == 0 or len(confirm_sign_up_password) == 0:
                messagebox.showwarning("Warning", "Passwords' fields can't be blank.\n"
                                                  "Please write in matching passwords and try again.")
            else:
                messagebox.showwarning("Warning", "Passwords doesn't match.\n"
                                                  "Please write in matching passwords and try again.")

        sign_up_entry = ttk.Entry(self, show="*")
        confirm_sign_up_entry = ttk.Entry(self, show="*")

        for w in [sign_up_entry, confirm_sign_up_entry]:
            w.bind("<Control-c>", lambda e: "break")

        sign_up_message = tk.Label(self, text="Enter and confirm the password")

        sign_up_button = ttk.Button(self, text="Sign Up", default="active", command=process_sign_up)

        for w in self.winfo_children():
            w.bind("<Return>", (lambda event: process_sign_up()))

        sign_up_message.grid(row=0, column=2, columnspan=4, sticky="we")

        sign_up_entry.grid(row=1, column=3, columnspan=2, sticky="we")
        confirm_sign_up_entry.grid(row=2, column=3, columnspan=2, sticky="we")
        sign_up_button.grid(row=3, column=3, columnspan=2)

        for col in range(6):
            tk.Label(self, padx=9).grid(row=4, column=col, sticky="we")
