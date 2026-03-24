import threading
import time

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.lock = threading.Lock()

def transfer(from_acc, to_acc, amount):
    thread_name = threading.current_thread().name

    # Determine lock order by account name to avoid deadlock
    first, second = (from_acc, to_acc) if from_acc.name < to_acc.name else (to_acc, from_acc)

    print(f"{thread_name} trying to lock {first.name}")
    with first.lock:
        print(f"{thread_name} locked {first.name}")
        time.sleep(0.1)  # optional delay for demonstration

        print(f"{thread_name} trying to lock {second.name}")
        with second.lock:
            print(f"{thread_name} locked {second.name}")

            # Critical section: transfer money
            if from_acc.balance >= amount:
                from_acc.balance -= amount
                to_acc.balance += amount
                print(f"{thread_name} transfer completed: {amount} from {from_acc.name} to {to_acc.name}")
            else:
                print(f"{thread_name} transfer failed: insufficient funds")

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