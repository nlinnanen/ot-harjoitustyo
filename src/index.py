
from repositories import user_repository


def main():
    print("Hello World")
    users = user_repository.get_all_users()
    print(users)

if __name__ == "__main__":
    main()