from tkinter import ttk, StringVar, constants

from services.registry_service import registry, EmailExistsError


class CreateUserView:
    """Käyttäjän rekisteröitymisestä vastaava näkymä."""

    def __init__(self, root, handle_create_user, handle_show_login_view):
        """Luokan konstruktori. Luo uuden rekisteröitymisnäkymän.

        Args:
            root:
                TKinter-elementti, jonka sisään näkymä alustetaan.
            handle_create_user:
                Kutsuttava-arvo, jota kutsutaan kun käyttäjä luodaan. Saa argumentteina käyttäjätunnuksen ja salasanan.
            handle_show_login_view:
                Kutsuttava-arvo, jota kutsutaan kun siirrytään kirjautumisnäkymään.
        """
        self._root = root
        self._handle_create_user = handle_create_user
        self._handle_show_login_view = handle_show_login_view
        self._frame = None
        self._email_entry = None
        self._password_entry = None
        self._error_variable = None
        self._error_label = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X) # type: ignore

    def destroy(self):
        self._frame.destroy() # type: ignore

    def _create_user_handler(self):
        email = self._email_entry.get() # type: ignore
        password = self._password_entry.get() # type: ignore

        if len(email) == 0 or len(password) == 0:
            self._show_error("email and password is required")
            return

        try:
            registry.add_user(email, password)
            self._handle_create_user()
        except EmailExistsError:
            self._show_error(f"email {email} already exists")

    def _show_error(self, message):
        self._error_variable.set(message) # type: ignore
        self._error_label.grid() # type: ignore

    def _hide_error(self):
        self._error_label.grid_remove() # type: ignore

    def _initialize_email_field(self):
        email_label = ttk.Label(master=self._frame, text="email")

        self._email_entry = ttk.Entry(master=self._frame)

        email_label.grid(padx=5, pady=5, sticky=constants.W)
        self._email_entry.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_password_field(self):
        password_label = ttk.Label(master=self._frame, text="Password")

        self._password_entry = ttk.Entry(master=self._frame)

        password_label.grid(padx=5, pady=5, sticky=constants.W)
        self._password_entry.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground="red"
        )

        self._error_label.grid(padx=5, pady=5)

        self._initialize_email_field()
        self._initialize_password_field()

        create_user_button = ttk.Button(
            master=self._frame,
            text="Create",
            command=self._create_user_handler
        )

        login_button = ttk.Button(
            master=self._frame,
            text="Login",
            command=self._handle_show_login_view
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)

        create_user_button.grid(padx=5, pady=5, sticky=constants.EW)
        login_button.grid(padx=5, pady=5, sticky=constants.EW)

        self._hide_error()
