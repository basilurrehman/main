import java.sql.*;

public class SampleDBApp {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/SampleDB";
        String user = "admin";
        String password = "admin123";

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            Connection conn = DriverManager.getConnection(url, user, password);
            System.out.println("Connected successfully!");

            Statement stmt = conn.createStatement();
            stmt.execute("CREATE TABLE IF NOT EXISTS Test (id INT PRIMARY KEY, name VARCHAR(50))");
            stmt.execute("INSERT INTO Test VALUES (1, 'Alice')");
            ResultSet rs = stmt.executeQuery("SELECT * FROM Test");

            while (rs.next()) {
                System.out.println(rs.getInt("id") + " - " + rs.getString("name"));
            }

            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

