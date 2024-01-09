import pickle
import os
import getpass
import time

class BankAccount:
    def __init__(self, accountNumber, accountHolderName, pin):
        self.accountNumber = accountNumber
        self.accountHolderName = accountHolderName
        self.balance = 0.0
        self.loan = 0.0
        self.pin = pin

    def getAccountNumber(self):
        return self.accountNumber

    def deposit(self, amount):
        self.balance += amount
        print("Deposit successful.")
        print("Current balance: $" + str(self.balance))

    def withdraw(self, amount):
        if self.balance + self.loan >= amount:
            if self.balance >= amount:
                self.balance -= amount
                print("Withdrawal successful.")
                print("Current balance: $" + str(self.balance))
            else:
                remainingAmount = amount - self.balance
                self.balance = 0
                self.loan -= remainingAmount
                print("Withdrawal successful.")
                print("Current balance: $" + str(self.balance))
                print("Loan amount remaining: $" + str(self.loan))
        else:
            print("Insufficient funds.")
            print("Current balance: $" + str(self.balance))

    def displayAccountDetails(self):
        print("Account Number: " + self.accountNumber)
        print("Account Holder: " + self.accountHolderName)
        print("Current Balance: $" + str(self.balance))
        print("Loan Amount: $" + str(self.loan))

    def requestLoan(self, loanAmount):
        if loanAmount > 0:
            self.loan += loanAmount
            interest = loanAmount * (5.0 / 100)  # 5% interest rate
            self.balance += loanAmount - interest
            print("Loan approved.")
            print("Loan amount: $" + str(loanAmount))
            print("Loan interest: $" + str(interest))
            print("Current balance: $" + str(self.balance))
        else:
            print("Invalid loan request.")

    def repayLoan(self, amount):
        if self.loan > 0:
            if amount >= self.loan:
                self.balance -= amount
                print("Loan fully repaid.")
                print("Current balance: $" + str(self.balance))
                print("Loan amount remaining: $0.00")
                self.loan = 0
            else:
                self.balance -= amount
                self.loan -= amount
                print("Loan partially repaid.")
                print("Current balance: $" + str(self.balance))
                print("Loan amount remaining: $" + str(self.loan))
        else:
            print("No active loan.")

    def verifyPin(self, enteredPin):
        if len(enteredPin) != len(self.pin):
            return False
        for i in range(len(self.pin)):
            if enteredPin[i] != self.pin[i]:
                return False
        return True

    def payBill(self, billType, amount):
        if billType == "Meralco":
            # Process Meralco bill payment
            if self.balance >= amount:
                self.balance -= amount
                print(f"{billType} bill payment of ${amount} successful.")
                print("Current balance: $" + str(self.balance))
            else:
                print("Insufficient funds.")
                print("Current balance: $" + str(self.balance))
        elif billType == "Water District":
            # Process Water District bill payment
            if self.balance >= amount:
                self.balance -= amount
                print(f"{billType} bill payment of ${amount} successful.")
                print("Current balance: $" + str(self.balance))
            else:
                print("Insufficient funds.")
                print("Current balance: $" + str(self.balance))
        elif billType == "Converge":
            # Process Converge bill payment
            if self.balance >= amount:
                self.balance -= amount
                print(f"{billType} bill payment of ${amount} successful.")
                print("Current balance: $" + str(self.balance))
            else:
                print("Insufficient funds.")
                print("Current balance: $" + str(self.balance))
        elif billType == "PLDT":
            # Process PLDT bill payment
            if self.balance >= amount:
                self.balance -= amount
                print(f"{billType} bill payment of ${amount} successful.")
                print("Current balance: $" + str(self.balance))
            else:
                print("Insufficient funds.")
                print("Current balance: $" + str(self.balance))
        else:
            print("Invalid bill type.")

class Bank:
    def __init__(self):
        self.accounts = []
        self.DATA_FILE = "accounts.pkl"
        self.loadAccounts()

    def createAccount(self, accountNumber, accountHolderName, pin):
        print("Creating account...")
        self.loadingScreen()

        account = BankAccount(accountNumber, accountHolderName, pin)
        self.accounts.append(account)

        print("Account created successfully.")
        self.loadingScreen()

        self.saveAccounts()

    def findAccount(self, accountNumber):
        for account in self.accounts:
            if account.getAccountNumber() == accountNumber:
                return account
        return None

    def requestLoan(self, accountNumber, enteredPin, loanAmount):
        loanAccount = self.findAccount(accountNumber)
        if loanAccount:
            if loanAccount.verifyPin(enteredPin):
                loanAccount.requestLoan(loanAmount)
                self.saveAccounts()
                self.loadingScreen()
            else:
                print("Invalid PIN.")
                self.loadingScreen()
        else:
            print("Account not found.")
            self.loadingScreen()

    def loadAccounts(self):
        try:
            with open(self.DATA_FILE, 'rb') as file:
                self.accounts = pickle.load(file)
                print("Accounts loaded successfully.")
        except (IOError, EOFError):
            print("No existing accounts found.")

    def saveAccounts(self):
        try:
            with open(self.DATA_FILE, 'wb') as file:
                pickle.dump(self.accounts, file)
                print("Accounts saved successfully.")
        except IOError:
            print("Failed to save accounts.")

    def payBill(self, accountNumber, enteredPin, billType, amount):
        billAccount = self.findAccount(accountNumber)
        if billAccount:
            if billAccount.verifyPin(enteredPin):
                billAccount.payBill(billType, amount)
                self.saveAccounts()
                self.loadingScreen()
            else:
                print("Invalid PIN.")
                self.loadingScreen()
        else:
            print("Account not found.")
            self.loadingScreen()

    @staticmethod
    def loadingScreen():
        time.sleep(2)  # Adjust the duration of the loading screen as needed

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    bank = Bank()

    while True:
        clearScreen()
        print("   _____ __              __             _    __            ____")
        print("  / ___// /_  ____ _____/ /___ _      _| |  / /___ ___  __/ / /_")
        print("  \\__ \\/ __ \\/ __ `/ __  / __ \\ | /| / / | / / __ `/ / / / / __/")
        print(" ___/ / / / / /_/ / /_/ / /_/ / |/ |/ /| |/ / /_/ / /_/ / / /_")
        print("/____/_/ /_/\\__,_/\\__,_/\\____/|__/|__/ |___/\\__,_/\\__,_/_/\\__/")
        print("                                                By veilwr4ith            ")
        print("\nWelcome to the Banking System!")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Account Details")
        print("5. Request Loan")
        print("6. Repay Loan")
        print("7. Pay Bills")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            print("\nCreating Account")
            print("-----------------")
            accountNumber = input("Enter Account Number: ")
            accountHolderName = input("Enter Account Holder Name: ")
            pin = getpass.getpass("Set PIN: ")
            bank.createAccount(accountNumber, accountHolderName, pin)
            input("\nPress Enter to continue...")
            continue
        elif choice == '2':
            print("\nDeposit")
            print("---------------")
            accountNumber = input("Enter Account Number: ")
            depositAccount = bank.findAccount(accountNumber)
            if depositAccount:
                enteredPin = getpass.getpass("Enter PIN: ")
                if depositAccount.verifyPin(enteredPin):
                    depositAmount = float(input("Enter Deposit Amount: "))
                    print("---------------")
                    depositAccount.deposit(depositAmount)
                    bank.saveAccounts()
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
                else:
                    print("Invalid PIN.")
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
            else:
                print("Account not found.")
                bank.loadingScreen()
                input("\nPress Enter to continue...")
                continue
        elif choice == '3':
            print("\nWithdraw")
            print("---------------")
            accountNumber = input("Enter Account Number: ")
            withdrawAccount = bank.findAccount(accountNumber)
            if withdrawAccount:
                enteredPin = getpass.getpass("Enter PIN: ")
                if withdrawAccount.verifyPin(enteredPin):
                    withdrawalAmount = float(input("Enter Withdrawal Amount: "))
                    print("---------------")
                    withdrawAccount.withdraw(withdrawalAmount)
                    bank.saveAccounts()
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
                else:
                    print("Invalid PIN.")
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
            else:
                print("Account not found.")
                bank.loadingScreen()
                input("\nPress Enter to continue...")
                continue
        elif choice == '4':
            print("\nAccount Details")
            print("---------------")
            accountNumber = input("Enter Account Number: ")
            accountDetailsAccount = bank.findAccount(accountNumber)
            if accountDetailsAccount:
                enteredPin = getpass.getpass("Enter PIN: ")
                print("---------------")
                if accountDetailsAccount.verifyPin(enteredPin):
                    accountDetailsAccount.displayAccountDetails()
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
                else:
                    print("Invalid PIN.")
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
            else:
                print("Account not found.")
                bank.loadingScreen()
                input("\nPress Enter to continue...")
                continue
        elif choice == '5':
            print("\nRequest Loan")
            print("---------------")
            accountNumber = input("Enter Account Number: ")
            loanAccount = bank.findAccount(accountNumber)
            if loanAccount:
                enteredPin = getpass.getpass("Enter PIN: ")
                if loanAccount.verifyPin(enteredPin):
                    loanAmount = float(input("Enter Loan Amount: "))
                    print("---------------")
                    bank.requestLoan(accountNumber, enteredPin, loanAmount)
                    input("\nPress Enter to continue...")
                    continue
                else:
                    print("Invalid PIN.")
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
            else:
                print("Account not found.")
                bank.loadingScreen()
                input("\nPress Enter to continue...")
                continue
        elif choice == '6':
            print("\nRepay Loan")
            print("---------------")
            accountNumber = input("Enter Account Number: ")
            repayLoanAccount = bank.findAccount(accountNumber)
            if repayLoanAccount:
                enteredPin = getpass.getpass("Enter PIN: ")
                if repayLoanAccount.verifyPin(enteredPin):
                    repaymentAmount = float(input("Enter Repayment Amount: "))
                    print("---------------")
                    repayLoanAccount.repayLoan(repaymentAmount)
                    bank.saveAccounts()
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
                else:
                    print("Invalid PIN.")
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
            else:
                print("Account not found.")
                bank.loadingScreen()
                input("\nPress Enter to continue...")
                continue
        if choice == '7':
            print("\nPay Bill")
            print("---------------")
            accountNumber = input("Enter Account Number: ")
            billAccount = bank.findAccount(accountNumber)
            if billAccount:
                enteredPin = getpass.getpass("Enter PIN: ")
                if billAccount.verifyPin(enteredPin):
                    print("Select bill type:")
                    print("1. Meralco")
                    print("2. Water District")
                    print("3. Converge")
                    print("4. PLDT")
                    billChoice = input("Enter your choice: ")

                    if billChoice == '1':
                        billType = "Meralco"
                        amount = float(input("Enter Meralco bill amount: "))
                    elif billChoice == '2':
                        billType = "Water District"
                        amount = float(input("Enter Water District bill amount: "))
                    elif billChoice == '3':
                        billType = "Converge"
                        amount = float(input("Enter Converge bill amount: "))
                    elif billChoice == '4':
                        billType = "PLDT"
                        amount = float(input("Enter PLDT bill amount: "))
                    else:
                        print("Invalid bill choice.")
                        continue

                    print("---------------")
                    bank.payBill(accountNumber, enteredPin, billType, amount)
                    input("\nPress Enter to continue...")
                    continue
                else:
                    print("Invalid PIN.")
                    bank.loadingScreen()
                    input("\nPress Enter to continue...")
                    continue
            else:
                print("Account not found.")
                bank.loadingScreen()
                input("\nPress Enter to continue...")
                continue

        elif choice == '8':
            print("\nExiting the program. Thank you for using the Banking System!")
            break
        else:
            print("Invalid choice. Please try again.")
            bank.loadingScreen()

if __name__ == "__main__":
    main()