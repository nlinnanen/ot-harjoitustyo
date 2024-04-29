

from services.registry_service import RegistryService


def list_users(registry: RegistryService):
    print("List of users:")
    users = registry.user_repository.get_all_users()
    for user in users:
        print(user)

def list_members(registry: RegistryService):
    print("List of members:")
    members = registry.member_repository.get_all_members()
    for member in members:
        print(member)

def create_user(registry: RegistryService):
    email = input("Enter email: ")
    password = input("Enter password: ")
    registry.add_user(
        email=email,
        password=password
    )
    print("User created")

def update_member(registry: RegistryService):
    member = None
    while True:
        member_id = input("Enter member ID: ")
        member = registry.member_repository.get_member_by_id(member_id)
        if not member:
            print("Invalid member ID")
        else:
            break

        print(f"Member {member}")

    while True:
        field = input("Enter field to update (empty to exit): ")
        if field == "":
            break

        if field not in member.__dict__:
            print("Invalid field")
            continue

        value = input("Enter new value: ")
        registry.member_repository.update_member(
            member.id, **{field: value})
        print("Member updated")


def log_in(registry: RegistryService):
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = registry.log_in(username, password)
    if user:
        print(f"Welcome {user}")
    else:
        print("Invalid username or password")
def log_out(registry: RegistryService):
    registry.log_out()
    print("You are now logged out")

def get_member(registry: RegistryService):
    while True:
        member_id = input("Enter member ID: ")
        member = registry.member_repository.get_member_by_id(int(member_id))
        if not member or member.user_id is None:
            print("Invalid member ID")
        else:
            user = registry.user_repository.get_user_by_id(
                int(member.user_id))
            print(member)
            print(user)
            break

def delete_member(registry: RegistryService):
    while True:
        member_id = input("Enter member ID: ")
        member = registry.member_repository.get_member_by_id(int(member_id))
        if not member:
            print("Invalid member ID")
        else:
            break

    confirm = input(
        f"Are you sure you want to delete {member}? (y/n): ")
    if confirm.lower() == "y" and member.id is not None:
        registry.delete_member(int(member.id))
        print("Member deleted")



def command_handler(command: str, registry: RegistryService):
    if command == "exit":
        print("Goodbye")
        exit()

    if command == "help":
        print("""
            Available commands:
                - list users
                - list members
                - create user
                - update member
                - log in
                - log out
                - get member
                - delete member
                - exit
            """)
    elif command == "list users":
        list_users(registry)
    elif command == "list members":
        list_members(registry)
    elif command == "create user":
        create_user(registry)
    elif command == "update member":
        update_member(registry)
    elif command == "log in":
        log_in(registry)
    elif command == "log out":
        log_out(registry)
    elif command == "get member":
        get_member(registry)
    elif command == "delete member":
        delete_member(registry)
    else:
        print("Unknown command. Type 'help' for a list of commands")
