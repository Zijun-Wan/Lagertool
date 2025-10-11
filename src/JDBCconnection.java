// Java Program to Illustrate JDBC Connection In Oracle DB

// Importing database
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

// Class 1
// JDBC Connection Class
// To communicate with the database
// Note: This class is to be used in Application class
// where moto of this class is connection object
public class JDBCconnection {

    // Declaring connection class object and
    // initializing it to null
    private static Connection connection = null;

    // Method
    // Static method that connects with database
    public static Connection getConnection()
    {
        try {
            // Connect to SQLite database (creates file if it doesn't exist in the docker container hopefully)
            connection = DriverManager.getConnection("jdbc:sqlite:/app/database.db");
            System.out.println("Connection established");
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return connection;
    }
}