
import csv
import os
from datetime import datetime

ACCOUNT_FILE = "accounts.csv"
TRANSACTION_FILE = "transactions.csv"


def setup_files():
    if not os.path.exists(ACCOUNT_FILE):
        with open(ACCOUNT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["account_no", "name", "pin", "balance"])

    if not os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["date", "account_no", "type", "amount", "balance"]
            )


def load_accounts():
    with open(ACCOUNT_FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


def save_accounts(accounts):
    with open(ACCOUNT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["account_no", "name", "pin", "balance"]
        )
        writer.writeheader()
        writer.writerows(accounts)


def log_transaction(account_no, transaction_type, amount, balance):
    with open(TRANSACTION_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            account_no,
            transaction_type,
            f"{amount:.2f}",
            f"{balance:.2f}"
        ])


def create_account():
    accounts = load_accounts()

    print("\n--- Create Account ---")
    name = input("Enter account holder name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    while True:
        pin = input("Create a 4-digit demo PIN: ")
        if pin.isdigit() and len(pin) == 4:
            break
        print("PIN must contain exactly 4 digits.")

    account_no = str(
        max([int(a["account_no"]) for a in accounts], default=1000) + 1
    )

    account = {
        "account_no": account_no,
        "name": name,
        "pin": pin,
        "balance": "0.00"
    }

    accounts.append(account)
    save_accounts(accounts)

    print("\nAccount created successfully!")
    print("Account Number:", account_no)
    print("Account Holder:", name)
    print("Opening Balance: Rs. 0.00")


def find_account(accounts, account_no):
    for account in accounts:
        if account["account_no"] == account_no:
            return account
    return None


def get_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount > 0:
                return round(amount, 2)
            print("Amount must be greater than zero.")
        except ValueError:
            print("Enter a valid number.")


def transaction_history(account_no):
    print("\n--- Transaction History ---")
    found = False

    with open(TRANSACTION_FILE, "r", newline="") as f:
        for row in csv.DictReader(f):
            if row["account_no"] == account_no:
                found = True
                print(
                    row["date"],
                    "|", row["type"],
                    "| Rs.", row["amount"],
                    "| Balance: Rs.", row["balance"]
                )

    if not found:
        print("No transactions found.")


def account_menu(account):
    while True:
        print(f"\n--- Welcome, {account['name']} ---")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transaction History")
        print("5. Logout")

        choice = input("Enter your choice: ")

        accounts = load_accounts()
        account = find_account(accounts, account["account_no"])

        if choice == "1":
            print("Available Balance: Rs.",
                  f"{float(account['balance']):.2f}")

        elif choice == "2":
            amount = get_amount("Enter deposit amount: Rs. ")
            account["balance"] = f"{float(account['balance']) + amount:.2f}"
            save_accounts(accounts)

            log_transaction(
                account["account_no"], "Deposit",
                amount, float(account["balance"])
            )

            print("Deposit successful!")
            print("New Balance: Rs.", account["balance"])

        elif choice == "3":
            amount = get_amount("Enter withdrawal amount: Rs. ")
            balance = float(account["balance"])

            if amount > balance:
                print("Insufficient balance!")
            else:
                account["balance"] = f"{balance - amount:.2f}"
                save_accounts(accounts)

                log_transaction(
                    account["account_no"], "Withdrawal",
                    amount, float(account["balance"])
                )

                print("Withdrawal successful!")
                print("New Balance: Rs.", account["balance"])

        elif choice == "4":
            transaction_history(account["account_no"])

        elif choice == "5":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Try again.")


def login_account():
    accounts = load_accounts()

    print("\n--- Account Login ---")
    account_no = input("Enter account number: ").strip()
    pin = input("Enter PIN: ").strip()

    account = find_account(accounts, account_no)

    if account and account["pin"] == pin:
        account_menu(account)
    else:
        print("Invalid account number or PIN.")


def main():
    setup_files()

    while True:
        print("\n========== BANK ACCOUNT SIMULATOR ==========")
        print("1. Create Account")
        print("2. Login to Account")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            login_account()
        elif choice == "3":
            print("Thank you for using Bank Account Simulator!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
