
from db import member_repository, user_repository
from services.registry_service import RegistryService



def main():
    while True:
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        registry = RegistryService()
        user = registry.log_in(username, password)
        if user:
            print(f"Welcome {user}")
            break
        else:
            print("Invalid username or password")
    
    print("You are now logged in")

    while True:
        command = input("Enter a command: ")
        match command.lower():
            case "exit":
                print("Goodbye")
                break
            case "help":
                print("Help message")
            case "list members":
                print("List of members:")
                members = member_repository.get_all_members()
                for member in members:
                    print(member)
            case "update member":
                member = None
                while True:
                    id = input("Enter member ID: ")
                    member = member_repository.get_member_by_id(id)
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
                    member_repository.update_member(member.id, **{field: value})
                    print("Member updated")
                    
            case "log out":
                registry.log_out()
                print("You are now logged out")
            
            case "get member":
                while True:
                    id = input("Enter member ID: ")
                    member = member_repository.get_member_by_id(id)
                    if not member:
                        print("Invalid member ID")
                    else:
                        user = user_repository.get_user_by_id(member.user_id)
                        print(member)
                        print(user)
                        break

            case "delete member":
                while True:
                    id = input("Enter member ID: ")
                    member = member_repository.get_member_by_id(id)
                    if not member:
                        print("Invalid member ID")
                    else:
                        break
                confirm = input(f"Are you sure you want to delete {member}? (y/n): ")
                if confirm.lower() == "y":
                    try:
                        registry.delete_user(member.user_id)
                        print("Member deleted")
                    except Exception as e:
                        print(f"Error deleting member: {e}")

            case _:
                print("Unknown command")
    

if __name__ == "__main__":
    main()