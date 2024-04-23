from tkinter import StringVar, constants, Entry
import tkinter as tk
from services.registry_service import registry


class LoginView:
    def __init__(self, root, handle_login, handle_show_create_user_view):
        self._root = root
        self._handle_login = handle_login
        self._handle_show_create_user_view = handle_show_create_user_view
        self._frame = None
        self._email_entry = None
        self._password_entry = None
        self._error_variable = None
        self._error_label = None

        self._initialize()

    def pack(self):
        if self._frame:
            self._frame.pack(fill=constants.X)

    def destroy(self):
        if self._frame:
            self._frame.destroy()

    def _login_handler(self):
        if self._email_entry is None or self._password_entry is None:
            return
        email = self._email_entry.get()
        password = self._password_entry.get()

        try:
            registry.log_in(email, password)
            self._handle_login()
        except PermissionError:
            self._show_error("Invalid email or password")

    def _show_error(self, message):
        if self._error_variable and self._error_label:
            self._error_variable.set(message)
            self._error_label.grid()

    def _hide_error(self):
        if self._error_label:
            self._error_label.grid_remove()

    def _initialize_email_field(self):
        email_label = tk.Label(master=self._frame, text="Email")

        self._email_entry = Entry(master=self._frame)

        email_label.grid(padx=5, pady=5, sticky=constants.W)
        self._email_entry.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_password_field(self):
        password_label = tk.Label(master=self._frame, text="Password")

        self._password_entry = tk.Entry(self._frame)

        password_label.grid(padx=5, pady=5, sticky=constants.W)
        self._password_entry.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize(self):
        self._frame = tk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)

        self._error_label = tk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(padx=5, pady=5)

        self._initialize_email_field()
        self._initialize_password_field()

        login_button = tk.Button(
            master=self._frame,
            text="Login",
            command=self._login_handler
        )

        create_user_button = tk.Button(
            master=self._frame,
            text="Create user",
            command=self._handle_show_create_user_view
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)

        login_button.grid(padx=5, pady=5, sticky=constants.EW)
        create_user_button.grid(padx=5, pady=5, sticky=constants.EW)

        self._hide_error()
