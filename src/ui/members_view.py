from tkinter import ttk, constants
from typing import Generator
from entities.member import Member
from services.registry_service import registry


class MemberListView:
    def __init__(self, root, members: Generator[Member, None, None]):
        self._root = root
        self._members = members
        self._frame = None

        self._initialize()

    def pack(self):
        if self._frame:
            self._frame.pack(fill=constants.X)

    def destroy(self):
        if self._frame:
            self._frame.destroy()

    def _initialize_member_item(self, member: Member):
        item_frame = ttk.Frame(master=self._frame)
        label = ttk.Label(master=item_frame, text=member.get_full_name())

        label.grid(row=0, column=0, padx=5, pady=5, sticky=constants.W)

        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.pack(fill=constants.X)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        for member in self._members:
            self._initialize_member_item(member)


class MembersView:
    def __init__(self, root, handle_logout):
        self._root = root
        self._handle_logout = handle_logout
        self._user = registry.get_current_user()
        self._frame = None
        self._create_member_entries = {}
        self._member_list_frame = None
        self._member_list_view = None

        self._initialize()

    def pack(self):
        if self._frame:
            self._frame.pack(fill=constants.X)

    def destroy(self):
        if self._frame:
            self._frame.destroy()

    def _logout_handler(self):
        registry.log_out()
        self._handle_logout()

    def _initialize_member_list(self):
        if self._member_list_view:
            self._member_list_view.destroy()

        members = registry.get_all_members()

        self._member_list_view = MemberListView(
            self._member_list_frame,
            members
        )

        self._member_list_view.pack()

    def _initialize_header(self):
        if self._user is None:
            raise PermissionError("You must be logged in to view this page")

        user_label = ttk.Label(
            master=self._frame,
            text=f"Logged in as {self._user.email}"
        )

        logout_button = ttk.Button(
            master=self._frame,
            text="Logout",
            command=self._logout_handler
        )

        user_label.grid(row=0, column=0, padx=5, pady=5, sticky=constants.W)

        logout_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.EW
        )

    def _handle_create_member(self):
        member_contents = {key: entry.get()
                           for key, entry in self._create_member_entries.items()}
        if all(member_contents.values()):
            registry.add_member(**member_contents)
            self._initialize_member_list()
            for entry in self._create_member_entries.values():
                entry.delete(0, constants.END)
        else:
            # TODO: Show error message
            print("All fields are required")

    def _initialize_footer(self):
        self._create_member_entries = {key: ttk.Entry(
            master=self._frame) for key in Member.__dict__}

        create_member_button = ttk.Button(
            master=self._frame,
            text="Create",
            command=self._handle_create_member
        )

        for index, (key, entry) in enumerate(self._create_member_entries.items()):
            label = ttk.Label(master=self._frame, text=key)
            entry.grid(row=index + 1, column=0, padx=5,
                       pady=5, sticky=constants.EW)
            label.grid(row=index + 1, column=1, padx=5,
                       pady=5, sticky=constants.W)

        create_member_button.grid(
            row=len(self._create_member_entries) + 1,
            column=0,
            padx=5,
            pady=5,
            sticky=constants.EW
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._member_list_frame = ttk.Frame(master=self._frame)

        self._initialize_header()
        self._initialize_member_list()
        self._initialize_footer()

        self._member_list_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=constants.EW
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=400)
        self._frame.grid_columnconfigure(1, weight=0)
