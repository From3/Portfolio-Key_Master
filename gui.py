#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import tkinter as tk
from tkinter import ttk, messagebox
from db import DataBase
import generator_tools as gt
import encryption_tools as et
from utils import icons, helper_text
import pyperclip
import webbrowser


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

        for F in (SignUpPage, LoginPage, MainPage, AddProfilePage, ChangePasswordPage):
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


##################################### Sign Up Page #####################################


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
                controller.show_frame(MainPage)
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


##################################### Login Page #####################################


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
                controller.show_frame(MainPage)
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


##################################### Main Page #####################################


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        style = ttk.Style(self)
        style.configure("lefttab.TNotebook", tabposition="wn")

        notebook = ttk.Notebook(self, style="lefttab.TNotebook")
        f1 = tk.Frame(notebook, width=225, height=90)
        f2 = tk.Frame(notebook, width=225, height=90)
        f3 = tk.Frame(notebook, width=225, height=90)
        f4 = tk.Frame(notebook, width=225, height=90)
        f5 = tk.Frame(notebook, width=225, height=90)
        notebook.add(f1, text=icons["Generator"])
        notebook.add(f2, text=icons["Manager"])
        notebook.add(f3, text=icons["Helper"])
        notebook.add(f4, text=icons["About"])
        notebook.add(f5, text=icons["Settings"])
        notebook.pack()

##################################### Generator #####################################

        def clear_check_text(*labels: tk.Label) -> None:
            if any([label["text"] for label in labels]):
                for label in labels:
                    label["text"] = ""

        def generate_password() -> None:
            clear_check_text(check_text, check_times_text)
            strings = [self.lowercase_var.get(), self.uppercase_var.get(), self.digits_var.get(),
                       self.punctuation_var.get()]
            generator_entry.delete(0, tk.END)
            generator_entry.insert(0, gt.generate(strings, length=length_list_var.get()))

        def check_password() -> None:
            clear_check_text(check_text, check_times_text)
            leaks_amount = gt.main_check(generator_entry.get())
            check_text["text"] = "Password leaked"
            check_times_text["text"] = f"{leaks_amount} time{'s' if leaks_amount != '1' else ''}"

        length_list = [num for num in range(6, 31)]
        length_list_var = tk.IntVar(value=15)
        length_menu = ttk.OptionMenu(f1, length_list_var, "15", *length_list)

        self.lowercase_var = tk.IntVar(value=1)
        lowercase_checkbox = ttk.Checkbutton(f1, text="lower case", cursor="hand2", variable=self.lowercase_var)

        self.uppercase_var = tk.IntVar(value=1)
        uppercase_checkbox = ttk.Checkbutton(f1, text="upper case", cursor="hand2", variable=self.uppercase_var)

        self.digits_var = tk.IntVar(value=1)
        digits_checkbox = ttk.Checkbutton(f1, text="digits", cursor="hand2", variable=self.digits_var)

        self.punctuation_var = tk.IntVar(value=0)
        punctuation_checkbox = ttk.Checkbutton(f1, text="punctuation", cursor="hand2", variable=self.punctuation_var)

        generator_entry = ttk.Entry(f1)
        generator_button = ttk.Button(f1, text="Generate", cursor="hand2", default="active", width=9,
                                      command=generate_password)
        checker_button = ttk.Button(f1, text="Check", cursor="hand2", width=9, command=check_password)

        check_text = tk.Label(f1)
        check_times_text = tk.Label(f1)

        tk.Label(f1, text="Length:").grid(row=0, column=0, columnspan=2)
        length_menu.grid(row=0, column=1, sticky="e")
        tk.Label(f1, padx=1).grid(row=0, column=2)
        lowercase_checkbox.grid(row=0, column=3, sticky="w")

        generator_entry.grid(row=1, column=0, columnspan=2)
        uppercase_checkbox.grid(row=1, column=3, sticky="w")

        generator_button.grid(row=2, column=0)
        checker_button.grid(row=2, column=1)
        digits_checkbox.grid(row=2, column=3, sticky="w")

        check_text.grid(row=3, column=0, columnspan=2)
        punctuation_checkbox.grid(row=3, column=3, sticky="wn")

        check_times_text.grid(row=4, column=0, columnspan=2)

##################################### Manager #####################################

        def refresh_profiles(event=None) -> None:
            tree.delete(*tree.get_children())
            for profile in controller.profiles.keys():
                tree.insert("", tk.END, values=(profile))

        def edit_profile() -> None:
            try:
                profile_name = str(tree.item(tree.focus())["values"][0])
                profile = controller.profiles[profile_name]
                add_profile_page = controller.frames[AddProfilePage]
                add_profile_page.profile_entry.insert(0, profile_name)
                add_profile_page.profile_entry.config(state="disabled")
                add_profile_page.username_entry.insert(0, profile["UserName"])
                add_profile_page.password_entry.insert(0, profile["Password"])
                controller.show_frame(AddProfilePage)
            except IndexError:  # happens when no row is selected
                pass

        def remove_profile() -> None:
            try:
                profile_name = str(tree.item(tree.focus())["values"][0])
                answer = messagebox.askyesno("Profiles removal", "Selected profile will be lost.\n"
                                                                 "Are you sure you want to continue?")
                if answer:
                    controller.profiles.pop(profile_name)
                    for profile in controller.db.get_profiles():
                        if et.decrypt_data(profile[1], controller.encryption_key) == profile_name:
                            controller.db.remove_profile(profile[1])
                    refresh_profiles()
            except IndexError:  # happens when no row is selected
                pass

        def do_popup(event) -> None:
            tree_row = tree.identify_row(event.y)
            if tree_row:
                tree.focus(tree_row)
                tree.selection_set(tree_row)
                profiles_menu.tk_popup(event.x_root, event.y_root)
            else:
                pass

        def copy_profile_info(key: str) -> None:
            profile_name = str(tree.item(tree.focus())["values"][0])
            profile_info = controller.profiles[profile_name][key]
            pyperclip.copy(profile_info)

        self.bind("<FocusIn>", refresh_profiles)

        columns = ("#1")
        tree = ttk.Treeview(f2, columns=columns, show="", selectmode="browse", height=5)
        tree.column("#1", minwidth=0, width=150, anchor="w")

        scrollbar = ttk.Scrollbar(f2, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        profiles_menu = tk.Menu(f2, tearoff=0)
        profiles_menu.add_command(label="Copy username", command=lambda: copy_profile_info("UserName"))
        profiles_menu.add_command(label="Copy password", command=lambda: copy_profile_info("Password"))
        profiles_menu.add_command(label="Edit profile", command=edit_profile)
        profiles_menu.add_command(label="Remove profile", command=remove_profile)

        tree.bind("<Button-3>", do_popup)

        add_button = ttk.Button(f2, text="Add", cursor="hand2", width=9,
                                command=lambda: controller.show_frame(AddProfilePage))
        edit_button = ttk.Button(f2, text="Edit", cursor="hand2", width=9, command=edit_profile)
        remove_button = ttk.Button(f2, text="Remove", cursor="hand2", width=9, command=remove_profile)
        logout_button = ttk.Button(f2, text="Logout", cursor="hand2", width=9,
                                   command=lambda: controller.show_frame(LoginPage))

        tree.grid(row=0, column=0, columnspan=2, rowspan=4, sticky="nsw")
        scrollbar.grid(row=0, column=2, rowspan=4, sticky="ns")
        add_button.grid(row=0, column=3, sticky="w")
        edit_button.grid(row=1, column=3, sticky="w")
        remove_button.grid(row=2, column=3, sticky="w")
        logout_button.grid(row=3, column=3, sticky="w")

##################################### Helper #####################################

        def update_text(event) -> None:
            section = event.widget.get()
            self.helper_text.set(helper_text[section][0])

        sections_list = [
            f"{icons['Generator']} Generator",
            f"{icons['Manager']} Manager",
            f"{icons['Settings']} Settings"
        ]

        sections_menu = ttk.Combobox(f3, values=sections_list, state="readonly")
        sections_menu.current(0)

        sections_menu.bind("<<ComboboxSelected>>", update_text)

        sections_menu.grid(row=0, column=0, columnspan=4, sticky="w")

        self.helper_text = tk.StringVar()
        self.helper_text.set(helper_text[f"{icons['Generator']} Generator"][0])
        helper_text_field = tk.Label(f3, textvariable=self.helper_text)
        helper_text_field.grid(row=1, column=0, columnspan=4, rowspan=4, sticky="w")

##################################### About #####################################

        def callback(url: str) -> None:
            webbrowser.open_new(url)

        author_info = tk.Label(f4, text="\n  Created by Deividas Jakubauskas", padx=21)
        github_hyperlink = tk.Label(f4, text="  Github", fg="blue", cursor="hand2")

        github_hyperlink.bind("<Button-1>", lambda e: callback("https://github.com/From3"))

        author_info.grid(row=0, column=0, columnspan=6, rowspan=2)
        github_hyperlink.grid(row=3, column=0, columnspan=6)

##################################### Settings #####################################

        def change_topmost() -> None:
            # keep the app on top when raising other windows
            controller.attributes("-topmost", bool(self.keep_on_top_var.get()))

        def remove_data() -> None:
            answer = messagebox.askyesno("Remove all profiles", "All current profiles will be lost.\n"
                                                                "Are you sure you want to continue?")
            if answer:
                controller.db.db_operation("DELETE FROM profiles")
                controller.profiles.clear()
                refresh_profiles()

        self.keep_on_top_var = tk.IntVar(value=0)
        keep_on_top_checkbox = ttk.Checkbutton(f5, text="keep on top", cursor="hand2", variable=self.keep_on_top_var,
                                               command=change_topmost)

        change_password_button = ttk.Button(f5, text="Change Password", cursor="hand2",
                                            command=lambda: controller.show_frame(ChangePasswordPage))
        remove_profiles_button = ttk.Button(f5, text="Remove all Profiles", cursor="hand2", width=19,
                                            command=remove_data)

        for col in range(6):
            tk.Label(f5, padx=16).grid(row=0, column=col, sticky="we")
        keep_on_top_checkbox.grid(row=1, column=0, columnspan=3, sticky="we")
        change_password_button.grid(row=2, column=0, columnspan=3, sticky="we")
        remove_profiles_button.grid(row=3, column=0, columnspan=3, sticky="we")


##################################### Add Manager Profile #####################################


class AddProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        def finish_add_profile(profile: str, username: str, password: str) -> None:
            controller.profiles[profile] = {"UserName": username, "Password": password}
            for entry_field in [self.profile_entry, self.username_entry, self.password_entry]:
                entry_field.delete(0, tk.END)
            controller.show_frame(MainPage)

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
            controller.show_frame(MainPage)

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


##################################### Change Password Page #####################################


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

                controller.show_frame(MainPage)
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
                                   command=lambda: controller.show_frame(MainPage))

        tk.Label(self).grid(row=0, column=0)
        tk.Label(self, text="Current Password").grid(row=1, column=0, sticky="e")
        current_password_entry.grid(row=1, column=1, columnspan=2)
        tk.Label(self, text="New Password").grid(row=2, column=0, sticky="e")
        new_password_entry.grid(row=2, column=1, columnspan=2)
        tk.Label(self, text="Confirm Password").grid(row=3, column=0, sticky="e")
        confirm_password_entry.grid(row=3, column=1, columnspan=2)
        confirm_button.grid(row=4, column=1)
        cancel_button.grid(row=4, column=2)


##################################### Main Loop #####################################


if __name__ == "__main__":
    app = App()
    app.resizable(width=False, height=False)
    app.title("KeyMaster")
    app.mainloop()
