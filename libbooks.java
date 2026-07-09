import java.io.*;
import java.util.*;

class Book {
    private String title;
    private String author;
    private String isbn;
    private String genre;
    private int pages;
    private boolean isAvailable;

    public Book(String title, String author, String isbn, String genre, int pages, boolean isAvailable) {
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.genre = genre;
        this.pages = pages;
        this.isAvailable = isAvailable;
    }

    @Override
    public String toString() {
        return title + "," + author + "," + isbn + "," + genre + "," + pages + "," + (isAvailable ? "Available" : "Not Available");
    }

    public static Book fromString(String line) {
        String[] parts = line.split(",");
        return new Book(parts[0], parts[1], parts[2], parts[3], Integer.parseInt(parts[4]), parts[5].equalsIgnoreCase("Available"));
    }
}

public class libbooks {
    private static final String FILE_NAME = "LibraryBooks.txt";

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        List<Book> books = new ArrayList<>();

        for (int i = 0; i < 3; i++) {
            System.out.println("Enter book " + (i + 1) + " details:");

            System.out.print("Title: ");
            String title = sc.nextLine();

            System.out.print("Author: ");
            String author = sc.nextLine();

            System.out.print("ISBN: ");
            String isbn = sc.nextLine();

            System.out.print("Genre: ");
            String genre = sc.nextLine();

            System.out.print("Number of Pages: ");
            int pages = Integer.parseInt(sc.nextLine());

            System.out.print("Is Available (true/false): ");
            boolean isAvailable = Boolean.parseBoolean(sc.nextLine());

            books.add(new Book(title, author, isbn, genre, pages, isAvailable));
        }

        // Write to file
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_NAME))) {
            for (Book b : books) {
                writer.write(b.toString());
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error writing to file.");
        }

        // Read and display file contents
        System.out.println("\nContents of " + FILE_NAME + ":");
        try (BufferedReader reader = new BufferedReader(new FileReader(FILE_NAME))) {
            String line;
            while ((line = reader.readLine()) != null) {
                Book book = Book.fromString(line);
                System.out.println(book.toString());
            }
        } catch (IOException e) {
            System.out.println("Error reading file.");
        }
    }
}
