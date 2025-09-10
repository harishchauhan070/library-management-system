# Library Management System

A command-line-based Library Management System (LMS) built with Python and SQLite. This application helps librarians manage their inventory, members, and book borrowing/returning processes efficiently.

## Features

-   **Book Management**: Add, update, delete, and view all books in the library.
-   **Member Management**: Add, update, and view library members.
-   **Transaction Processing**: Handle borrowing and returning of books.
-   **Search Functionality**: Search for books by title, author, or ISBN.
-   **Data Persistence**: All data is saved in an SQLite database.
-   **Simple CLI Menu**: Easy-to-use text-based interface.

## Tech Stack

-   **Language**: Python 3
-   **Database**: SQLite3
-   **Libraries**: `sqlite3` (standard library), `datetime`

## Project Structure
library-management-system/
│
├── library.py # Main application script
├── library.db # SQLite database (auto-generated on first run)
├── requirements.txt # Project dependencies (none beyond standard library)
└── README.md # Project documentation (this file)

## Installation & Usage

1.  **Clone the repository**
    ```bash
    git clone https://github.com/<your-username>/library-management-system.git
    cd library-management-system
    ```

2.  **Run the application**
    ```bash
    python library.py
    ```

3.  **Follow the menu prompts** to manage your library.

## Database Schema

The system uses three main tables:
-   `books`: Stores book details (ISBN, Title, Author, Quantity).
-   `members`: Stores member details (ID, Name, Contact).
-   `transactions`: Records all borrow/return transactions (Book ISBN, Member ID, Borrow Date, Return Date).

## Code Overview

The main script (`library.py`) handles:
-   Database connection and table creation.
-   A main menu loop with options for Books, Members, and Transactions.
-   Functions for each core operation (add, view, update, delete, borrow, return).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Future Enhancements

-   [ ] Implement a GUI using Tkinter or PyQt.
-   [ ] Add email reminders for overdue books.
-   [ ] Generate reports (e.g., popular books, overdue books).
-   [ ] Add user authentication for librarians.

## License

This project is licensed under the MIT License.
