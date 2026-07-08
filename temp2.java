import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.FileOutputStream;
import java.io.File;
import java.util.InputMismatchException;
import java.util.Scanner;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.SQLException;
import java.sql.ResultSet;
public class temp2{
    static final String USER = "gymuser"; // or your MySQL username
    static final String PASS = "gympass"; 
    public static void main(String[] args) throws FileNotFoundException,InputMismatchException{
        // PrintWriter pw = new PrintWriter(new FileOutputStream("temp2.txt",true));
        // pw.println("hello1");
        // pw.close();
        // Scanner sc = new Scanner(new FileInputStream("temp2.txt"));
        // System.out.println(sc.next());
        // Scanner sc2 = new Scanner(System.in);
        // sc2.nextInt();
        // Scanner sc =  new Scanner(new File("temp2.txt"));
        try {
            // Class.forName("net.ucanaccess.jdbc.UcanaccessDriver");
            Class.forName("com.mysql.cj.jdbc.Driver");
            // String url = "jdbc:ucanaccess:Books.db";
            
            String url = "jdbc:mysql://localhost:3306/GymDB";
            Connection conn = DriverManager.getConnection(url,USER,PASS);
            Statement st = conn.createStatement();
            st.execute("INSERT INTO Members (Name, Status) VALUES (Basil, active)");
            ResultSet rs = st.executeQuery("SELECT * FROM Members WHERE Status = 'active'");
            rs.next();
            System.out.println(rs.getString("Name"));
        } catch (ClassNotFoundException ez) {
            // TODO Auto-generated catch block
            ez.printStackTrace();
        } catch(SQLException e){
            System.out.println("hello"+e);
        }
        
    }
}