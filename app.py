#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import tkinter as tk
from database import DataBase
from pages.sign_up_page import SignUpPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.add_profile_page import AddProfilePage
from pages.change_password_page import ChangePasswordPage


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        main_frame = tk.Frame(self)
        main_frame.grid(column=0, row=0, columnspan=3, rowspan=2)

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.db = DataBase()
        self.db.start()

        self.encryption_key = None
        self.profiles = {}

        self.frames = {}

        self.SignUpPage = SignUpPage
        self.LoginPage = LoginPage
        self.MainPage = MainPage
        self.AddProfilePage = AddProfilePage
        self.ChangePasswordPage = ChangePasswordPage

        for F in (self.SignUpPage, self.LoginPage, self.MainPage, self.AddProfilePage, self.ChangePasswordPage):
            frame = F(main_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        if self.db.is_master():
            self.show_frame(LoginPage)
        else:
            self.show_frame(SignUpPage)

    def show_frame(self, cont) -> None:
        frame = self.frames[cont]
        frame.focus()
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.resizable(width=False, height=False)
    app.title("KeyMaster")
    app.mainloop()
