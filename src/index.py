
from repositories import user_repository
from services import user_service


def main():
    while True:
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        user = user_service.log_in(username, password)
        if user:
            print(f"Welcome {user}")
            break
        else:
            print("Invalid username or password")
    

if __name__ == "__main__":
    main()