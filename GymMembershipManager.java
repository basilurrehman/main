import java.sql.*;
import java.util.Scanner;

public class GymMembershipManager {
    static final String DB_URL = "jdbc:mysql://localhost:3306/GymDB";
    static final String USER = "gymuser"; // or your MySQL username
    static final String PASS = "gympass";     // or your MySQL password

    static Connection conn;
    static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            menu();
            conn.close();
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    static void menu() {
        int choice;
        do {
            System.out.println("\n--- Gym Membership Manager ---");
            System.out.println("1. Add Member");
            System.out.println("2. View Members");
            System.out.println("3. Update Member");
            System.out.println("4. Delete Member");
            System.out.println("5. Exit");
            System.out.print("Choice: ");
            choice = Integer.parseInt(sc.nextLine());

            switch (choice) {
                case 1 -> addMember();
                case 2 -> viewMembers();
                case 3 -> updateMember();
                case 4 -> deleteMember();
                case 5 -> System.out.println("Goodbye!");
                default -> System.out.println("Invalid choice.");
            }
        } while (choice != 5);
    }

    static void addMember() {
        try {
            System.out.print("Name: ");
            String name = sc.nextLine();
            System.out.print("Membership Type: ");
            String type = sc.nextLine();
            System.out.print("Start Date (YYYY-MM-DD): ");
            String start = sc.nextLine();
            System.out.print("End Date (YYYY-MM-DD): ");
            String end = sc.nextLine();
            System.out.print("Status (Active/Inactive): ");
            String status = sc.nextLine();

            String sql = "INSERT INTO Members (Name, MembershipType, StartDate, EndDate, Status) VALUES (?, ?, ?, ?, ?)";
            PreparedStatement pst = conn.prepareStatement(sql);
            pst.setString(1, name);
            pst.setString(2, type);
            pst.setDate(3, Date.valueOf(start));
            pst.setDate(4, Date.valueOf(end));
            pst.setString(5, status);

            pst.executeUpdate();
            System.out.println("Member added.");
        } catch (Exception e) {
            System.out.println("Error adding member: " + e.getMessage());
        }
    }

    static void viewMembers() {
        try {
            ResultSet rs = conn.createStatement().executeQuery("SELECT * FROM Members");
            System.out.println("\n-- Members List --");
            while (rs.next()) {
                System.out.printf("ID: %d | Name: %s | Type: %s | From: %s | To: %s | Status: %s\n",
                        rs.getInt("MemberID"),
                        rs.getString("Name"),
                        rs.getString("MembershipType"),
                        rs.getDate("StartDate"),
                        rs.getDate("EndDate"),
                        rs.getString("Status"));
            }
        } catch (SQLException e) {
            System.out.println("Error viewing members.");
        }
    }

    static void updateMember() {
        try {
            System.out.print("Enter Member ID to update: ");
            int id = Integer.parseInt(sc.nextLine());

            System.out.print("New Membership Type: ");
            String type = sc.nextLine();
            System.out.print("New End Date (YYYY-MM-DD): ");
            String end = sc.nextLine();
            System.out.print("New Status (Active/Inactive): ");
            String status = sc.nextLine();

            String sql = "UPDATE Members SET MembershipType=?, EndDate=?, Status=? WHERE MemberID=?";
            PreparedStatement pst = conn.prepareStatement(sql);
            pst.setString(1, type);
            pst.setDate(2, Date.valueOf(end));
            pst.setString(3, status);
            pst.setInt(4, id);

            int rows = pst.executeUpdate();
            System.out.println(rows > 0 ? "Member updated." : "Member not found.");
        } catch (SQLException e) {
            System.out.println("Error updating member.");
        }
    }

    static void deleteMember() {
        try {
            System.out.print("Enter Member ID to delete: ");
            int id = Integer.parseInt(sc.nextLine());

            String sql = "DELETE FROM Members WHERE MemberID=?";
            PreparedStatement pst = conn.prepareStatement(sql);
            pst.setInt(1, id);

            int rows = pst.executeUpdate();
            System.out.println(rows > 0 ? "Member deleted." : "Member not found.");
        } catch (SQLException e) {
            System.out.println("Error deleting member.");
        }
    }
}
