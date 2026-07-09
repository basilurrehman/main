class Customer {
    private String customerID, name, address, contactNumber;

    public Customer(String customerID,String name,String address,String contactNumber)
    {
        this.customerID =customerID;
        this.name = name;
        this.contactNumber = contactNumber;
        this.address = address;
    }
    public String getCustomerDetails()
    {
        return customerID + name + contactNumber +address;
    }
}

class Account{
    protected int accountNumber; 
    //protected List<Transaction> transactionHistory; 
    protected Transaction[] transactionHistory;
    protected int balance;
    protected static int accountCount = 1000;
    protected int transactionCount=0;

    public Account(int balance)
    {
        this.accountNumber = accountCount++;
        this.balance = balance;
        this.transactionHistory = new Transaction[100];
    }

    public void deposit(int deposit){ // remember to change all access modifiers accordingly after completion
        balance+=deposit;
    }
    public void withdraw(int withdraw)
    {
        balance-=withdraw;
    }
    public int displayBalance(){
        return balance;
    }
    public void addTransaction(Transaction transaction)
    {
        transactionHistory[transactionCount] = transaction;
        this.transactionCount++;
    }
}

class Savings extends Accounts{
    private int interestRate;
    
}