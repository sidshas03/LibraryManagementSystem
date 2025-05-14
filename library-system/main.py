
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class LibraryManagementSystem:
    def __init__(self):
        self.conn = sqlite3.connect('library.db')
        self.create_tables()
        self.setup_ui()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                membership_date DATE
            )
        ''')

        # Create Books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                quantity INTEGER,
                available INTEGER
            )
        ''')

        # Create Loans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS loans (
                loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id INTEGER,
                loan_date DATE,
                due_date DATE,
                return_date DATE,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (book_id) REFERENCES books (book_id)
            )
        ''')
        
        self.conn.commit()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("800x600")

        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True)

        # Users tab
        users_frame = ttk.Frame(notebook)
        notebook.add(users_frame, text="Users")
        self.setup_users_tab(users_frame)

        # Books tab
        books_frame = ttk.Frame(notebook)
        notebook.add(books_frame, text="Books")
        self.setup_books_tab(books_frame)

        # Loans tab
        loans_frame = ttk.Frame(notebook)
        notebook.add(loans_frame, text="Loans")
        self.setup_loans_tab(loans_frame)

    def setup_users_tab(self, parent):
        # Add user form
        ttk.Label(parent, text="Add New User").grid(row=0, column=0, pady=10)
        
        ttk.Label(parent, text="Name:").grid(row=1, column=0)
        name_entry = ttk.Entry(parent)
        name_entry.grid(row=1, column=1)

        ttk.Label(parent, text="Email:").grid(row=2, column=0)
        email_entry = ttk.Entry(parent)
        email_entry.grid(row=2, column=1)

        ttk.Button(parent, text="Add User", 
                  command=lambda: self.add_user(name_entry.get(), email_entry.get())
                  ).grid(row=3, column=0, columnspan=2, pady=10)

        # User list
        self.users_tree = ttk.Treeview(parent, columns=("ID", "Name", "Email"), show="headings")
        self.users_tree.grid(row=4, column=0, columnspan=2, pady=10)
        self.users_tree.heading("ID", text="ID")
        self.users_tree.heading("Name", text="Name")
        self.users_tree.heading("Email", text="Email")

    def setup_books_tab(self, parent):
        # Add book form
        ttk.Label(parent, text="Add New Book").grid(row=0, column=0, pady=10)
        
        ttk.Label(parent, text="Title:").grid(row=1, column=0)
        title_entry = ttk.Entry(parent)
        title_entry.grid(row=1, column=1)

        ttk.Label(parent, text="Author:").grid(row=2, column=0)
        author_entry = ttk.Entry(parent)
        author_entry.grid(row=2, column=1)

        ttk.Button(parent, text="Add Book", 
                  command=lambda: self.add_book(title_entry.get(), author_entry.get())
                  ).grid(row=3, column=0, columnspan=2, pady=10)

        # Book list
        self.books_tree = ttk.Treeview(parent, columns=("ID", "Title", "Author", "Available"), show="headings")
        self.books_tree.grid(row=4, column=0, columnspan=2, pady=10)
        self.books_tree.heading("ID", text="ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Author", text="Author")
        self.books_tree.heading("Available", text="Available")

    def setup_loans_tab(self, parent):
        # Create loan form
        ttk.Label(parent, text="Create New Loan").grid(row=0, column=0, pady=10)
        
        ttk.Label(parent, text="User ID:").grid(row=1, column=0)
        user_id_entry = ttk.Entry(parent)
        user_id_entry.grid(row=1, column=1)

        ttk.Label(parent, text="Book ID:").grid(row=2, column=0)
        book_id_entry = ttk.Entry(parent)
        book_id_entry.grid(row=2, column=1)

        ttk.Button(parent, text="Create Loan", 
                  command=lambda: self.create_loan(user_id_entry.get(), book_id_entry.get())
                  ).grid(row=3, column=0, columnspan=2, pady=10)

        # Loan list
        self.loans_tree = ttk.Treeview(parent, 
                                     columns=("ID", "User", "Book", "Loan Date", "Due Date"),
                                     show="headings")
        self.loans_tree.grid(row=4, column=0, columnspan=2, pady=10)
        self.loans_tree.heading("ID", text="ID")
        self.loans_tree.heading("User", text="User")
        self.loans_tree.heading("Book", text="Book")
        self.loans_tree.heading("Loan Date", text="Loan Date")
        self.loans_tree.heading("Due Date", text="Due Date")

    def add_user(self, name, email):
        if not name or not email:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (name, email, membership_date)
                VALUES (?, ?, ?)
            ''', (name, email, datetime.now().date()))
            self.conn.commit()
            messagebox.showinfo("Success", "User added successfully")
            self.refresh_users_list()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists")

    def add_book(self, title, author):
        if not title or not author:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, quantity, available)
            VALUES (?, ?, 1, 1)
        ''', (title, author))
        self.conn.commit()
        messagebox.showinfo("Success", "Book added successfully")
        self.refresh_books_list()

    def create_loan(self, user_id, book_id):
        if not user_id or not book_id:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        cursor = self.conn.cursor()
        try:
            # Check if book is available
            cursor.execute('SELECT available FROM books WHERE book_id = ?', (book_id,))
            result = cursor.fetchone()
            if not result or result[0] <= 0:
                messagebox.showerror("Error", "Book not available")
                return

            # Create loan and update book availability
            loan_date = datetime.now().date()
            due_date = datetime.now().date()  # Add logic for due date calculation
            
            cursor.execute('''
                INSERT INTO loans (user_id, book_id, loan_date, due_date)
                VALUES (?, ?, ?, ?)
            ''', (user_id, book_id, loan_date, due_date))
            
            cursor.execute('''
                UPDATE books 
                SET available = available - 1 
                WHERE book_id = ?
            ''', (book_id,))
            
            self.conn.commit()
            messagebox.showinfo("Success", "Loan created successfully")
            self.refresh_loans_list()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def refresh_users_list(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT user_id, name, email FROM users')
        for row in cursor.fetchall():
            self.users_tree.insert('', 'end', values=row)

    def refresh_books_list(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute('SELECT book_id, title, author, available FROM books')
        for row in cursor.fetchall():
            self.books_tree.insert('', 'end', values=row)

    def refresh_loans_list(self):
        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT l.loan_id, u.name, b.title, l.loan_date, l.due_date
            FROM loans l
            JOIN users u ON l.user_id = u.user_id
            JOIN books b ON l.book_id = b.book_id
            WHERE l.return_date IS NULL
        ''')
        for row in cursor.fetchall():
            self.loans_tree.insert('', 'end', values=row)

    def run(self):
        self.refresh_users_list()
        self.refresh_books_list()
        self.refresh_loans_list()
        self.root.mainloop()

if __name__ == "__main__":
    app = LibraryManagementSystem()
    app.run()
