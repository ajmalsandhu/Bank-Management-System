import os
import json

class ATM:
    def __init__(self, balance=0, pincode=1234):
        self._balance = balance
        self._pincode = pincode

    def get_balance(self):
        return self._balance

    def withdraw(self, amount, pin):
        if pin != self._pincode:
            print("Invalid PIN.")
            return False
        if amount > self._balance:
            print("Insufficient Balance.")
            return False
        self._balance -= amount
        return True

    def deposit(self, amount):
        self._balance += amount

    def transfer(self, amount, receiver, pin):
        if pin != self._pincode:
            print("Invalid PIN.")
            return False
        success = self.withdraw(amount, pin)
        if success:
            receiver.deposit(amount)
            return True
        return False

    def change_pin(self, old_pin, new_pin):
        if old_pin == self._pincode:
            self._pincode = new_pin
            print("PIN changed successfully.")
        else:
            print("Invalid old PIN.")

class ATMSystem:
    def __init__(self, storage_file='atm_data.json', manager_pin=9999):
        self.storage_file = storage_file
        self.manager_pin = manager_pin
        self.load_data()

    def load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file: # r means,it opens the file in read mode
                data = json.load(file)
                self.accounts = {acc: ATM(balance, pin) for acc, (balance, pin) in data.items()}
        else:
            self.accounts = {}

    def save_data(self):
        data = {acc: (atm.get_balance(), atm._pincode) for acc, atm in self.accounts.items()}
        with open(self.storage_file, 'w') as file: # w means,it opens the file in write mode
            json.dump(data, file)

    def create_account(self, account_number, initial_balance=0, pincode=1234):
        if account_number in self.accounts:
            print("Account already exists.")
        else:
            self.accounts[account_number] = ATM(initial_balance, pincode)
            self.save_data()
            print("Account created successfully.")

    def access_account(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number]
        else:
            print("Account not found.")
            return None

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]  # Remove the account
            self.save_data()  # Save the updated account data
            print(f"Account {account_number} has been deleted.")
        else:
            print("Account not found.")

    def show_all_accounts(self, manager_pin):
        if manager_pin == self.manager_pin:
            print("\n--- All Accounts ---")
            for account_number, atm in self.accounts.items():
                print(f"Account Number: {account_number}, Balance: ${atm.get_balance()}")
        else:
            print("Invalid Manager PIN.")

    def main_menu(self):
        while True:
            print("\n--- ATM System ---")
            print("1. Create Account")
            print("2. Access Account")
            print("3. Delete Account")
            print("4. View All Accounts (Manager Only)")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                account_number = input("Enter new account number: ")
                initial_balance = float(input("Enter initial balance: "))
                pincode = int(input("Set a 4-digit PIN: "))
                self.create_account(account_number, initial_balance, pincode)

            elif choice == '2':
                account_number = input("Enter your account number: ")
                atm = self.access_account(account_number)
                if atm:
                    self.account_menu(atm)

            elif choice == '3':  # Delete account option
                account_number = input("Enter the account number to delete: ")
                self.delete_account(account_number)

            elif choice == '4':  # Manager option to view all accounts
                manager_pin = int(input("Enter the Manager PIN: "))
                self.show_all_accounts(manager_pin)

            elif choice == '5':
                self.save_data()
                print("Exiting... Goodbye!")
                break

            else:
                print("Invalid choice, please try again.")

    def account_menu(self, atm):
        while True:
            print("\n--- Account Menu ---")
            print("1. View Balance")
            print("2. Withdraw Balance")
            print("3. Deposit Cash")
            print("4. Transfer Cash")
            print("5. Change PIN")
            print("6. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == '1':
                print(f"Your Current Balance is: ${atm.get_balance()}")

            elif choice == '2':
                pin = int(input("Enter your PIN: "))
                amount = float(input("Enter the amount to withdraw: "))
                if atm.withdraw(amount, pin):
                    print("Withdrawal successful.")
                self.save_data()

            elif choice == '3':
                amount = float(input("Enter the amount to deposit: "))
                atm.deposit(amount)
                print("Deposit successful.")
                self.save_data()

            elif choice == '4':
                pin = int(input("Enter your PIN: "))
                receiver_account = input("Enter the receiver's account number: ")
                amount = float(input("Enter the amount to transfer: "))
                receiver = self.access_account(receiver_account)
                if receiver and atm.transfer(amount, receiver, pin):
                    print("Transfer successful.")
                self.save_data()

            elif choice == '5':
                old_pin = int(input("Enter your old PIN: "))
                new_pin = int(input("Enter your new PIN: "))
                atm.change_pin(old_pin, new_pin)
                self.save_data()

            elif choice == '6':
                break

            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    atm_system = ATMSystem()
    atm_system.main_menu()
