import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class temp {
    public static void main(String[] args) {
        try {
            // Load SQLite JDBC driver
            
            // SQLite database file (will create if not exists)
            Class.forName("org.sqlite.JDBC");
            String url = "jdbc:sqlite:Books.db";
            Connection conn = DriverManager.getConnection(url);
            Statement st = conn.createStatement();

            // Create dummy table similar to 'Authors'
            st.execute("CREATE TABLE IF NOT EXISTS Authors (lastName TEXT, firstName TEXT)");

            // Insert test data if empty
            st.execute("INSERT INTO Authors (lastName, firstName) SELECT 'Rehman', 'Basil' WHERE NOT EXISTS (SELECT 1 FROM Authors)");

            ResultSet rs = st.executeQuery("SELECT lastName, firstName FROM Authors");

            while (rs.next()) {
                System.out.println(rs.getString("lastName") + ", " + rs.getString("firstName"));
            }

            st.close();
            conn.close();
        } catch (ClassNotFoundException e) {
            System.out.println("Could not load JDBC driver: " + e);
        } catch (SQLException e) {
            System.out.println("SQL Exception: " + e);
        }
    }
}

// public class temp{
//     public static void main(String[] args){
//         try{
//             Class.forName("net.ucanaccess.jdbc.UcanaccessDriver");
//             String url = "jdbc:ucanaccess:Books.accdb";
//             Connection conn = DriverManager.getConnection(url);
//             Statement st = conn.createStatement();
//             ResultSet rs = st.executeQuery("select * from Authors");
//             st.close();
//             conn.close();
//         }
//         catch(ClassNotFoundException e){
//             System.out.println(e);
//         }
//         catch(SQLException e){
//             System.out.println(e);
//         }
//     }
// }