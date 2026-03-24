import threading
import time

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.lock = threading.Lock()

def transfer(from_acc, to_acc, amount):
    thread_name = threading.current_thread().name
    print(f"{thread_name} trying to lock FROM {from_acc.name}")
    with from_acc.lock:
        print(f"{thread_name} locked FROM {from_acc.name}")

        # Delay to increase deadlock chance
        time.sleep(0.1)

        print(f"{thread_name} trying to lock TO {to_acc.name}")
        with to_acc.lock:
            print(f"{thread_name} locked TO {to_acc.name}")

            # Critical section
            from_acc.balance -= amount
            to_acc.balance += amount

            print(f"{thread_name} transfer completed")

def main():
    account1 = Account("Account-1", 1000)
    account2 = Account("Account-2", 1000)

    t1 = threading.Thread(target=transfer, args=(account1, account2, 100), name="Thread-1")
    t2 = threading.Thread(target=transfer, args=(account2, account1, 200), name="Thread-2")

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Final balance: {account1.name} = {account1.balance}, {account2.name} = {account2.balance}")

if __name__ == "__main__":
    main()