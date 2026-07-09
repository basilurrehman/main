import java.util.List;
import java.util.ArrayList;
import java.time.LocalDate; // Base Class: Customer
class Customer {
    private String customerID;
    private String name;
    private String address;
    private String contactNumber;

    public Customer(String customerID, String name, String address, String contactNumber) {
        this.customerID = customerID;
        this.name = name;
        this.address = address;
        this.contactNumber = contactNumber;
    }
    
    public String getCustomerDetails() {
        return "ID: " + customerID + ", Name: " + name + ", Address: " + address + ", Contact: " + contactNumber;
    }
}

// Account class (Base class for all types of accounts)
class Account {
    protected String accountNumber;
    protected double balance;
    protected java.util.List<Transaction> transactionHistory;
    private SecurityModule security;

    public Account(String accountNumber, double balance) {
        this.accountNumber = accountNumber;
        this.balance = balance;
        this.transactionHistory = new java.util.ArrayList<>();
        // Composition: SecurityModule exists as a part of Account
        this.security = new SecurityModule("secretKey");
    }
    
    public void deposit(double amount) {
        if(amount > 0) {
            balance += amount;
            transactionHistory.add(new Transaction("T" + System.currentTimeMillis(), "Deposit", amount));
        }
    }

    public boolean withdraw(double amount) {
        // Check for sufficient funds
        if(amount > 0 && balance >= amount) {
            balance -= amount;
            transactionHistory.add(new Transaction("T" + System.currentTimeMillis(), "Withdrawal", amount));
            return true;
        } else {
            System.out.println("Insufficient balance!");
            return false;
        }
    }
    
    public double getBalance() {
        return balance;
    }
    
    public void displayTransactions() {
        System.out.println("Transaction History for Account: " + accountNumber);
        for(Transaction t : transactionHistory) {
            System.out.println(t.getTransactionDetails());
        }
    }
}

// Derived Class: SavingsAccount (Inheritance)
class SavingsAccount extends Account {
    private double interestRate;

    public SavingsAccount(String accountNumber, double balance, double interestRate) {
        super(accountNumber, balance);
        this.interestRate = interestRate;
    }
    
    // Recursively calculate interest for multiple years
    public double calculateInterest(int years) {
        if(years == 0) return balance;
        balance = balance + balance * interestRate;
        return calculateInterest(years - 1);
    }
}

// Derived Class: CurrentAccount (Inheritance)
class CurrentAccount extends Account {
    private double overdraftLimit;

    public CurrentAccount(String accountNumber, double balance, double overdraftLimit) {
        super(accountNumber, balance);
        this.overdraftLimit = overdraftLimit;
    }
    
    public boolean checkOverdraftAvailability(double amount) {
        return (balance + overdraftLimit) >= amount;
    }
}

// Transaction Class (Aggregation)
class Transaction {
    private String transactionID;
    private String date;
    private String type;
    private double amount;
    
    public Transaction(String transactionID, String type, double amount) {
        this.transactionID = transactionID;
        this.date = java.time.LocalDate.now().toString();
        this.type = type;
        this.amount = amount;
    }
    
    public String getTransactionDetails() {
        return "ID: " + transactionID + ", Date: " + date + ", Type: " + type + ", Amount: $" + amount;
    }
}

// SecurityModule Class (Composition)
class SecurityModule {
    private String encryptionKey;
    
    public SecurityModule(String encryptionKey) {
        this.encryptionKey = encryptionKey;
    }
    
    public boolean verifyUser(String key) {
        return this.encryptionKey.equals(key);
    }
    
    // Methods to encrypt/decrypt data could be added here
}

// BankOperations Class (Association between Customer and Account)
class BankOperations {
    private Customer customer;
    private Account account;
    
    public BankOperations(Customer customer, Account account) {
        this.customer = customer;
        this.account = account;
    }
    
    public void processDeposit(double amount) {
        account.deposit(amount);
    }
    
    public void processWithdrawal(double amount) {
        if(account.withdraw(amount)) {
            System.out.println("Withdrawal successful.");
        }
    }
    
    public void inquireBalance() {
        System.out.println("Current Balance: $" + account.getBalance());
    }
}

// Main Class Implementation
public class Main {
    public static void main(String[] args) {
        // Create a Customer
        Customer cust = new Customer("C001", "John Doe", "123 Main St", "555-1234");
        System.out.println("Customer Details: " + cust.getCustomerDetails());
        
        // Create accounts: Savings and Current
        SavingsAccount savings = new SavingsAccount("A1001", 1000.0, 0.05);
        CurrentAccount current = new CurrentAccount("A2001", 500.0, 200.0);
        
        // Process transactions through BankOperations
        BankOperations opSavings = new BankOperations(cust, savings);
        opSavings.processDeposit(500);
        opSavings.processWithdrawal(200);
        opSavings.inquireBalance();
        savings.displayTransactions();
        
        // Calculate interest recursively for 3 years in Savings Account
        double futureBalance = savings.calculateInterest(3);
        System.out.println("Balance after 3 years with interest: $" + futureBalance);
        
        // Similarly, you can create BankOperations for current account and display its details.
    }
}
