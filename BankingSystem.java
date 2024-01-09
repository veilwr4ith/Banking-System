import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class BankAccount implements Serializable {
    private String accountNumber;
    private String accountHolderName;
    private double balance;
    private double loan;
    private char[] pin;

    public BankAccount(String accountNumber, String accountHolderName, char[] pin) {
        this.accountNumber = accountNumber;
        this.accountHolderName = accountHolderName;
        this.balance = 0.0;
        this.loan = 0.0;
        this.pin = pin;
    }

    public String getAccountNumber() {
        return accountNumber;
    }

    // Getter and setter methods

    public void deposit(double amount) {
        balance += amount;
        System.out.println("Deposit successful.");
        System.out.println("Current balance: $" + balance);
    }

    public void withdraw(double amount) {
        if (balance + loan >= amount) {
            if (balance >= amount) {
                balance -= amount;
                System.out.println("Withdrawal successful.");
                System.out.println("Current balance: $" + balance);
            } else {
                double remainingAmount = amount - balance;
                balance = 0;
                loan -= remainingAmount;
                System.out.println("Withdrawal successful.");
                System.out.println("Current balance: $" + balance);
                System.out.println("Loan amount remaining: $" + loan);
            }
        } else {
            System.out.println("Insufficient funds.");
            System.out.println("Current balance: $" + balance);
        }
    }

    public void displayAccountDetails() {
        System.out.println("Account Number: " + accountNumber);
        System.out.println("Account Holder: " + accountHolderName);
        System.out.println("Current Balance: $" + balance);
        System.out.println("Loan Amount: $" + loan);
    }

    public void requestLoan(double loanAmount) {
    if (loanAmount > 0) {
        loan += loanAmount;
        double interest = loanAmount * (5.0 / 100); // 5% interest rate
        balance += loanAmount - interest;
        System.out.println("Loan approved.");
        System.out.println("Loan amount: $" + loanAmount);
        System.out.println("Loan interest: $" + interest);
        System.out.println("Current balance: $" + balance);
    } else {
        System.out.println("Invalid loan request.");
    }
}

    public void repayLoan(double amount) {
        if (loan > 0) {
            if (amount >= loan) {
                balance -= amount;
                System.out.println("Loan fully repaid.");
                System.out.println("Current balance: $" + balance);
                System.out.println("Loan amount remaining: $0.00");
                loan = 0;
            } else {
                balance -= amount;
                loan -= amount;
                System.out.println("Loan partially repaid.");
                System.out.println("Current balance: $" + balance);
                System.out.println("Loan amount remaining: $" + loan);
            }
        } else {
            System.out.println("No active loan.");
        }
    }

    public boolean verifyPin(char[] enteredPin) {
        if (enteredPin.length != pin.length) {
            return false;
        }
        for (int i = 0; i < pin.length; i++) {
            if (enteredPin[i] != pin[i]) {
                return false;
            }
        }
        return true;
    }
}

class Bank implements Serializable {
    private List<BankAccount> accounts;
    private static final String DATA_FILE = "accounts.dat";

    public Bank() {
        accounts = new ArrayList<>();
        loadAccounts();
    }

    public void createAccount(String accountNumber, String accountHolderName, char[] pin) {
        System.out.println("Creating account...");
        loadingScreen();

        BankAccount account = new BankAccount(accountNumber, accountHolderName, pin);
        accounts.add(account);

        System.out.println("Account created successfully.");
        loadingScreen();

        saveAccounts();
    }

    public BankAccount findAccount(String accountNumber) {
        for (BankAccount account : accounts) {
            if (account.getAccountNumber().equals(accountNumber)) {
                return account;
            }
        }
        return null;
    }

    public void requestLoan(String accountNumber, char[] enteredPin, double loanAmount) {
        BankAccount loanAccount = findAccount(accountNumber);
        if (loanAccount != null) {
            if (loanAccount.verifyPin(enteredPin)) {
                loanAccount.requestLoan(loanAmount);
                saveAccounts();
                Bank.loadingScreen();
            } else {
                System.out.println("Invalid PIN.");
                Bank.loadingScreen();
            }
        } else {
            System.out.println("Account not found.");
            Bank.loadingScreen();
        }
    }

    private void loadAccounts() {
        try (ObjectInputStream inputStream = new ObjectInputStream(new FileInputStream(DATA_FILE))) {
            accounts = (List<BankAccount>) inputStream.readObject();
            System.out.println("Accounts loaded successfully.");
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("No existing accounts found.");
        }
    }

    public void saveAccounts() {
        try (ObjectOutputStream outputStream = new ObjectOutputStream(new FileOutputStream(DATA_FILE))) {
            outputStream.writeObject(accounts);
            System.out.println("Accounts saved successfully.");
        } catch (IOException e) {
            System.out.println("Failed to save accounts.");
        }
    }

    public static void loadingScreen() {
        try {
            Thread.sleep(2000); // Adjust the duration of the loading screen as needed
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

public class BankingSystem {
    public static void main(String[] args) {
        Bank bank = new Bank();
        Scanner scanner = new Scanner(System.in);
        int choice = 0;

        while (choice != 7) {
            clearScreen();
            System.out.println("   _____ __              __             _    __            ____");
            System.out.println("  / ___// /_  ____ _____/ /___ _      _| |  / /___ ___  __/ / /_");
            System.out.println("  \\__ \\/ __ \\/ __ `/ __  / __ \\ | /| / / | / / __ `/ / / / / __/");
            System.out.println(" ___/ / / / / /_/ / /_/ / /_/ / |/ |/ /| |/ / /_/ / /_/ / / /_");
            System.out.println("/____/_/ /_/\\__,_/\\__,_/\\____/|__/|__/ |___/\\__,_/\\__,_/_/\\__/");
            System.out.println("                                                By veilwr4ith            ");
            System.out.println("\nWelcome to the Banking System!");
            System.out.println("1. Create Account");
            System.out.println("2. Deposit");
            System.out.println("3. Withdraw");
            System.out.println("4. Account Details");
            System.out.println("5. Request Loan");
            System.out.println("6. Repay Loan");
            System.out.println("7. Exit");
            System.out.print("\nEnter your choice: ");
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume the newline character

            clearScreen();
            switch (choice) {
                case 1:
                    System.out.println("   _____ __              __             _    __            ____");
                    System.out.println("  / ___// /_  ____ _____/ /___ _      _| |  / /___ ___  __/ / /_");
                    System.out.println("  \\__ \\/ __ \\/ __ `/ __  / __ \\ | /| / / | / / __ `/ / / / / __/");
                    System.out.println(" ___/ / / / / /_/ / /_/ / /_/ / |/ |/ /| |/ / /_/ / /_/ / / /_");
                    System.out.println("/____/_/ /_/\\__,_/\\__,_/\\____/|__/|__/ |___/\\__,_/\\__,_/_/\\__/");
                    System.out.println("                                                By veilwr4ith           ");
                    System.out.println("\nCreating Account");
                    System.out.println("-----------------");
                    System.out.print("Enter Account Number: ");
                    String accountNumber = scanner.nextLine();
                    System.out.print("Enter Account Holder Name: ");
                    String accountHolderName = scanner.nextLine();
                    System.out.print("Set PIN: ");
                    char[] pin = System.console().readPassword(); // Read the PIN without echoing
                    bank.createAccount(accountNumber, accountHolderName, pin);
                    break;
                case 2:
                    System.out.println("   _____ __              __             _    __            ____");
                    System.out.println("  / ___// /_  ____ _____/ /___ _      _| |  / /___ ___  __/ / /_");
                    System.out.println("  \\__ \\/ __ \\/ __ `/ __  / __ \\ | /| / / | / / __ `/ / / / / __/");
                    System.out.println(" ___/ / / / / /_/ / /_/ / /_/ / |/ |/ /| |/ / /_/ / /_/ / / /_");
                    System.out.println("/____/_/ /_/\\__,_/\\__,_/\\____/|__/|__/ |___/\\__,_/\\__,_/_/\\__/");
                    System.out.println("                                                By veilwr4ith             ");
                    System.out.println("\nDeposit");
                    System.out.println("---------------");
                    System.out.print("Enter Account Number: ");
                    accountNumber = scanner.nextLine();
                    BankAccount depositAccount = bank.findAccount(accountNumber);
                    if (depositAccount != null) {
                        System.out.print("Enter PIN: ");
                        char[] enteredPin = System.console().readPassword(); // Read the PIN without echoing
                        if (depositAccount.verifyPin(enteredPin)) {
                            System.out.print("Enter Deposit Amount: ");
                            double depositAmount = scanner.nextDouble();
                            scanner.nextLine(); // Consume the newline character
                            System.out.println("---------------");
                            depositAccount.deposit(depositAmount);
                            bank.saveAccounts(); // Save account balances after deposit
                            Bank.loadingScreen();
                        } else {
                            System.out.println("Invalid PIN.");
                            Bank.loadingScreen();
                        }
                    } else {
                        System.out.println("Account not found.");
                        Bank.loadingScreen();
                    }
                    break;
                case 3:
                    System.out.println("   _____ __              __             _    __            ____");
                    System.out.println("  / ___// /_  ____ _____/ /___ _      _| |  / /___ ___  __/ / /_");
                    System.out.println("  \\__ \\/ __ \\/ __ `/ __  / __ \\ | /| / / | / / __ `/ / / / / __/");
                    System.out.println(" ___/ / / / / /_/ / /_/ / /_/ / |/ |/ /| |/ / /_/ / /_/ / / /_");
                    System.out.println("/____/_/ /_/\\__,_/\\__,_/\\____/|__/|__/ |___/\\__,_/\\__,_/_/\\__/");
                    System.out.println("                                                By veilwr4ith            ");
                    System.out.println("\nWithdraw");
                    System.out.println("---------------");
                    System.out.print("Enter Account Number: ");
                    accountNumber = scanner.nextLine();
                    BankAccount withdrawAccount = bank.findAccount(accountNumber);
                    if (withdrawAccount != null) {
                        System.out.print("Enter PIN: ");
                        char[] enteredPin = System.console().readPassword(); // Read the PIN without echoing
                        if (withdrawAccount.verifyPin(enteredPin)) {
                            System.out.print("Enter Withdrawal Amount: ");
                            double withdrawalAmount = scanner.nextDouble();
                            scanner.nextLine(); // Consume the newline character
                            System.out.println("---------------");
                            withdrawAccount.withdraw(withdrawalAmount);
                            bank.saveAccounts(); // Save account balances after withdrawal
                            Bank.loadingScreen();
                        } else {
                            System.out.println("Invalid PIN.");
                            Bank.loadingScreen();
                        }
                    } else {
                        System.out.println("Account not found.");
                        Bank.loadingScreen();
                    }
                    break;
                case 4:
                    System.out.println("   _____ __              __             _    __            ____");
                    System.out.println("  / ___// /_  ____ _____/ /___ _      _| |  / /___ ___  __/ / /_");
                    System.out.println("  \\__ \\/ __ \\/ __ `/ __  / __ \\ | /| / / | / / __ `/ / / / / __/");
                    System.out.println(" ___/ / / / / /_/ / /_/ / /_/ / |/ |/ /| |/ / /_/ / /_/ / / /_");
                    System.out.println("/____/_/ /_/\\__,_/\\__,_/\\____/|__/|__/ |___/\\__,_/\\__,_/_/\\__/");
                    System.out.println("                                                By veilwr4ith             ");
                    System.out.println("\nAccount Details");
                    System.out.println("---------------");
                    System.out.print("Enter Account Number: ");
                    accountNumber = scanner.nextLine();
                    BankAccount accountDetailsAccount = bank.findAccount(accountNumber);
                    if (accountDetailsAccount != null) {
                        System.out.print("Enter PIN: ");
                        char[] enteredPin = System.console().readPassword(); // Read the PIN without echoing
                        System.out.println("---------------");
                        if (accountDetailsAccount.verifyPin(enteredPin)) {
                            accountDetailsAccount.displayAccountDetails();
                            Bank.loadingScreen();
                        } else {
                            System.out.println("Invalid PIN.");
                            Bank.loadingScreen();
                        }
                    } else {
                        System.out.println("Account not found.");
                        Bank.loadingScreen();
                    }
                    break;

                case 5:
                    System.out.println("   _____ __              __             _    __            ____");
                    System.out.println("  / ___// /_  ____ _____/ /___ _      _| |  / /___ ___  __/ / /_");
                    System.out.println("  \\__ \\/ __ \\/ __ `/ __  / __ \\ | /| / / | / / __ `/ / / / / __/");
                    System.out.println(" ___/ / / / / /_/ / /_/ / /_/ / |/ |/ /| |/ / /_/ / /_/ / / /_");
                    System.out.println("/____/_/ /_/\\__,_/\\__,_/\\____/|__/|__/ |___/\\__,_/\\__,_/_/\\__/");
                    System.out.println("                                                By veilwr4ith             ");
                    System.out.println("\nRequest Loan");
                    System.out.println("---------------");
                    System.out.print("Enter Account Number: ");
                    accountNumber = scanner.nextLine();
                    BankAccount loanAccount = bank.findAccount(accountNumber);
                    if (loanAccount != null) {
                        System.out.print("Enter PIN: ");
                        char[] enteredPin = System.console().readPassword(); // Read the PIN without echoing
                        if (loanAccount.verifyPin(enteredPin)) {
                            System.out.print("Enter Loan Amount: ");
                            double loanAmount = scanner.nextDouble();
                            scanner.nextLine(); // Consume the newline character
                            System.out.println("---------------");
                            bank.requestLoan(accountNumber, enteredPin, loanAmount);
                        } else {
                            System.out.println("Invalid PIN.");
                            Bank.loadingScreen();
                        }
                    } else {
                        System.out.println("Account not found.");
                        Bank.loadingScreen();
                    }
                    break;
                case 6:
                    System.out.println("   _____ __              __             _    __            ____");
                    System.out.println("  / ___// /_  ____ _____/ /___ _      _| |  / /___ ___  __/ / /_");
                    System.out.println("  \\__ \\/ __ \\/ __ `/ __  / __ \\ | /| / / | / / __ `/ / / / / __/");
                    System.out.println(" ___/ / / / / /_/ / /_/ / /_/ / |/ |/ /| |/ / /_/ / /_/ / / /_");
                    System.out.println("/____/_/ /_/\\__,_/\\__,_/\\____/|__/|__/ |___/\\__,_/\\__,_/_/\\__/");
                    System.out.println("                                                By veilwr4ith             ");
                    System.out.println("\nRepay Loan");
                    System.out.println("---------------");
                    System.out.print("Enter Account Number: ");
                    accountNumber = scanner.nextLine();
                    BankAccount repayLoanAccount = bank.findAccount(accountNumber);
                    if (repayLoanAccount != null) {
                        System.out.print("Enter PIN: ");
                        char[] enteredPin = System.console().readPassword(); // Read the PIN without echoing
                        if (repayLoanAccount.verifyPin(enteredPin)) {
                            System.out.print("Enter Repayment Amount: ");
                            double repaymentAmount = scanner.nextDouble();
                            scanner.nextLine(); // Consume the newline character
                            System.out.println("---------------");
                            repayLoanAccount.repayLoan(repaymentAmount);
                            bank.saveAccounts(); // Save account balances and loan details
                            Bank.loadingScreen();
                        } else {
                            System.out.println("Invalid PIN.");
                            Bank.loadingScreen();
                        }
                    } else {
                        System.out.println("Account not found.");
                        Bank.loadingScreen();
                    }
                    break;
                case 7:
                    System.out.println("   _____ __              __             _    __            ____");
                    System.out.println("  / ___// /_  ____ _____/ /___ _      _| |  / /___ ___  __/ / /_");
                    System.out.println("  \\__ \\/ __ \\/ __ `/ __  / __ \\ | /| / / | / / __ `/ / / / / __/");
                    System.out.println(" ___/ / / / / /_/ / /_/ / /_/ / |/ |/ /| |/ / /_/ / /_/ / / /_");
                    System.out.println("/____/_/ /_/\\__,_/\\__,_/\\____/|__/|__/ |___/\\__,_/\\__,_/_/\\__/");
                    System.out.println("                                                By veilwr4ith            ");
                    System.out.println("\nExiting the program. Thank you for using the Banking System!");
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
                    Bank.loadingScreen();
            }
            if (choice != 7) {
                System.out.println();
                System.out.println("Press Enter to continue...");
                try {
                    System.in.read();
                    clearScreen();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        scanner.close();
    }

    public static void clearScreen() {
        try {
            if (System.getProperty("os.name").contains("Windows")) {
                new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
            } else {
                System.out.print("\033[H\033[2J");
                System.out.flush();
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}