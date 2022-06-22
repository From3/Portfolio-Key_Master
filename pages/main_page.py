#!/usr/bin/env python3
# -*- coding: utf-8 -*- #

import pyperclip
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from utils import icons, helper_text
import generator_tools as gt
import encryption_tools as et


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

# ----------------------------- Generator -----------------------------

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

# ----------------------------- Manager -----------------------------

        def refresh_profiles(event=None) -> None:
            tree.delete(*tree.get_children())
            for profile in controller.profiles.keys():
                tree.insert("", tk.END, values=profile)

        def edit_profile() -> None:
            try:
                profile_name = str(tree.item(tree.focus())["values"][0])
                profile = controller.profiles[profile_name]
                add_profile_page = controller.frames[controller.AddProfilePage]
                add_profile_page.profile_entry.insert(0, profile_name)
                add_profile_page.profile_entry.config(state="disabled")
                add_profile_page.username_entry.insert(0, profile["UserName"])
                add_profile_page.password_entry.insert(0, profile["Password"])
                controller.show_frame(controller.AddProfilePage)
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
                                command=lambda: controller.show_frame(controller.AddProfilePage))
        edit_button = ttk.Button(f2, text="Edit", cursor="hand2", width=9, command=edit_profile)
        remove_button = ttk.Button(f2, text="Remove", cursor="hand2", width=9, command=remove_profile)
        logout_button = ttk.Button(f2, text="Logout", cursor="hand2", width=9,
                                   command=lambda: controller.show_frame(controller.LoginPage))

        tree.grid(row=0, column=0, columnspan=2, rowspan=4, sticky="nsw")
        scrollbar.grid(row=0, column=2, rowspan=4, sticky="ns")
        add_button.grid(row=0, column=3, sticky="w")
        edit_button.grid(row=1, column=3, sticky="w")
        remove_button.grid(row=2, column=3, sticky="w")
        logout_button.grid(row=3, column=3, sticky="w")

# ----------------------------- Helper -----------------------------

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

# ----------------------------- About -----------------------------

        def callback(url: str) -> None:
            webbrowser.open_new(url)

        author_info = tk.Label(f4, text="\n  Created by Deividas Jakubauskas", padx=21)
        github_hyperlink = tk.Label(f4, text="  Github", fg="blue", cursor="hand2")

        github_hyperlink.bind("<Button-1>", lambda e: callback("https://github.com/From3"))

        author_info.grid(row=0, column=0, columnspan=6, rowspan=2)
        github_hyperlink.grid(row=3, column=0, columnspan=6)

# ----------------------------- Settings -----------------------------

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
                                            command=lambda: controller.show_frame(controller.ChangePasswordPage))
        remove_profiles_button = ttk.Button(f5, text="Remove all Profiles", cursor="hand2", width=19,
                                            command=remove_data)

        for col in range(6):
            tk.Label(f5, padx=16).grid(row=0, column=col, sticky="we")
        keep_on_top_checkbox.grid(row=1, column=0, columnspan=3, sticky="we")
        change_password_button.grid(row=2, column=0, columnspan=3, sticky="we")
        remove_profiles_button.grid(row=3, column=0, columnspan=3, sticky="we")
