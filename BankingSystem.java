import java.util.Scanner;

class Account {
    protected static int nextAccountNumber = 1000;
    protected String accountNumber;
    protected double balance;
    protected String[] transactionHistory;
    protected int transactionCount;

    public Account(double initialBalance) {
        this.accountNumber = String.valueOf(nextAccountNumber++);
        this.balance = initialBalance;
        transactionHistory = new String[100]; 
        transactionCount = 0;
        addTransaction("Account created with initial balance: " + initialBalance);
    }

    protected void addTransaction(String record) {
        if (transactionCount < transactionHistory.length) {
            transactionHistory[transactionCount++] = record;
        }
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            addTransaction("Deposited: " + amount + ", New Balance: " + balance);
            System.out.println("Deposit successful. Current balance: " + balance);
        } else {
            System.out.println("Invalid deposit amount.");
        }
    }

    public void withdraw(double amount) {
        if (amount > 0) {
            if (amount <= balance) {
                balance -= amount;
                addTransaction("Withdrew: " + amount + ", New Balance: " + balance);
                System.out.println("Withdrawal successful. Current balance: " + balance);
            } else {
                System.out.println("Insufficient funds.");
            }
        } else {
            System.out.println("Invalid withdrawal amount.");
        }
    }

    public double getBalance() {
        return balance;
    }

    public void printTransactionHistory() {
        System.out.println("Transaction History for Account " + accountNumber + ":");
        for (int i = 0; i < transactionCount; i++) {
            System.out.println(transactionHistory[i]);
        }
    }

    public String getAccountNumber() {
        return accountNumber;
    }
}

class BankAccount extends Account {
    private double interestRate;

    public BankAccount(double initialBalance, double interestRate) {
        super(initialBalance);
        this.interestRate = interestRate;
    }

    public double calculateCompoundInterest(int years) {
        if (interestRate <= 0) {
            System.out.println("Compound interest calculation is not available for current accounts.");
            return balance;
        }
        return calculateCompoundInterestRecursive(balance, interestRate, years);
    }

    private double calculateCompoundInterestRecursive(double principal, double rate, int years) {
        if (years == 0) {
            return principal;
        } else {
            return calculateCompoundInterestRecursive(principal * (1 + rate), rate, years - 1);
        }
    }

    public double getInterestRate() {
        return interestRate;
    }
}

class Customer {
    private String name;
    private String password;
    private BankAccount account;

    public Customer(String name, String password, BankAccount account) {
        this.name = name;
        this.password = password;
        this.account = account;
    }

    public String getName() {
        return name;
    }

    public BankAccount getAccount() {
        return account;
    }

    public boolean validatePassword(String inputPassword) {
        return this.password.equals(inputPassword);
    }
}

class Bank {
    private String bankName;
    private Customer[] customers;
    private int customerCount;

    public Bank(String bankName) {
        this.bankName = bankName;
        customers = new Customer[100];
        customerCount = 0;
    }

    public void addCustomer(Customer customer) {
        if(customerCount < customers.length) {
            customers[customerCount++] = customer;
        }
    }

    public Customer findCustomerByAccount(String accountNumber) {
        for (int i = 0; i < customerCount; i++) {
            if (customers[i].getAccount().getAccountNumber().equals(accountNumber)) {
                return customers[i];
            }
        }
        return null;
    }

    public void listCustomers() {
        System.out.println("Customers of " + bankName + ":");
        for (int i = 0; i < customerCount; i++) {
            System.out.println("- " + customers[i].getName() +
                               " (Account Number: " + customers[i].getAccount().getAccountNumber() + ")");
        }
    }
}

public class BankingSystem {
    private static final String ADMIN_PASSWORD = "admin123";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Bank bank = new Bank("Global Bank");

        boolean exitSystem = false;
        while (!exitSystem) {
            System.out.println("\nWelcome to Global Bank Automated Banking System");
            System.out.println("1. Create New Account");
            System.out.println("2. Login to Existing Account");
            System.out.println("3. Admin: List All Customers");
            System.out.println("0. Exit");
            System.out.print("Enter your choice: ");
            int mainChoice = scanner.nextInt();
            scanner.nextLine(); 

            switch (mainChoice) {
                case 1:
                    createNewAccount(bank, scanner);
                    break;
                case 2:
                    loginToAccount(bank, scanner);
                    break;
                case 3:
                    System.out.print("Enter admin password: ");
                    String adminPass = scanner.nextLine();
                    if (ADMIN_PASSWORD.equals(adminPass)) {
                        bank.listCustomers();
                    } else {
                        System.out.println("Invalid admin password.");
                    }
                    break;
                case 0:
                    System.out.println("Thank you for banking with us. Goodbye!");
                    exitSystem = true;
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
                    break;
            }
        }
        scanner.close();
    }
    
    private static void createNewAccount(Bank bank, Scanner scanner) {
        System.out.print("Enter your name: ");
        String name = scanner.nextLine();

        System.out.print("Enter a password for your account: ");
        String password = scanner.nextLine();

        System.out.print("Select account type (1 for Savings, 2 for Current): ");
        int accountType = scanner.nextInt();
        scanner.nextLine(); 

        System.out.print("Enter initial deposit amount: ");
        double initialDeposit = scanner.nextDouble();
        scanner.nextLine();

        double interestRate = 0;
        if (accountType == 1) {
            System.out.print("Enter interest rate (e.g., 0.05 for 5%): ");
            interestRate = scanner.nextDouble();
            scanner.nextLine(); 
        } else if (accountType != 2) {
            System.out.println("Invalid account type selected.");
            return;
        }
        BankAccount account = new BankAccount(initialDeposit, interestRate);
        Customer customer = new Customer(name, password, account);
        bank.addCustomer(customer);
        System.out.println("Account created successfully! Your account number is: " + account.getAccountNumber());
    }

    private static void loginToAccount(Bank bank, Scanner scanner) {
        System.out.print("Enter your account number: ");
        String accNum = scanner.nextLine();

        Customer customer = bank.findCustomerByAccount(accNum);
        if (customer == null) {
            System.out.println("Account not found. Please check your account number.");
            return;
        }

        System.out.print("Enter your password: ");
        String inputPassword = scanner.nextLine();
        if (!customer.validatePassword(inputPassword)) {
            System.out.println("Incorrect password.");
            return;
        }

        BankAccount account = customer.getAccount();
        boolean loggedIn = true;
        while (loggedIn) {
            System.out.println("\nHello, " + customer.getName());
            System.out.println("Account Number: " + account.getAccountNumber());
            System.out.println("1. Deposit");
            System.out.println("2. Withdraw");
            System.out.println("3. Check Balance");
            System.out.println("4. Transaction History");
            if (account.getInterestRate() > 0) {
                System.out.println("5. Calculate Compound Interest");
            }
            System.out.println("0. Logout");
            System.out.print("Enter your choice: ");
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    System.out.print("Enter deposit amount: ");
                    double depositAmount = scanner.nextDouble();
                    scanner.nextLine();
                    account.deposit(depositAmount);
                    break;
                case 2:
                    System.out.print("Enter withdrawal amount: ");
                    double withdrawAmount = scanner.nextDouble();
                    scanner.nextLine();
                    account.withdraw(withdrawAmount);
                    break;
                case 3:
                    System.out.println("Current Balance: " + account.getBalance());
                    break;
                case 4:
                    account.printTransactionHistory();
                    break;
                case 5:
                    if (account.getInterestRate() > 0) {
                        System.out.print("Enter number of years for interest calculation: ");
                        int years = scanner.nextInt();
                        scanner.nextLine();
                        double futureBalance = account.calculateCompoundInterest(years);
                        System.out.println("Balance after " + years + " years with compound interest: " + futureBalance);
                    } else {
                        System.out.println("Invalid option for current account.");
                    }
                    break;
                case 0:
                    System.out.println("Logging out...");
                    loggedIn = false;
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
                    break;
            }
        }
    }
}
