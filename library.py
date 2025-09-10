import sqlite3
from datetime import datetime

class LibraryManagementSystem:
    def __init__(self, db_name='library.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates the necessary tables in the database if they don't exist."""
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                quantity INTEGER DEFAULT 1
            )
        ''')
       
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT
            )
        ''')
       
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_isbn TEXT NOT NULL,
                member_id INTEGER NOT NULL,
                borrow_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (book_isbn) REFERENCES books (isbn),
                FOREIGN KEY (member_id) REFERENCES members (id)
            )
        ''')
        self.conn.commit()

   
    def add_book(self):
        isbn = input("Enter ISBN: ")
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            return

        try:
            self.cursor.execute("INSERT INTO books (isbn, title, author, quantity) VALUES (?, ?, ?, ?)",
                               (isbn, title, author, quantity))
            self.conn.commit()
            print("Book added successfully!")
        except sqlite3.IntegrityError:
            print("Error: A book with this ISBN already exists.")

    def view_books(self):
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        if not books:
            print("No books in the library.")
            return
        print("\n--- Library Books ---")
        for book in books:
            print(f"ISBN: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available: {book[3]}")

    def update_book_quantity(self):
        isbn = input("Enter ISBN of the book to update: ")
        try:
            new_quantity = int(input("Enter new quantity: "))
        except ValueError:
            print("Invalid quantity.")
            return

        self.cursor.execute("UPDATE books SET quantity = ? WHERE isbn = ?", (new_quantity, isbn))
        if self.cursor.rowcount == 0:
            print("Book not found.")
        else:
            self.conn.commit()
            print("Book quantity updated successfully.")

    def delete_book(self):
        isbn = input("Enter ISBN of the book to delete: ")
        self.cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        if self.cursor.rowcount == 0:
            print("Book not found.")
        else:
            self.conn.commit()
            print("Book deleted successfully.")

   
    def add_member(self):
        name = input("Enter member name: ")
        contact = input("Enter contact info: ")
        self.cursor.execute("INSERT INTO members (name, contact) VALUES (?, ?)", (name, contact))
        self.conn.commit()
        print("Member added successfully!")

    def view_members(self):
        self.cursor.execute("SELECT * FROM members")
        members = self.cursor.fetchall()
        if not members:
            print("No members registered.")
            return
        print("\n--- Library Members ---")
        for member in members:
            print(f"ID: {member[0]}, Name: {member[1]}, Contact: {member[2]}")


    def borrow_book(self):
        member_id = input("Enter your member ID: ")
        isbn = input("Enter ISBN of the book to borrow: ")


        self.cursor.execute("SELECT quantity FROM books WHERE isbn = ?", (isbn,))
        result = self.cursor.fetchone()
        if not result or result[0] < 1:
            print("Book is not available for borrowing.")
            return


        self.cursor.execute("SELECT id FROM members WHERE id = ?", (member_id,))
        if not self.cursor.fetchone():
            print("Invalid member ID.")
            return

        borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute("INSERT INTO transactions (book_isbn, member_id, borrow_date) VALUES (?, ?, ?)",
                               (isbn, member_id, borrow_date))
     
            self.cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE isbn = ?", (isbn,))
            self.conn.commit()
            print("Book borrowed successfully! Please return on time.")
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def return_book(self):
        isbn = input("Enter ISBN of the book to return: ")
        member_id = input("Enter your member ID: ")

     
        self.cursor.execute('''SELECT id FROM transactions 
                            WHERE book_isbn=? AND member_id=? AND return_date IS NULL''',
                            (isbn, member_id))
        transaction = self.cursor.fetchone()
        if not transaction:
            print("No active borrowing record found for this book and member.")
            return

        return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Update transaction with return date
        self.cursor.execute("UPDATE transactions SET return_date=? WHERE id=?",
                           (return_date, transaction[0]))
   
        self.cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE isbn = ?", (isbn,))
        self.conn.commit()
        print("Book returned successfully. Thank you!")

    def search_books(self):
        search_term = input("Enter title, author, or ISBN to search: ")
        query = "%" + search_term + "%"
        self.cursor.execute('''SELECT * FROM books 
                            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?''',
                            (query, query, query))
        books = self.cursor.fetchall()
        if not books:
            print("No matching books found.")
            return
        print("\n--- Search Results ---")
        for book in books:
            print(f"ISBN: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available: {book[3]}")


    def main_menu(self):
        while True:
            print("\n===== Library Management System =====")
            print("1. Book Operations")
            print("2. Member Operations")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. Search Books")
            print("6. Exit")
            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                self.book_operations_menu()
            elif choice == '2':
                self.member_operations_menu()
            elif choice == '3':
                self.borrow_book()
            elif choice == '4':
                self.return_book()
            elif choice == '5':
                self.search_books()
            elif choice == '6':
                print("Thank you for using the Library Management System!")
                self.conn.close()
                break
            else:
                print("Invalid choice. Please try again.")

    def book_operations_menu(self):
        while True:
            print("\n--- Book Operations ---")
            print("1. Add New Book")
            print("2. View All Books")
            print("3. Update Book Quantity")
            print("4. Delete Book")
            print("5. Back to Main Menu")
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.view_books()
            elif choice == '3':
                self.update_book_quantity()
            elif choice == '4':
                self.delete_book()
            elif choice == '5':
                break
            else:
                print("Invalid choice.")

    def member_operations_menu(self):
        while True:
            print("\n--- Member Operations ---")
            print("1. Add New Member")
            print("2. View All Members")
            print("3. Back to Main Menu")
            choice = input("Enter your choice (1-3): ")

            if choice == '1':
                self.add_member()
            elif choice == '2':
                self.view_members()
            elif choice == '3':
                break
            else:
                print("Invalid choice.")

if __name__ == "__main__":
    lms = LibraryManagementSystem()
    lms.main_menu()
