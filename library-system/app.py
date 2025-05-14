import sqlite3
from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_NAME = 'library.db'

# Hardcoded login users
LOGIN_USERS = {
    'admin': 'admin123',
    'sid': 'sid123',
}

BOOK_ICONS = [
    # Emojis
    '📚', '📖', '📘', '📙', '📗', '📕', '📒', '📓',
    # Book cover images (royalty-free/unsplash)
    'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1455885664032-7cbbda5dfd0e?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1465101178521-c1a9136a3b99?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1463320898484-cdee8141c787?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=200&q=80',
    # Flat icon images
    'https://img.icons8.com/color/96/000000/book.png',
    'https://img.icons8.com/color/96/000000/open-book--v2.png',
    'https://img.icons8.com/color/96/000000/books.png',
]

BOOK_IMAGES = [
    'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1455885664032-7cbbda5dfd0e?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1465101178521-c1a9136a3b99?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1463320898484-cdee8141c787?auto=format&fit=crop&w=200&q=80',
    'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=200&q=80',
    'https://img.icons8.com/color/96/000000/book.png',
    'https://img.icons8.com/color/96/000000/open-book--v2.png',
    'https://img.icons8.com/color/96/000000/books.png',
]

USER_NAMES = [
    'Alice Johnson', 'Bob Smith', 'Charlie Lee', 'Diana Evans', 'Ethan Brown', 'Fiona Clark', 'George Miller',
    'Hannah Wilson', 'Ian Moore', 'Julia Taylor', 'Kevin Anderson', 'Laura Thomas', 'Mike Harris', 'Nina Martin',
    'Oscar Lewis', 'Paula Walker', 'Quentin Young', 'Rachel King', 'Sam Scott', 'Tina Adams', 'Uma Baker',
    'Victor Carter', 'Wendy Davis', 'Xander Edwards', 'Yara Foster', 'Zane Green', 'Amber Hall', 'Brian Ingram',
    'Cathy James', 'David Knight'
]

BOOK_TITLES = [
    ('To Kill a Mockingbird', 'Harper Lee'),
    ('1984', 'George Orwell'),
    ('The Great Gatsby', 'F. Scott Fitzgerald'),
    ('The Catcher in the Rye', 'J.D. Salinger'),
    ('Pride and Prejudice', 'Jane Austen'),
    ('The Hobbit', 'J.R.R. Tolkien'),
    ('Moby Dick', 'Herman Melville'),
    ('War and Peace', 'Leo Tolstoy'),
    ('The Odyssey', 'Homer'),
    ('Crime and Punishment', 'Fyodor Dostoevsky'),
    ('Brave New World', 'Aldous Huxley'),
    ('Jane Eyre', 'Charlotte Brontë'),
    ('Wuthering Heights', 'Emily Brontë'),
    ('The Lord of the Rings', 'J.R.R. Tolkien'),
    ('Animal Farm', 'George Orwell'),
    ('The Alchemist', 'Paulo Coelho'),
    ('The Book Thief', 'Markus Zusak'),
    ('Great Expectations', 'Charles Dickens'),
    ('Little Women', 'Louisa May Alcott'),
    ('Dracula', 'Bram Stoker'),
    ('The Kite Runner', 'Khaled Hosseini'),
    ('The Da Vinci Code', 'Dan Brown'),
    ('The Hunger Games', 'Suzanne Collins'),
    ('Gone Girl', 'Gillian Flynn'),
    ('The Girl with the Dragon Tattoo', 'Stieg Larsson'),
    ('Memoirs of a Geisha', 'Arthur Golden'),
    ('The Fault in Our Stars', 'John Green'),
    ('Life of Pi', 'Yann Martel'),
    ('A Tale of Two Cities', 'Charles Dickens'),
    ('The Shining', 'Stephen King')
]

# HTML Templates (using Jinja2)
base_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    <style>
        body { background: linear-gradient(135deg, #f8fafc 0%, #e3f0ff 100%); }
        .library-hero {
            background: linear-gradient(120deg, #1a237e99 0%, #3949abcc 100%), url('https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
            color: #fff;
            padding: 3rem 1rem 2rem 1rem;
            text-shadow: 0 2px 8px #0008;
            border-radius: 0 0 2rem 2rem;
            box-shadow: 0 8px 32px #0002;
            position: relative;
        }
        .library-navbar {
            background: linear-gradient(90deg, #1a237e 60%, #ffd600 100%) !important;
            box-shadow: 0 2px 8px #0002;
        }
        .sidebar {
            background: linear-gradient(180deg, #283593 80%, #ffd600 100%);
            min-height: 100vh;
            color: #fff;
            box-shadow: 2px 0 8px #0001;
        }
        .sidebar .nav-link {
            color: #fff;
            font-weight: 500;
            transition: background 0.2s, color 0.2s;
        }
        .sidebar .nav-link.active, .sidebar .nav-link:hover {
            background: #ffd600;
            color: #1a237e;
        }
        .library-footer {
            background: linear-gradient(90deg, #1a237e 60%, #ffd600 100%);
            color: #fff;
            padding: 1rem 0;
            text-align: center;
            margin-top: 2rem;
            box-shadow: 0 -2px 8px #0002;
        }
        .book-card {
            min-width: 220px;
            max-width: 260px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 16px #3949ab22;
            border: 2px solid #ffd60022;
            border-radius: 1rem;
            transition: transform 0.15s, box-shadow 0.15s;
        }
        .book-card:hover {
            transform: translateY(-6px) scale(1.03);
            box-shadow: 0 8px 32px #3949ab44;
            border-color: #ffd600;
        }
        .book-icon {
            font-size: 2.5rem;
            height: 48px;
        }
        .book-img {
            width: 48px;
            height: 48px;
            object-fit: contain;
        }
        .login-bg {
            background: linear-gradient(120deg, #1a237e99 0%, #ffd600cc 100%), url('https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
            min-height: 100vh;
        }
        .btn-flashy {
            background: linear-gradient(90deg, #ffd600 0%, #ff9800 100%);
            color: #1a237e;
            font-weight: bold;
            box-shadow: 0 2px 8px #ffd60044;
            border: none;
        }
        .btn-flashy:hover {
            background: linear-gradient(90deg, #ff9800 0%, #ffd600 100%);
            color: #fff;
        }
        .table thead th {
            background: linear-gradient(90deg, #1a237e 60%, #ffd600 100%);
            color: #fff;
            border: none;
            font-size: 1.1rem;
        }
        .table-striped>tbody>tr:nth-of-type(odd) {
            background-color: #f3f6ff;
        }
        .table-striped>tbody>tr:hover {
            background-color: #ffe082;
            transition: background 0.2s;
        }
        .badge-flashy {
            background: linear-gradient(90deg, #ffd600 0%, #ff9800 100%);
            color: #1a237e;
            font-size: 1rem;
        }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg library-navbar mb-0">
  <div class="container-fluid">
    <a class="navbar-brand fw-bold d-flex align-items-center gap-2" href="/">
      <i class="bi bi-journal-bookmark-fill"></i> My Library
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        {% if session.get('user') %}
        <li class="nav-item"><a class="nav-link {% if request.path=='/dashboard' %}active{% endif %}" href="/dashboard"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
        <li class="nav-item"><a class="nav-link {% if request.path=='/books' %}active{% endif %}" href="/books"><i class="bi bi-book"></i> Books</a></li>
        <li class="nav-item"><a class="nav-link {% if request.path=='/authors' %}active{% endif %}" href="/authors"><i class="bi bi-person-lines-fill"></i> Authors</a></li>
        <li class="nav-item"><a class="nav-link {% if request.path=='/clients' %}active{% endif %}" href="/clients"><i class="bi bi-people"></i> Clients</a></li>
        <li class="nav-item"><a class="nav-link {% if request.path=='/events' %}active{% endif %}" href="/events"><i class="bi bi-calendar-event"></i> Events</a></li>
        <li class="nav-item"><a class="nav-link {% if request.path=='/rentals' %}active{% endif %}" href="/rentals"><i class="bi bi-arrow-left-right"></i> Rentals</a></li>
        <li class="nav-item"><a class="nav-link {% if request.path=='/users' %}active{% endif %}" href="/users"><i class="bi bi-person-badge"></i> Users</a></li>
        <li class="nav-item"><a class="nav-link {% if request.path=='/other' %}active{% endif %}" href="/other"><i class="bi bi-three-dots"></i> Other</a></li>
        {% endif %}
      </ul>
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
        {% if session.get('user') %}
        <li class="nav-item"><span class="navbar-text text-light me-2"><i class="bi bi-person-circle"></i> Signed in as {{ session['user'] }}</span></li>
        <li class="nav-item"><a class="nav-link" href="/logout"><i class="bi bi-box-arrow-right"></i> Logout</a></li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
{% if session.get('user') %}
<div class="row g-0">
  <div class="col-md-2 d-none d-md-block sidebar p-0">
    <div class="d-flex flex-column align-items-start p-3">
      <h5 class="fw-bold mb-4"><i class="bi bi-list-stars"></i> Navigation</h5>
      <a class="nav-link {% if request.path=='/dashboard' %}active{% endif %}" href="/dashboard"><i class="bi bi-speedometer2"></i> Dashboard</a>
      <a class="nav-link {% if request.path=='/books' %}active{% endif %}" href="/books"><i class="bi bi-book"></i> Books</a>
      <a class="nav-link {% if request.path=='/authors' %}active{% endif %}" href="/authors"><i class="bi bi-person-lines-fill"></i> Authors</a>
      <a class="nav-link {% if request.path=='/clients' %}active{% endif %}" href="/clients"><i class="bi bi-people"></i> Clients</a>
      <a class="nav-link {% if request.path=='/events' %}active{% endif %}" href="/events"><i class="bi bi-calendar-event"></i> Events</a>
      <a class="nav-link {% if request.path=='/rentals' %}active{% endif %}" href="/rentals"><i class="bi bi-arrow-left-right"></i> Rentals</a>
      <a class="nav-link {% if request.path=='/users' %}active{% endif %}" href="/users"><i class="bi bi-person-badge"></i> Users</a>
      <a class="nav-link {% if request.path=='/other' %}active{% endif %}" href="/other"><i class="bi bi-three-dots"></i> Other</a>
    </div>
  </div>
  <div class="col-md-10">
    <div class="library-hero mb-4 animate__animated animate__fadeInDown">
      <div class="container">
        <h1 class="display-4 fw-bold"><i class="bi bi-journal-bookmark-fill"></i> Welcome to My Library</h1>
        <p class="lead">Explore, borrow, and manage your favorite books with <span class="badge badge-flashy">style</span>!</p>
      </div>
    </div>
    <div class="container">
      {% with messages = get_flashed_messages() %}
        {% if messages %}
          <div class="alert alert-info animate__animated animate__fadeInDown">{{ messages[0] }}</div>
        {% endif %}
      {% endwith %}
      {{ content|safe }}
    </div>
  </div>
</div>
{% else %}
  {{ content|safe }}
{% endif %}
<footer class="library-footer">
  &copy; {{ 2024 }} My Library. All rights reserved.
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
</body>
</html>
'''

login_template = '''
<div class="login-bg d-flex align-items-center justify-content-center">
  <div class="card shadow-lg p-4" style="max-width: 400px; width: 100%; margin-top: 5vh;">
    <div class="card-body">
      <h2 class="mb-4 text-center">Welcome to My Library</h2>
      <form method="post">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" id="username" name="username" required>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" name="password" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">Sign In</button>
      </form>
    </div>
  </div>
</div>
'''

users_template = '''
<h2>Users</h2>
<form method="post" class="row g-3 mb-4">
  <div class="col-md-4">
    <input type="text" name="name" class="form-control" placeholder="Name" required>
  </div>
  <div class="col-md-4">
    <input type="email" name="email" class="form-control" placeholder="Email" required>
  </div>
  <div class="col-md-4">
    <button type="submit" class="btn btn-primary">Add User</button>
  </div>
</form>
<table class="table table-striped">
  <thead><tr><th>ID</th><th>Name</th><th>Email</th></tr></thead>
  <tbody>
    {% for user in users %}
      <tr><td>{{ user[0] }}</td><td>{{ user[1] }}</td><td>{{ user[2] }}</td></tr>
    {% endfor %}
  </tbody>
</table>
'''

books_template = '''
<h2 class="mb-4">Books</h2>
<form method="post" class="row g-3 mb-4">
  <div class="col-md-3">
    <input type="text" name="title" class="form-control" placeholder="Title" required>
  </div>
  <div class="col-md-3">
    <input type="text" name="author" class="form-control" placeholder="Author" required>
  </div>
  <div class="col-md-3">
    <button type="submit" class="btn btn-primary">Add Book</button>
  </div>
</form>
<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
  {% for book in books %}
    <div class="col">
      <div class="card book-card h-100">
        <div class="card-body d-flex flex-column align-items-center">
          <img src="{{ book[4] }}" class="book-img mb-2" alt="Book Cover">
          <h5 class="card-title text-center">{{ book[1] }}</h5>
          <p class="card-text text-center text-muted">by {{ book[2] }}</p>
          <span class="badge bg-{{ 'success' if book[3] > 0 else 'danger' }} mt-2">{{ book[3] }} available</span>
        </div>
      </div>
    </div>
  {% endfor %}
</div>
'''

loans_template = '''
<h2>Loans</h2>
<form method="post" class="row g-3 mb-4">
  <div class="col-md-3">
    <input type="number" name="user_id" class="form-control" placeholder="User ID" required>
  </div>
  <div class="col-md-3">
    <input type="number" name="book_id" class="form-control" placeholder="Book ID" required>
  </div>
  <div class="col-md-3">
    <button type="submit" class="btn btn-primary">Create Loan</button>
  </div>
</form>
<table class="table table-striped">
  <thead><tr><th>ID</th><th>User</th><th>Book</th><th>Loan Date</th><th>Due Date</th></tr></thead>
  <tbody>
    {% for loan in loans %}
      <tr><td>{{ loan[0] }}</td><td>{{ loan[1] }}</td><td>{{ loan[2] }}</td><td>{{ loan[3] }}</td><td>{{ loan[4] }}</td></tr>
    {% endfor %}
  </tbody>
</table>
'''

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            membership_date DATE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            quantity INTEGER,
            available INTEGER,
            icon TEXT
        )
    ''')
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
    conn.commit()
    conn.close()

def add_sample_data():
    conn = get_db()
    cursor = conn.cursor()
    # Check if users table is empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        for i in range(30):
            name = USER_NAMES[i % len(USER_NAMES)]
            email = name.lower().replace(' ', '.') + f'{i+1}@example.com'
            cursor.execute('INSERT INTO users (name, email, membership_date) VALUES (?, ?, ?)',
                           (name, email, datetime(2023, 1, (i % 28) + 1).date()))
    # Check if books table is empty
    cursor.execute('SELECT COUNT(*) FROM books')
    if cursor.fetchone()[0] == 0:
        for i in range(30):
            title, author = BOOK_TITLES[i % len(BOOK_TITLES)]
            image = random.choice(BOOK_IMAGES)
            cursor.execute('INSERT INTO books (title, author, quantity, available, icon) VALUES (?, ?, ?, ?, ?)',
                           (title, author, 5, 5, image))
    # Check if loans table is empty
    cursor.execute('SELECT COUNT(*) FROM loans')
    if cursor.fetchone()[0] == 0:
        # Get user and book ids
        cursor.execute('SELECT user_id FROM users')
        user_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute('SELECT book_id FROM books')
        book_ids = [row[0] for row in cursor.fetchall()]
        for i in range(30):
            user_id = random.choice(user_ids)
            book_id = random.choice(book_ids)
            loan_date = datetime(2023, 2, (i % 28) + 1).date()
            due_date = datetime(2023, 3, (i % 28) + 1).date()
            cursor.execute('INSERT INTO loans (user_id, book_id, loan_date, due_date, return_date) VALUES (?, ?, ?, ?, NULL)',
                           (user_id, book_id, loan_date, due_date))
            cursor.execute('UPDATE books SET available = available - 1 WHERE book_id = ?', (book_id,))
    conn.commit()
    conn.close()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in LOGIN_USERS and LOGIN_USERS[username] == password:
            session['user'] = username
            flash('Signed in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    content = render_template_string(login_template)
    return render_template_string(base_template, content=content)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Signed out successfully!')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return redirect(url_for('users'))

@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name or not email:
            flash('Please fill all fields')
        else:
            try:
                cursor.execute('INSERT INTO users (name, email, membership_date) VALUES (?, ?, ?)',
                               (name, email, datetime.now().date()))
                conn.commit()
                flash('User added successfully')
            except sqlite3.IntegrityError:
                flash('Email already exists')
    cursor.execute('SELECT user_id, name, email FROM users')
    users = cursor.fetchall()
    conn.close()
    content = render_template_string(users_template, users=users)
    return render_template_string(base_template, content=content)

@app.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        if not title or not author:
            flash('Please fill all fields')
        else:
            image = random.choice(BOOK_IMAGES)
            cursor.execute('INSERT INTO books (title, author, quantity, available, icon) VALUES (?, ?, 1, 1, ?)',
                           (title, author, image))
            conn.commit()
            flash('Book added successfully')
    cursor.execute('SELECT book_id, title, author, available, icon FROM books')
    books = cursor.fetchall()
    conn.close()
    content = render_template_string(books_template, books=books)
    return render_template_string(base_template, content=content)

@app.route('/loans', methods=['GET', 'POST'])
@login_required
def loans():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        user_id = request.form['user_id']
        book_id = request.form['book_id']
        if not user_id or not book_id:
            flash('Please fill all fields')
        else:
            cursor.execute('SELECT available FROM books WHERE book_id = ?', (book_id,))
            result = cursor.fetchone()
            if not result or result['available'] <= 0:
                flash('Book not available')
            else:
                loan_date = datetime.now().date()
                due_date = datetime.now().date()  # You can add logic for due date calculation
                cursor.execute('INSERT INTO loans (user_id, book_id, loan_date, due_date) VALUES (?, ?, ?, ?)',
                               (user_id, book_id, loan_date, due_date))
                cursor.execute('UPDATE books SET available = available - 1 WHERE book_id = ?', (book_id,))
                conn.commit()
                flash('Loan created successfully')
    cursor.execute('''
        SELECT l.loan_id, u.name, b.title, l.loan_date, l.due_date
        FROM loans l
        JOIN users u ON l.user_id = u.user_id
        JOIN books b ON l.book_id = b.book_id
        WHERE l.return_date IS NULL
    ''')
    loans = cursor.fetchall()
    conn.close()
    content = render_template_string(loans_template, loans=loans)
    return render_template_string(base_template, content=content)

def nav_buttons(current):
    # Returns HTML for the navigation button group, highlighting the current page
    add_url = f"?add=1"
    return f'''
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div class="btn-group" role="group">
        <a href="/books" class="btn btn-outline-primary{' active' if current == 'books' else ''}"><i class="bi bi-book"></i> Books</a>
        <a href="/authors" class="btn btn-outline-primary{' active' if current == 'authors' else ''}"><i class="bi bi-person-lines-fill"></i> Authors</a>
        <a href="/clients" class="btn btn-outline-primary{' active' if current == 'clients' else ''}"><i class="bi bi-people"></i> Clients</a>
        <a href="/events" class="btn btn-outline-primary{' active' if current == 'events' else ''}"><i class="bi bi-calendar-event"></i> Events</a>
        <a href="/rentals" class="btn btn-outline-primary{' active' if current == 'rentals' else ''}"><i class="bi bi-arrow-left-right"></i> Rentals</a>
        <a href="/users" class="btn btn-outline-primary{' active' if current == 'users' else ''}"><i class="bi bi-person-badge"></i> Users</a>
        <a href="/other" class="btn btn-outline-primary{' active' if current == 'other' else ''}"><i class="bi bi-three-dots"></i> Other</a>
      </div>
      <a href="{request.path}?add=1" class="btn btn-flashy btn-lg ms-2"><i class="bi bi-plus-circle"></i> Add</a>
    </div>
    '''

@app.route('/authors', methods=['GET', 'POST'])
@login_required
def authors():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        em_add = request.form['em_add']
        add_c = request.form['add_c']
        add_s = request.form['add_s']
        add_ci = request.form['add_ci']
        add_str = request.form['add_str']
        cursor.execute('INSERT INTO ps_author (a_fname, a_lname, em_add, add_c, add_s, add_ci, add_str) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (fname, lname, em_add, add_c, add_s, add_ci, add_str))
        conn.commit()
        return redirect(url_for('authors'))
    cursor.execute('SELECT a_id, a_fname, a_lname, em_add, add_c, add_s, add_ci, add_str FROM ps_author')
    authors = cursor.fetchall()
    conn.close()
    show_add = request.args.get('add') == '1'
    authors_template = f'''
    {nav_buttons('authors')}
    {{% if show_add %}}
    <form method="post" class="row g-2 mb-3">
      <div class="col-md-2"><input name="fname" class="form-control" placeholder="First Name" required></div>
      <div class="col-md-2"><input name="lname" class="form-control" placeholder="Last Name" required></div>
      <div class="col-md-2"><input name="em_add" class="form-control" placeholder="Email"></div>
      <div class="col-md-1"><input name="add_c" class="form-control" placeholder="Country"></div>
      <div class="col-md-1"><input name="add_s" class="form-control" placeholder="State"></div>
      <div class="col-md-1"><input name="add_ci" class="form-control" placeholder="City"></div>
      <div class="col-md-2"><input name="add_str" class="form-control" placeholder="Street"></div>
      <div class="col-md-1"><button class="btn btn-success w-100">Add</button></div>
    </form>
    {{% endif %}}
    <h2>Authors</h2>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>ID</th><th>First Name</th><th>Last Name</th><th>Email</th>
          <th>Country</th><th>State</th><th>City</th><th>Street</th>
        </tr>
      </thead>
      <tbody>
        {{% for a in authors %}}
        <tr>
          <td>{{{{ a[0] }}}}</td><td>{{{{ a[1] }}}}</td><td>{{{{ a[2] }}}}</td><td>{{{{ a[3] }}}}</td>
          <td>{{{{ a[4] }}}}</td><td>{{{{ a[5] }}}}</td><td>{{{{ a[6] }}}}</td><td>{{{{ a[7] }}}}</td>
        </tr>
        {{% endfor %}}
      </tbody>
    </table>
    '''
    content = render_template_string(authors_template, authors=authors, show_add=show_add)
    return render_template_string(base_template, content=content)

@app.route('/psbooks', methods=['GET', 'POST'])
@login_required
def psbooks():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        bname = request.form['bname']
        top_id = request.form['top_id'] or None
        cursor.execute('INSERT INTO ps_book (bname, top_id) VALUES (?, ?)', (bname, top_id))
        conn.commit()
        return redirect(url_for('psbooks'))
    cursor.execute('SELECT b_id, bname, top_id FROM ps_book')
    books = cursor.fetchall()
    conn.close()
    show_add = request.args.get('add') == '1'
    books_template = f'''
    {nav_buttons('psbooks')}
    {{% if show_add %}}
    <form method="post" class="row g-2 mb-3">
      <div class="col-md-6"><input name="bname" class="form-control" placeholder="Book Title" required></div>
      <div class="col-md-4"><input name="top_id" class="form-control" placeholder="Topic ID (optional)"></div>
      <div class="col-md-2"><button class="btn btn-success w-100">Add</button></div>
    </form>
    {{% endif %}}
    <h2>Books</h2>
    <table class="table table-striped">
      <thead>
        <tr><th>ID</th><th>Title</th><th>Topic ID</th></tr>
      </thead>
      <tbody>
        {{% for b in books %}}
        <tr><td>{{{{ b[0] }}}}</td><td>{{{{ b[1] }}}}</td><td>{{{{ b[2] }}}}</td></tr>
        {{% endfor %}}
      </tbody>
    </table>
    '''
    content = render_template_string(books_template, books=books, show_add=show_add)
    return render_template_string(base_template, content=content)

@app.route('/clients', methods=['GET', 'POST'])
@login_required
def clients():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        phone_num = request.form['phone_num']
        email = request.form['email']
        id_ty = request.form['id_ty']
        re_id = request.form['re_id'] or None
        cursor.execute('INSERT INTO ps_client (fname, lname, phone_num, email, id_ty, re_id) VALUES (?, ?, ?, ?, ?, ?)',
                       (fname, lname, phone_num, email, id_ty, re_id))
        conn.commit()
        return redirect(url_for('clients'))
    cursor.execute('SELECT c_id, fname, lname, phone_num, email, id_ty, re_id FROM ps_client')
    clients = cursor.fetchall()
    conn.close()
    show_add = request.args.get('add') == '1'
    clients_template = f'''
    {nav_buttons('clients')}
    {{% if show_add %}}
    <form method="post" class="row g-2 mb-3">
      <div class="col-md-2"><input name="fname" class="form-control" placeholder="First Name" required></div>
      <div class="col-md-2"><input name="lname" class="form-control" placeholder="Last Name" required></div>
      <div class="col-md-2"><input name="phone_num" class="form-control" placeholder="Phone"></div>
      <div class="col-md-2"><input name="email" class="form-control" placeholder="Email"></div>
      <div class="col-md-2"><input name="id_ty" class="form-control" placeholder="ID Type"></div>
      <div class="col-md-1"><input name="re_id" class="form-control" placeholder="Reserve ID"></div>
      <div class="col-md-1"><button class="btn btn-success w-100">Add</button></div>
    </form>
    {{% endif %}}
    <h2>Clients</h2>
    <table class="table table-striped">
      <thead>
        <tr><th>ID</th><th>First Name</th><th>Last Name</th><th>Phone</th><th>Email</th><th>ID Type</th><th>Reserve ID</th></tr>
      </thead>
      <tbody>
        {{% for c in clients %}}
        <tr><td>{{{{ c[0] }}}}</td><td>{{{{ c[1] }}}}</td><td>{{{{ c[2] }}}}</td><td>{{{{ c[3] }}}}</td><td>{{{{ c[4] }}}}</td><td>{{{{ c[5] }}}}</td><td>{{{{ c[6] }}}}</td></tr>
        {{% endfor %}}
      </tbody>
    </table>
    '''
    content = render_template_string(clients_template, clients=clients, show_add=show_add)
    return render_template_string(base_template, content=content)

@app.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        s_date = request.form['s_date']
        eve_type = request.form['eve_type']
        e_date = request.form['e_date']
        top_id = request.form['top_id'] or None
        cursor.execute('INSERT INTO ps_event (name, s_date, eve_type, e_date, top_id) VALUES (?, ?, ?, ?, ?)',
                       (name, s_date, eve_type, e_date, top_id))
        conn.commit()
        return redirect(url_for('events'))
    cursor.execute('SELECT eve_id, name, s_date, eve_type, e_date, top_id FROM ps_event')
    events = cursor.fetchall()
    conn.close()
    show_add = request.args.get('add') == '1'
    events_template = f'''
    {nav_buttons('events')}
    {{% if show_add %}}
    <form method="post" class="row g-2 mb-3">
      <div class="col-md-3"><input name="name" class="form-control" placeholder="Event Name" required></div>
      <div class="col-md-2"><input name="s_date" class="form-control" placeholder="Start Date (YYYY-MM-DD)"></div>
      <div class="col-md-2"><input name="eve_type" class="form-control" placeholder="Type"></div>
      <div class="col-md-2"><input name="e_date" class="form-control" placeholder="End Date (YYYY-MM-DD)"></div>
      <div class="col-md-2"><input name="top_id" class="form-control" placeholder="Topic ID"></div>
      <div class="col-md-1"><button class="btn btn-success w-100">Add</button></div>
    </form>
    {{% endif %}}
    <h2>Events</h2>
    <table class="table table-striped">
      <thead>
        <tr><th>ID</th><th>Name</th><th>Start Date</th><th>Type</th><th>End Date</th><th>Topic ID</th></tr>
      </thead>
      <tbody>
        {{% for e in events %}}
        <tr><td>{{{{ e[0] }}}}</td><td>{{{{ e[1] }}}}</td><td>{{{{ e[2] }}}}</td><td>{{{{ e[3] }}}}</td><td>{{{{ e[4] }}}}</td><td>{{{{ e[5] }}}}</td></tr>
        {{% endfor %}}
      </tbody>
    </table>
    '''
    content = render_template_string(events_template, events=events, show_add=show_add)
    return render_template_string(base_template, content=content)

@app.route('/rentals', methods=['GET', 'POST'])
@login_required
def rentals():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        bdate = request.form['bdate']
        er_date = request.form['er_date']
        ar_date = request.form['ar_date']
        rstatus = request.form['rstatus']
        c_id = request.form['c_id']
        in_id = request.form['in_id']
        cursor.execute('INSERT INTO ps_rental (bdate, er_date, ar_date, rstatus, c_id, in_id) VALUES (?, ?, ?, ?, ?, ?)',
                       (bdate, er_date, ar_date, rstatus, c_id, in_id))
        conn.commit()
        return redirect(url_for('rentals'))
    cursor.execute('SELECT ren_id, bdate, er_date, ar_date, rstatus, c_id, in_id FROM ps_rental')
    rentals = cursor.fetchall()
    conn.close()
    show_add = request.args.get('add') == '1'
    rentals_template = f'''
    {nav_buttons('rentals')}
    {{% if show_add %}}
    <form method="post" class="row g-2 mb-3">
      <div class="col-md-2"><input name="bdate" class="form-control" placeholder="Book Date (YYYY-MM-DD)"></div>
      <div class="col-md-2"><input name="er_date" class="form-control" placeholder="Expected Return (YYYY-MM-DD)"></div>
      <div class="col-md-2"><input name="ar_date" class="form-control" placeholder="Actual Return (YYYY-MM-DD)"></div>
      <div class="col-md-2"><input name="rstatus" class="form-control" placeholder="Status"></div>
      <div class="col-md-2"><input name="c_id" class="form-control" placeholder="Client ID"></div>
      <div class="col-md-1"><input name="in_id" class="form-control" placeholder="Invoice ID"></div>
      <div class="col-md-1"><button class="btn btn-success w-100">Add</button></div>
    </form>
    {{% endif %}}
    <h2>Rentals</h2>
    <table class="table table-striped">
      <thead>
        <tr><th>ID</th><th>Book Date</th><th>Expected Return</th><th>Actual Return</th><th>Status</th><th>Client ID</th><th>Invoice ID</th></tr>
      </thead>
      <tbody>
        {{% for r in rentals %}}
        <tr><td>{{{{ r[0] }}}}</td><td>{{{{ r[1] }}}}</td><td>{{{{ r[2] }}}}</td><td>{{{{ r[3] }}}}</td><td>{{{{ r[4] }}}}</td><td>{{{{ r[5] }}}}</td><td>{{{{ r[6] }}}}</td></tr>
        {{% endfor %}}
      </tbody>
    </table>
    '''
    content = render_template_string(rentals_template, rentals=rentals, show_add=show_add)
    return render_template_string(base_template, content=content)

@app.route('/other', methods=['GET', 'POST'])
@login_required
def other():
    show_add = request.args.get('add') == '1'
    if request.method == 'POST':
        # Placeholder: just flash a message
        flash('Add functionality for "Other" can be implemented here.')
        return redirect(url_for('other'))
    other_template = f'''
    {nav_buttons('other')}
    {{% if show_add %}}
    <form method="post" class="row g-2 mb-3">
      <div class="col-md-10"><input class="form-control" placeholder="Other data (customize as needed)"></div>
      <div class="col-md-2"><button class="btn btn-success w-100">Add</button></div>
    </form>
    {{% endif %}}
    <h2>Other</h2>
    <div class="alert alert-secondary">This is a placeholder for other features or tables you may want to add in the future.</div>
    '''
    content = render_template_string(other_template, show_add=show_add)
    return render_template_string(base_template, content=content)

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    # Get overall counts
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM books')
    book_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM loans')
    loan_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM ps_author')
    author_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM ps_client')
    client_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM ps_event')
    event_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM ps_rental')
    rental_count = cursor.fetchone()[0]
    # For graphs: Books per author (top 5), Loans per month (last 12 months)
    cursor.execute('''
        SELECT author, COUNT(*) as cnt FROM books GROUP BY author ORDER BY cnt DESC LIMIT 5
    ''')
    books_per_author = cursor.fetchall()
    cursor.execute('''
        SELECT strftime('%Y-%m', loan_date) as month, COUNT(*) FROM loans GROUP BY month ORDER BY month DESC LIMIT 12
    ''')
    loans_per_month = cursor.fetchall()
    conn.close()
    dashboard_template = '''
    <h2 class="mb-4"><i class="bi bi-speedometer2"></i> Dashboard</h2>
    <div class="row mb-4 g-4">
      <div class="col-md-3">
        <div class="card shadow-sm border-0 animate__animated animate__fadeInUp">
          <div class="card-body text-center">
            <i class="bi bi-people display-5 text-primary"></i>
            <h4 class="fw-bold">{{ user_count }}</h4>
            <div class="text-muted">Users</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card shadow-sm border-0 animate__animated animate__fadeInUp">
          <div class="card-body text-center">
            <i class="bi bi-book display-5 text-warning"></i>
            <h4 class="fw-bold">{{ book_count }}</h4>
            <div class="text-muted">Books</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card shadow-sm border-0 animate__animated animate__fadeInUp">
          <div class="card-body text-center">
            <i class="bi bi-arrow-left-right display-5 text-success"></i>
            <h4 class="fw-bold">{{ loan_count }}</h4>
            <div class="text-muted">Loans</div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card shadow-sm border-0 animate__animated animate__fadeInUp">
          <div class="card-body text-center">
            <i class="bi bi-person-lines-fill display-5 text-info"></i>
            <h4 class="fw-bold">{{ author_count }}</h4>
            <div class="text-muted">Authors</div>
          </div>
        </div>
      </div>
    </div>
    <div class="row mb-4 g-4">
      <div class="col-md-4">
        <div class="card shadow-sm border-0 animate__animated animate__fadeInUp">
          <div class="card-body text-center">
            <i class="bi bi-people-fill display-6 text-secondary"></i>
            <h5 class="fw-bold">{{ client_count }}</h5>
            <div class="text-muted">Clients</div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm border-0 animate__animated animate__fadeInUp">
          <div class="card-body text-center">
            <i class="bi bi-calendar-event display-6 text-danger"></i>
            <h5 class="fw-bold">{{ event_count }}</h5>
            <div class="text-muted">Events</div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card shadow-sm border-0 animate__animated animate__fadeInUp">
          <div class="card-body text-center">
            <i class="bi bi-file-earmark-text display-6 text-dark"></i>
            <h5 class="fw-bold">{{ rental_count }}</h5>
            <div class="text-muted">Rentals</div>
          </div>
        </div>
      </div>
    </div>
    <div class="row mt-5 g-4">
      <div class="col-md-6">
        <div class="card shadow-sm border-0 animate__animated animate__fadeInUp">
          <div class="card-body">
            <h5 class="card-title">Top 5 Authors by Book Count</h5>
            <canvas id="booksPerAuthorChart"></canvas>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card shadow-sm border-0 animate__animated animate__fadeInUp">
          <div class="card-body">
            <h5 class="card-title">Loans per Month (Last 12 Months)</h5>
            <canvas id="loansPerMonthChart"></canvas>
          </div>
        </div>
      </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
      // Books per Author
      const booksPerAuthorLabels = {{ books_per_author|map(attribute=0)|list|tojson }};
      const booksPerAuthorData = {{ books_per_author|map(attribute=1)|list|tojson }};
      new Chart(document.getElementById('booksPerAuthorChart'), {
        type: 'bar',
        data: {
          labels: booksPerAuthorLabels,
          datasets: [{
            label: 'Books',
            data: booksPerAuthorData,
            backgroundColor: 'rgba(33, 150, 243, 0.7)',
            borderRadius: 8
          }]
        },
        options: {
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true } }
        }
      });
      // Loans per Month
      const loansPerMonthLabels = {{ loans_per_month|map(attribute=0)|list|tojson }}.reverse();
      const loansPerMonthData = {{ loans_per_month|map(attribute=1)|list|tojson }}.reverse();
      new Chart(document.getElementById('loansPerMonthChart'), {
        type: 'line',
        data: {
          labels: loansPerMonthLabels,
          datasets: [{
            label: 'Loans',
            data: loansPerMonthData,
            fill: true,
            backgroundColor: 'rgba(255, 193, 7, 0.2)',
            borderColor: 'rgba(255, 193, 7, 1)',
            tension: 0.3
          }]
        },
        options: {
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true } }
        }
      });
    </script>
    '''
    content = render_template_string(
        dashboard_template,
        user_count=user_count,
        book_count=book_count,
        loan_count=loan_count,
        author_count=author_count,
        client_count=client_count,
        event_count=event_count,
        rental_count=rental_count,
        books_per_author=books_per_author,
        loans_per_month=loans_per_month
    )
    return render_template_string(base_template, content=content)

if __name__ == '__main__':
    create_tables()
    add_sample_data()
    app.run(debug=True) 