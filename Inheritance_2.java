class Member {
    private String memberName;
    private String memberEmail;
    private String memberContact;

    public Member(String name, String email, String contact) {
        this.memberName = name;
        this.memberEmail = email;
        this.memberContact = contact;
    }

    public String getMemberName() { return memberName; }
    public String getMemberEmail() { return memberEmail; }
    public String getMemberContact() { return memberContact; }
}

class Account 
{ 
 private int accountNo;
 private Member accountOwner;
 private String accountBranch;
  private double accountBalance;

    public Account(int accNo, String branch, Member owner, double balance) {
        this.accountNo = accNo;
        this.accountBranch = branch;
        this.accountOwner = owner;
        this.accountBalance = balance;
    }

    public String getOwnerName() { return accountOwner.getMemberName(); }
    public String getOwnerEmail() { return accountOwner.getMemberEmail(); }
    public String getOwnerContact() { return accountOwner.getMemberContact(); }
   public int getAccountNo() { return accountNo; }
    public String getAccountBranch() { return accountBranch; }
    public double getAccountBalance() { return accountBalance; }
}

class CurrentAccount extends Account {
    private String accountType = "Current Account";

    public CurrentAccount(String type, int accNo, String branch, Member owner, double balance) {
        super(accNo, branch, owner, balance);
    }

    public String getAccountType() { return accountType; }

    public void displayInfo() {
        System.out.println("Account Type: " + getAccountType());
        System.out.println("Account Number: " + getAccountNo());
        System.out.println("Branch: " + getAccountBranch());
        System.out.println("Balance: " + getAccountBalance());
        System.out.println("Owner Name: " + getOwnerName());
        System.out.println("Owner Email: " + getOwnerEmail());
        System.out.println("Owner Contact: " + getOwnerContact());
        System.out.println();
    }
}

class SavingAccount extends Account {
    private String accountType = "Saving Account";

    public SavingAccount(String type, int accNo, String branch, Member owner, double balance) {
        super(accNo, branch, owner, balance);
    }

    public String getAccountType() { return accountType; }

    public void displayInfo() {
        System.out.println("Account Type: " + getAccountType());
        System.out.println("Account Number: " + getAccountNo());
        System.out.println("Branch: " + getAccountBranch());
        System.out.println("Balance: " + getAccountBalance());
        System.out.println("Owner Name: " + getOwnerName());
        System.out.println("Owner Email: " + getOwnerEmail());
        System.out.println("Owner Contact: " + getOwnerContact());
        System.out.println();
    }
}

public class Inheritance_2 {
    public static void main(String[] args) {
        Member member1 = new Member("Alice", "alice@example.com", "123-456-7890");
        Member member2 = new Member("Bob", "bob@example.com", "987-654-3210");
        Member member3 = new Member("Charlie", "charlie@example.com", "555-666-7777");

        CurrentAccount acc1 = new CurrentAccount("Current", 1001, "Main Branch", member1, 5000.0);
        CurrentAccount acc2 = new CurrentAccount("Current", 1002, "Downtown Branch", member2, 7000.0);
        SavingAccount acc3 = new SavingAccount("Saving", 2001, "Uptown Branch", member3, 12000.0);

        acc1.displayInfo();
        acc2.displayInfo();
        acc3.displayInfo();
    }
}
