// Java Program to Illustrate JDBC Connection In Oracle DB

// Importing database
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import oracle.jdbc.driver.OracleDriver;

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

        // Try block to check for exceptions
        try {

            // Loading and registering drivers
            // using DriverManager

            // Setting instance as Oracle driver
            // This implies database is Oracle
            DriverManager.registerDriver(
                new OracleDriver());

            // Passing DB- URL,username,password
            connection = DriverManager.getConnection(
                "jdbc:oracle:thin:@localhost:1521:xe",
                "username", "password");
        }

        // Catch block ot handle DB exception
        catch (SQLException e) {

            // Display the line number where exception
            // occurred using printStackTrace() method
            e.printStackTrace();
        }

        // If no exception caught database is connected
        return connection;

        // Display message successful connection
        System.out.print("Connection established");
    }
}