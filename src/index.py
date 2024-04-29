
from services.registry_service import RegistryService
from ui.commands import command_handler


def main():
    registry = RegistryService()
    while True:
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        user = registry.log_in(username, password)
        if user:
            print(f"Welcome {user}")
            break

        print("Invalid username or password")

    print("You are now logged in")

    while True:
        command = input("Enter a command: ").lower()
        command_handler(command, registry)


if __name__ == "__main__":
    main()
