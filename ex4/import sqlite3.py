import sqlite3

# Create the database and tables
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create Books table
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                    BookID INTEGER PRIMARY KEY,
                    Title TEXT,
                    Author TEXT,
                    ISBN TEXT,
                    Status TEXT
                )''')

# Create Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    UserID INTEGER PRIMARY KEY,
                    Name TEXT,
                    Email TEXT
                )''')

# Create Reservations table
cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID INTEGER PRIMARY KEY,
                    BookID INTEGER,
                    UserID INTEGER,
                    ReservationDate TEXT,
                    FOREIGN KEY (BookID) REFERENCES Books(BookID),
                    FOREIGN KEY (UserID) REFERENCES Users(UserID)
                )''')

# Function to add a new book to the database
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")
    status = input("Enter the status of the book: ")
    
    cursor.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)",
                   (title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")

# Function to find a book's detail based on BookID
def find_book_by_id():
    book_id = input("Enter the BookID: ")
    
    cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                      Users.UserID, Users.Name, Users.Email
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID
                      WHERE Books.BookID = ?''', (book_id,))
    
    result = cursor.fetchone()
    if result:
        book_id, title, author, isbn, status, user_id, name, email = result
        print(f"BookID: {book_id}")
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"ISBN: {isbn}")
        print(f"Status: {status}")
        if user_id:
            print("Reserved by:")
            print(f"UserID: {user_id}")
            print(f"Name: {name}")
            print(f"Email: {email}")
    else:
        print("Book not found!")

# Function to find a book's reservation status based on BookID, Title, UserID, or ReservationID
def find_reservation_status():
    text = input("Enter the text (BookID, Title, UserID, or ReservationID): ")
    
    if text.startswith("LB"):  # BookID
        cursor.execute('''SELECT Books.BookID, Books.Title, Books.Status,
                          Users.UserID, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Books.BookID = ?''', (text,))
    elif text.startswith("LU"):  # UserID
        cursor.execute('''SELECT Books.BookID, Books.Title, Books.Status,
                          Users.UserID, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Users.UserID = ?''', (text,))
    elif text.startswith("LR"):  # ReservationID
        cursor.execute('''SELECT Books.BookID, Books.Title, Books.Status,
                          Users.UserID, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Reservations.ReservationID = ?''', (text,))
    else:  # Title
        cursor.execute('''SELECT Books.BookID, Books.Title, Books.Status,
                          Users.UserID, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Books.Title = ?''', (text,))
    
    results = cursor.fetchall()
    if results:
        for result in results:
            book_id, title, status, user_id, name, email = result
            print(f"BookID: {book_id}")
            print(f"Title: {title}")
            print(f"Status: {status}")
            if user_id:
                print("Reserved by:")
                print(f"UserID: {user_id}")
                print(f"Name: {name}")
                print(f"Email: {email}")
            print()
    else:
        print("Book not found!")

# Function to find all the books in the database
def find_all_books():
    cursor.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status,
                      Users.UserID, Users.Name, Users.Email
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    
    results = cursor.fetchall()
    if results:
        for result in results:
            book_id, title, author, isbn, status, user_id, name, email = result
            print(f"BookID: {book_id}")
            print(f"Title: {title}")
            print(f"Author: {author}")
            print(f"ISBN: {isbn}")
            print(f"Status: {status}")
            if user_id:
                print("Reserved by:")
                print(f"UserID: {user_id}")
                print(f"Name: {name}")
                print(f"Email: {email}")
            print()
    else:
        print("No books found!")

# Function to modify/update book details based on BookID
def update_book_details():
    book_id = input("Enter the BookID: ")
    new_status = input("Enter the new status: ")
    
    cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
    cursor.execute("UPDATE Reservations SET Status = ? WHERE BookID = ?", (new_status, book_id))
    conn.commit()
    print("Book details updated successfully!")

# Function to delete a book based on its BookID
def delete_book():
    book_id = input("Enter the BookID: ")
    
    cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
    cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
    conn.commit()
    print("Book deleted successfully!")

# Main function
def main():
    while True:
        print("Library Management System")
        print("1. Add a new book")
        print("2. Find a book's detail based on BookID")
        print("3. Find a book's reservation status")
        print("4. Find all the books in the database")
        print("5. Modify/update book details")
        print("6. Delete a book")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_book()
        elif choice == "2":
            find_book_by_id()
        elif choice == "3":
            find_reservation_status()
        elif choice == "4":
            find_all_books()
        elif choice == "5":
            update_book_details()
        elif choice == "6":
            delete_book()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")
        
        print()

# Call the main function
if __name__ == "__main__":
    main()

# Close the database connection
conn.close()