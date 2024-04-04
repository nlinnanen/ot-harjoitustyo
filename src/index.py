
from services.registry_service import RegistryService


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

    # TODO: Refactor this
    while True:
        command = input("Enter a command: ").lower()
        if command == "exit":
            print("Goodbye")
            break

        if command == "help":
            print("Help message")
        elif command == "list members":
            print("List of members:")
            members = registry.member_repository.get_all_members()
            for member in members:
                print(member)
        elif command == "update member":
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

        elif command == "log out":
            registry.log_out()
            print("You are now logged out")

        elif command == "get member":
            while True:
                member_id = input("Enter member ID: ")
                member = registry.member_repository.get_member_by_id(member_id)
                if not member:
                    print("Invalid member ID")
                else:
                    user = registry.user_repository.get_user_by_id(
                        member.user_id)
                    print(member)
                    print(user)
                    break

        elif command == "delete member":
            while True:
                member_id = input("Enter member ID: ")
                member = registry.member_repository.get_member_by_id(member_id)
                if not member:
                    print("Invalid member ID")
                else:
                    break

            confirm = input(
                f"Are you sure you want to delete {member}? (y/n): ")
            if confirm.lower() == "y":
                registry.delete_member(member.id)
                print("Member deleted")

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
