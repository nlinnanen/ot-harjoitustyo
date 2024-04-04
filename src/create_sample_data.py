

from multiprocessing import Process, Queue
from faker import Faker
import queue  # For catching the Empty exception

from db.member_repository import MemberRepository
from db.user_repository import UserRepository
from db import conn, create_db_conn

fake = Faker(locale='fi_FI')
task_queue = Queue()

N = 10000


def create_sample_user(user_repository: UserRepository):
    return user_repository.add_user(
        email=fake.email(),
        password="password"
    )


def create_sample_member(member_repository: MemberRepository, user_id: str):
    member_repository.add_member(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        start_year=fake.year(),
        member_until=fake.date_between(
            start_date='-5y', end_date='+1y').isoformat(),
        home_municipality=fake.city(),
        user_id=user_id
    )


def create_sample_data(i: int, user_repository: UserRepository, member_repository: MemberRepository):
    print(f"Creating sample data for user {i}/{N}")
    user_id = create_sample_user(user_repository)
    create_sample_member(member_repository, user_id)


def process_function(task_queue):
    with create_db_conn() as conn:
        user_repository = UserRepository(db_conn=conn)
        member_repository = MemberRepository(db_conn=conn)

        while True:
            try:
                # Instead of get_nowait(), use get() with a timeout
                i = task_queue.get(timeout=1)  # Adjust timeout as necessary
            except queue.Empty:
                break  # Exit loop if queue is empty
            else:
                create_sample_data(i, user_repository, member_repository)
                # No task_done() call is needed here


def main_process():
    task_queue = Queue()

    confirmation = input("Do you want to empty the database? (y/n): ")
    if confirmation.lower() == "y":
        delete_db_contents()
        print("Database emptied.")
    else:
        print("Database not emptied.")

    for i in range(N):
        task_queue.put(i)

    num_processes = 30  # Adjust based on your task and system capabilities

    processes = []
    for _ in range(num_processes):
        p = Process(target=process_function, args=(task_queue,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    main_process()
