import sqlite3

DB_NAME = 'library.db'
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS ps_author (
  a_id INTEGER PRIMARY KEY,
  a_fname TEXT NOT NULL,
  a_lname TEXT NOT NULL,
  em_add TEXT,
  add_c TEXT,
  add_s TEXT,
  add_ci TEXT,
  add_str TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_book (
  b_id INTEGER PRIMARY KEY,
  bname TEXT NOT NULL,
  top_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_client (
  c_id INTEGER PRIMARY KEY,
  fname TEXT,
  lname TEXT,
  phone_num TEXT,
  email TEXT,
  id_ty TEXT,
  re_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_event (
  eve_id INTEGER PRIMARY KEY,
  name TEXT,
  s_date DATE,
  eve_type TEXT,
  e_date DATE,
  top_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_invoice (
  in_id INTEGER PRIMARY KEY,
  in_date DATE,
  amount REAL,
  ren_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_payment (
  pay_id INTEGER PRIMARY KEY,
  pdate DATE,
  met TEXT,
  cardn TEXT,
  p_amount REAL,
  in_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_rental (
  ren_id INTEGER PRIMARY KEY,
  bdate DATE,
  er_date DATE,
  ar_date DATE,
  rstatus TEXT,
  c_id INTEGER,
  in_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_reserve (
  re_id INTEGER PRIMARY KEY,
  stime TEXT,
  etime TEXT,
  date DATE,
  gsize INTEGER,
  top_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_study_room (
  room_id INTEGER PRIMARY KEY,
  capacity INTEGER,
  re_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_topic (
  top_id INTEGER PRIMARY KEY,
  tname TEXT,
  top_ty TEXT,
  b_id INTEGER,
  re_id INTEGER,
  eve_id INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ps_users (
  user_id INTEGER PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  role TEXT NOT NULL
)''')

# Insert data for ps_author
cursor.executemany('''INSERT OR IGNORE INTO ps_author VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', [
(1, 'Aishwarya', 'Mehta', 'aish1@mail.com', 'India', 'MH', 'Mumbai', 'Andheri'),
(2, 'Raghav', 'Menon', 'raghav2@mail.com', 'India', 'KL', 'Cochin', 'MG Road'),
(3, 'Priya', 'Natarajan', 'priya3@mail.com', 'India', 'TN', 'Chennai', 'Adyar'),
(4, 'Neeraj', 'Kumar', 'neeraj4@mail.com', 'India', 'DL', 'Delhi', 'Saket'),
(5, 'Lakshmi', 'Das', 'lakshmi5@mail.com', 'India', 'WB', 'Kolkata', 'Salt Lake'),
(6, 'Anuj', 'Bhatt', 'anuj6@mail.com', 'India', 'RJ', 'Jaipur', 'Malviya Nagar'),
(7, 'Kavya', 'Rao', 'kavya7@mail.com', 'India', 'KA', 'Bangalore', 'Koramangala'),
(8, 'Rohit', 'Shah', 'rohit8@mail.com', 'India', 'GJ', 'Ahmedabad', 'CG Road'),
(9, 'Sneha', 'Iyer', 'sneha9@mail.com', 'India', 'TN', 'Chennai', 'T Nagar'),
(10, 'Vikram', 'Patel', 'vikram10@mail.com', 'India', 'MH', 'Pune', 'Baner'),
(11, 'Meera', 'Jain', 'meera11@mail.com', 'India', 'KA', 'Mysore', 'Vijayanagar'),
(12, 'Nisha', 'Kohli', 'nisha12@mail.com', 'India', 'PB', 'Ludhiana', 'Civil Lines'),
(13, 'Ramesh', 'Tiwari', 'ramesh13@mail.com', 'India', 'UP', 'Lucknow', 'Hazratganj'),
(14, 'Divya', 'Singh', 'divya14@mail.com', 'India', 'MP', 'Indore', 'Palasia'),
(15, 'Harsha', 'Ghosh', 'harsha15@mail.com', 'India', 'WB', 'Kolkata', 'New Alipore'),
(16, 'Amit', 'Chopra', 'amit16@mail.com', 'India', 'DL', 'Delhi', 'Dwarka'),
(17, 'Bhavna', 'Roy', 'bhavna17@mail.com', 'India', 'BR', 'Patna', 'Kankarbagh'),
(18, 'Sunil', 'Das', 'sunil18@mail.com', 'India', 'OD', 'Bhubaneswar', 'Jaydev Vihar'),
(19, 'Geeta', 'Kumar', 'geeta19@mail.com', 'India', 'UP', 'Noida', 'Sector 18'),
(20, 'Anjali', 'Malik', 'anjali20@mail.com', 'India', 'HR', 'Gurgaon', 'DLF Phase 3'),
(21, 'Naveen', 'Reddy', 'naveen21@mail.com', 'India', 'AP', 'Vijayawada', 'Labbipet'),
(22, 'Chitra', 'Bose', 'chitra22@mail.com', 'India', 'WB', 'Howrah', 'Shibpur'),
(23, 'Tushar', 'Joshi', 'tushar23@mail.com', 'India', 'MH', 'Nagpur', 'Dharampeth'),
(24, 'Lavanya', 'Shekhar', 'lavanya24@mail.com', 'India', 'KA', 'Hubli', 'Vidyanagar'),
(25, 'Sandeep', 'Verma', 'sandeep25@mail.com', 'India', 'RJ', 'Jodhpur', 'Paota'),
(26, 'Radha', 'Pillai', 'radha26@mail.com', 'India', 'KL', 'Trivandrum', 'Vellayambalam'),
(27, 'Deepak', 'Kumar', 'deepak27@mail.com', 'India', 'DL', 'Delhi', 'CP'),
(28, 'Rekha', 'Desai', 'rekha28@mail.com', 'India', 'GJ', 'Surat', 'Athwa'),
(29, 'Vinod', 'Rathore', 'vinod29@mail.com', 'India', 'MP', 'Bhopal', 'TT Nagar'),
(30, 'Shalini', 'Dwivedi', 'shalini30@mail.com', 'India', 'UP', 'Kanpur', 'Swaroop Nagar'),
])

# Insert data for ps_book
cursor.executemany('''INSERT OR IGNORE INTO ps_book VALUES (?, ?, ?)''', [
(1, 'Book A', 1), (2, 'Book 2', None), (3, 'Book 3', None), (4, 'Book 4', None), (5, 'Book 5', None), (6, 'Book 6', None), (7, 'Book 7', None), (8, 'Book 8', None), (9, 'Book 9', None), (10, 'Book 10', None), (11, 'Book 11', None), (12, 'Book 12', None), (13, 'Book 13', None), (14, 'Book 14', None), (15, 'Book 15', None), (16, 'Book 16', None), (17, 'Book 17', None), (18, 'Book 18', None), (19, 'Book 19', None), (20, 'Book 20', None), (21, 'Book 21', None), (22, 'Book 22', None), (23, 'Book 23', None), (24, 'Book 24', None), (25, 'Book 25', None), (26, 'Book 26', None), (27, 'Book 27', None), (28, 'Book 28', None), (29, 'Book 29', None), (30, 'Book 30', None), (31, "Man's Search for Meaning Book by Viktor Frankl", 2),
])

# Insert data for ps_client
ps_client_data = [
(1, 'Sneha', 'Patel e', '9876500001', 'sneha1@example.com', 'PAN', 1),
(2, 'Arjun', 'Verma', '9876500002', 'arjun2@example.com', 'AAD', 2),
(3, 'Divya', 'Iyer', '9876500003', 'divya3@example.com', 'DL', 3),
(4, 'Karthik', 'Nair', '9876500004', 'karthik4@example.com', 'VOT', 4),
(5, 'Riya', 'Sharma', '9876500005', 'riya5@example.com', 'PAN', 5),
(6, 'Ajay', 'Pillai', '9876500006', 'ajay6@example.com', 'AAD', 6),
(7, 'Megha', 'Bansal', '9876500007', 'megha7@example.com', 'PAN', 7),
(8, 'Tarun', 'Joshi', '9876500008', 'tarun8@example.com', 'DL', 8),
(9, 'Latha', 'Krishnan', '9876500009', 'latha9@example.com', 'VOT', 9),
(10, 'Nikhil', 'Desai', '9876500010', 'nikhil10@example.com', 'PAN', 10),
(11, 'Sara', 'Kapoor', '9876500011', 'sara11@example.com', 'AAD', 11),
(12, 'Manoj', 'Shetty', '9876500012', 'manoj12@example.com', 'PAN', 12),
(13, 'Ishita', 'Rao', '9876500013', 'ishita13@example.com', 'DL', 13),
(14, 'Kunal', 'Jain', '9876500014', 'kunal14@example.com', 'VOT', 14),
(15, 'Radhika', 'Sen', 'radhika15@example.com', 'PAN', 15),
(16, 'Yash', 'Bhatt', 'yash16@example.com', 'AAD', 16),
(17, 'Aditi', 'Mehra', '9876500017', 'aditi17@example.com', 'PAN', 17),
(18, 'Ravi', 'Mishra', '9876500018', 'ravi18@example.com', 'DL', 18),
(19, 'Tanvi', 'Gupta', '9876500019', 'tanvi19@example.com', 'VOT', 19),
(20, 'Nitin', 'Chawla', 'nitin20@example.com', 'PAN', 20),
(21, 'Priya', 'Dixit', 'priya21@example.com', 'AAD', 21),
(22, 'Aman', 'Goel', 'aman22@example.com', 'PAN', 22),
(23, 'Neha', 'Malhotra', 'neha23@example.com', 'DL', 23),
(24, 'Abhishek', 'Singh', 'abhishek24@example.com', 'VOT', 24),
(25, 'Shruti', 'Agarwal', 'shruti25@example.com', 'PAN', 25),
(26, 'Vivek', 'Kapadia', 'vivek26@example.com', 'AAD', 26),
(27, 'Tanya', 'Mohan', 'tanya27@example.com', 'PAN', 27),
(28, 'Rohan', 'Naik', 'rohan28@example.com', 'DL', 28),
(29, 'Jaya', 'Kulkarni', 'jaya29@example.com', 'VOT', 29),
(30, 'Rakesh', 'Bose', 'rakesh30@example.com', 'PAN', 30),
(31, 'Siddharthan', 'P S', '9790267089', 'sp8004@nyu.edu', 'PAN', 22),
(32, 'Cust', 'One', '9876543000', 'cust1', 'AAD', 19),
]
# Ensure all tuples have 7 values
ps_client_data = [row if len(row) == 7 else row + (None,) for row in ps_client_data]
cursor.executemany('''INSERT OR IGNORE INTO ps_client VALUES (?, ?, ?, ?, ?, ?, ?)''', ps_client_data)

# Insert data for ps_event
cursor.executemany('''INSERT OR IGNORE INTO ps_event VALUES (?, ?, ?, ?, ?, ?)''', [
(1, 'Event 1', '2025-05-01', 'Seminar', '2025-05-01', 1),
(2, 'Event 2', '2025-05-02', 'Workshop', '2025-05-02', 2),
(3, 'Event 3', '2025-05-03', 'Seminar', '2025-05-03', 3),
(4, 'Event 4', '2025-05-04', 'Seminar', '2025-05-04', 4),
(5, 'Event 5', '2025-05-05', 'Workshop', '2025-05-05', 5),
(6, 'Event 6', '2025-05-06', 'Seminar', '2025-05-06', 6),
(7, 'Event 7', '2025-05-07', 'Seminar', '2025-05-07', 7),
(8, 'Event 8', '2025-05-08', 'Seminar', '2025-05-08', 8),
(9, 'Event 9', '2025-05-09', 'Workshop', '2025-05-09', 9),
(10, 'Event 10', '2025-05-10', 'Seminar', '2025-05-10', 10),
(11, 'Event 11', '2025-05-11', 'Workshop', '2025-05-11', 11),
(12, 'Event 12', '2025-05-12', 'Seminar', '2025-05-12', 12),
(13, 'Event 13', '2025-05-13', 'Seminar', '2025-05-13', 13),
(14, 'Event 14', '2025-05-14', 'Seminar', '2025-05-14', 14),
(15, 'Event 15', '2025-05-15', 'Seminar', '2025-05-15', 15),
(16, 'Event 16', '2025-05-16', 'Workshop', '2025-05-16', 16),
(17, 'Event 17', '2025-05-17', 'Seminar', '2025-05-17', 17),
(18, 'Event 18', '2025-05-18', 'Seminar', '2025-05-18', 18),
(19, 'Event 19', '2025-05-19', 'Seminar', '2025-05-19', 19),
(20, 'Event 20', '2025-05-20', 'Workshop', '2025-05-20', 20),
(21, 'Event 21', '2025-05-21', 'Seminar', '2025-05-21', 21),
(22, 'Event 22', '2025-05-22', 'Seminar', '2025-05-22', 22),
(23, 'Event 23', '2025-05-23', 'Workshop', '2025-05-23', 23),
(24, 'Event 24', '2025-05-24', 'Seminar', '2025-05-24', 24),
(25, 'Event 25', '2025-05-25', 'Seminar', '2025-05-25', 25),
(26, 'Event 26', '2025-05-26', 'Seminar', '2025-05-26', 26),
(27, 'Event 27', '2025-05-27', 'Seminar', '2025-05-27', 27),
(28, 'Event 28', '2025-05-28', 'Workshop', '2025-05-28', 28),
(29, 'Event 29', '2025-05-29', 'Seminar', '2025-05-29', 29),
(30, 'Event 30', '2025-05-30', 'Seminar', '2025-05-30', 30),
(31, 'NYU EVENT', '2025-10-03', 'Seminar', '2025-10-04', 3),
])

# Insert data for ps_invoice
cursor.executemany('''INSERT OR IGNORE INTO ps_invoice VALUES (?, ?, ?, ?)''', [
(1, '2025-05-01', 120.00, 1), (2, '2025-05-02', 110.00, 2), (3, '2025-05-03', 115.00, 3), (4, '2025-05-04', 120.00, 4), (5, '2025-05-05', 125.00, 5), (6, '2025-05-06', 130.00, 6), (7, '2025-05-07', 135.00, 7), (8, '2025-05-08', 140.00, 8), (9, '2025-05-09', 145.00, 9), (10, '2025-05-10', 150.00, 10), (11, '2025-05-11', 155.00, 11), (12, '2025-05-12', 160.00, 12), (13, '2025-05-13', 165.00, 13), (14, '2025-05-14', 170.00, 14), (15, '2025-05-15', 175.00, 15), (16, '2025-05-16', 180.00, 16), (17, '2025-05-17', 185.00, 17), (18, '2025-05-18', 190.00, 18), (19, '2025-05-19', 195.00, 19), (20, '2025-05-20', 200.00, 20), (21, '2025-05-21', 205.00, 21), (22, '2025-05-22', 210.00, 22), (23, '2025-05-23', 215.00, 23), (24, '2025-05-24', 220.00, 24), (25, '2025-05-25', 225.00, 25), (26, '2025-05-26', 230.00, 26), (27, '2025-05-27', 235.00, 27), (28, '2025-05-28', 240.00, 28), (29, '2025-05-29', 245.00, 29), (30, '2025-05-30', 250.00, 30),
])

# Insert data for ps_payment
cursor.executemany('''INSERT OR IGNORE INTO ps_payment VALUES (?, ?, ?, ?, ?, ?)''', [
(1, '2025-05-01', 'Card', '1111-2222-3333-4444', 120.00, 1), (2, '2025-05-02', 'Card', '1111-2222-3333-1002', 110.00, 2), (3, '2025-05-03', 'Card', '1111-2222-3333-1003', 115.00, 3), (4, '2025-05-04', 'Card', '1111-2222-3333-1004', 120.00, 4), (5, '2025-05-05', 'Card', '1111-2222-3333-1005', 125.00, 5), (6, '2025-05-06', 'Card', '1111-2222-3333-1006', 130.00, 6), (7, '2025-05-07', 'Card', '1111-2222-3333-1007', 135.00, 7), (8, '2025-05-08', 'Card', '1111-2222-3333-1008', 140.00, 8), (9, '2025-05-09', 'Card', '1111-2222-3333-1009', 145.00, 9), (10, '2025-05-10', 'Card', '1111-2222-3333-1010', 150.00, 10), (11, '2025-05-11', 'Card', '1111-2222-3333-1011', 155.00, 11), (12, '2025-05-12', 'Card', '1111-2222-3333-1012', 160.00, 12), (13, '2025-05-13', 'Card', '1111-2222-3333-1013', 165.00, 13), (14, '2025-05-14', 'Card', '1111-2222-3333-1014', 170.00, 14), (15, '2025-05-15', 'Card', '1111-2222-3333-1015', 175.00, 15), (16, '2025-05-16', 'Card', '1111-2222-3333-1016', 180.00, 16), (17, '2025-05-17', 'Card', '1111-2222-3333-1017', 185.00, 17), (18, '2025-05-18', 'Card', '1111-2222-3333-1018', 190.00, 18), (19, '2025-05-19', 'Card', '1111-2222-3333-1019', 195.00, 19), (20, '2025-05-20', 'Card', '1111-2222-3333-1020', 200.00, 20), (21, '2025-05-21', 'Card', '1111-2222-3333-1021', 205.00, 21), (22, '2025-05-22', 'Card', '1111-2222-3333-1022', 210.00, 22), (23, '2025-05-23', 'Card', '1111-2222-3333-1023', 215.00, 23), (24, '2025-05-24', 'Card', '1111-2222-3333-1024', 220.00, 24), (25, '2025-05-25', 'Card', '1111-2222-3333-1025', 225.00, 25), (26, '2025-05-26', 'Card', '1111-2222-3333-1026', 230.00, 26), (27, '2025-05-27', 'Card', '1111-2222-3333-1027', 235.00, 27), (28, '2025-05-28', 'Card', '1111-2222-3333-1028', 240.00, 28), (29, '2025-05-29', 'Card', '1111-2222-3333-1029', 245.00, 29), (30, '2025-05-30', 'Card', '1111-2222-3333-1030', 250.00, 30),
])

# Insert data for ps_rental
cursor.executemany('''INSERT OR IGNORE INTO ps_rental VALUES (?, ?, ?, ?, ?, ?, ?)''', [
(1, '2025-05-01', '2025-05-07', '2025-05-06', 'Returned', 1, 1), (2, '2025-05-02', '2025-05-08', '2025-05-07', 'Returned', 2, 2), (3, '2025-05-03', '2025-05-09', '2025-05-08', 'Returned', 3, 3), (4, '2025-05-04', '2025-05-10', '2025-05-09', 'Returned', 4, 4), (5, '2025-05-05', '2025-05-11', '2025-05-10', 'Returned', 5, 5), (6, '2025-05-06', '2025-05-12', '2025-05-11', 'Returned', 6, 6), (7, '2025-05-07', '2025-05-13', '2025-05-12', 'Returned', 7, 7), (8, '2025-05-08', '2025-05-14', '2025-05-13', 'Returned', 8, 8), (9, '2025-05-09', '2025-05-15', '2025-05-14', 'Returned', 9, 9), (10, '2025-05-10', '2025-05-16', '2025-05-15', 'Returned', 10, 10), (11, '2025-05-11', '2025-05-17', '2025-05-16', 'Returned', 11, 11), (12, '2025-05-12', '2025-05-18', '2025-05-17', 'Returned', 12, 12), (13, '2025-05-13', '2025-05-19', '2025-05-18', 'Returned', 13, 13), (14, '2025-05-14', '2025-05-20', '2025-05-19', 'Returned', 14, 14), (15, '2025-05-15', '2025-05-21', '2025-05-20', 'Returned', 15, 15), (16, '2025-05-16', '2025-05-22', '2025-05-21', 'Returned', 16, 16), (17, '2025-05-17', '2025-05-23', '2025-05-22', 'Returned', 17, 17), (18, '2025-05-18', '2025-05-24', '2025-05-23', 'Returned', 18, 18), (19, '2025-05-19', '2025-05-25', '2025-05-24', 'Returned', 19, 19), (20, '2025-05-20', '2025-05-26', '2025-05-25', 'Returned', 20, 20), (21, '2025-05-21', '2025-05-27', '2025-05-26', 'Returned', 21, 21), (22, '2025-05-22', '2025-05-28', '2025-05-27', 'Returned', 22, 22), (23, '2025-05-23', '2025-05-29', '2025-05-28', 'Returned', 23, 23), (24, '2025-05-24', '2025-05-30', '2025-05-29', 'Returned', 24, 24), (25, '2025-05-25', '2025-06-01', '2025-05-31', 'Returned', 25, 25), (26, '2025-05-26', '2025-06-02', '2025-06-01', 'Returned', 26, 26), (27, '2025-05-27', '2025-06-03', '2025-06-02', 'Returned', 27, 27), (28, '2025-05-28', '2025-06-04', '2025-06-03', 'Returned', 28, 28), (29, '2025-05-29', '2025-06-05', '2025-06-04', 'Returned', 29, 29), (30, '2025-05-30', '2025-06-06', '2025-06-05', 'Returned', 30, 30),
])

# Insert data for ps_reserve
cursor.executemany('''INSERT OR IGNORE INTO ps_reserve VALUES (?, ?, ?, ?, ?, ?)''', [
(1, '2025-05-01 09:00:00', '2025-05-01 10:00:00', '2025-05-01', 2, 1), (2, '2025-05-02 10:00:00', '2025-05-02 11:00:00', '2025-05-02', 4, 2), (3, '2025-05-03 11:00:00', '2025-05-03 12:00:00', '2025-05-03', 3, 3), (4, '2025-05-04 12:00:00', '2025-05-04 13:00:00', '2025-05-04', 5, 4), (5, '2025-05-05 09:30:00', '2025-05-05 10:30:00', '2025-05-05', 6, 5), (6, '2025-05-06 14:00:00', '2025-05-06 15:00:00', '2025-05-06', 2, 6), (7, '2025-05-07 15:00:00', '2025-05-07 16:00:00', '2025-05-07', 3, 7), (8, '2025-05-08 16:00:00', '2025-05-08 17:00:00', '2025-05-08', 1, 8), (9, '2025-05-09 17:00:00', '2025-05-09 18:00:00', '2025-05-09', 8, 9), (10, '2025-05-10 18:00:00', '2025-05-10 19:00:00', '2025-05-10', 10, 10), (11, '2025-05-11 09:00:00', '2025-05-11 10:00:00', '2025-05-11', 2, 11), (12, '2025-05-12 10:00:00', '2025-05-12 11:00:00', '2025-05-12', 4, 12), (13, '2025-05-13 11:00:00', '2025-05-13 12:00:00', '2025-05-13', 3, 13), (14, '2025-05-14 12:00:00', '2025-05-14 13:00:00', '2025-05-14', 5, 14), (15, '2025-05-15 09:30:00', '2025-05-15 10:30:00', '2025-05-15', 6, 15), (16, '2025-05-16 14:00:00', '2025-05-16 15:00:00', '2025-05-16', 2, 16), (17, '2025-05-17 15:00:00', '2025-05-17 16:00:00', '2025-05-17', 3, 17), (18, '2025-05-18 16:00:00', '2025-05-18 17:00:00', '2025-05-18', 1, 18), (19, '2025-05-19 17:00:00', '2025-05-19 18:00:00', '2025-05-19', 8, 19), (20, '2025-05-20 18:00:00', '2025-05-20 19:00:00', '2025-05-20', 10, 20), (21, '2025-05-21 09:00:00', '2025-05-21 10:00:00', '2025-05-21', 2, 21), (22, '2025-05-22 10:00:00', '2025-05-22 11:00:00', '2025-05-22', 4, 22), (23, '2025-05-23 11:00:00', '2025-05-23 12:00:00', '2025-05-23', 3, 23), (24, '2025-05-24 12:00:00', '2025-05-24 13:00:00', '2025-05-24', 5, 24), (25, '2025-05-25 09:30:00', '2025-05-25 10:30:00', '2025-05-25', 6, 25), (26, '2025-05-26 14:00:00', '2025-05-26 15:00:00', '2025-05-26', 2, 26), (27, '2025-05-27 15:00:00', '2025-05-27 16:00:00', '2025-05-27', 3, 27), (28, '2025-05-28 16:00:00', '2025-05-28 17:00:00', '2025-05-28', 1, 28), (29, '2025-05-29 17:00:00', '2025-05-29 18:00:00', '2025-05-29', 8, 29), (30, '2025-05-30 18:00:00', '2025-05-30 19:00:00', '2025-05-30', 10, 30),
])

# Insert data for ps_study_room
cursor.executemany('''INSERT OR IGNORE INTO ps_study_room VALUES (?, ?, ?)''', [
(101, 4, 1), (102, 6, 2), (103, 8, 3), (104, 6, 4), (105, 2, 5), (106, 10, 6), (107, 4, 7), (108, 6, 8), (109, 8, 9), (110, 6, 10), (111, 2, 11), (112, 10, 12), (113, 4, 13), (114, 6, 14), (115, 8, 15), (116, 6, 16), (117, 2, 17), (118, 10, 18), (119, 4, 19), (120, 6, 20), (121, 8, 21), (122, 6, 22), (123, 2, 23), (124, 10, 24), (125, 4, 25), (126, 6, 26), (127, 8, 27), (128, 6, 28), (129, 2, 29), (130, 10, 30),
])

# Insert data for ps_topic
cursor.executemany('''INSERT OR IGNORE INTO ps_topic VALUES (?, ?, ?, ?, ?, ?)''', [
(1, 'Topic 1', 'A', 1, 1, 1), (2, 'Topic 2', 'B', 2, 2, 2), (3, 'Topic 3', 'A', 3, 3, 3), (4, 'Topic 4', 'B', 4, 4, 4), (5, 'Topic 5', 'A', 5, 5, 5), (6, 'Topic 6', 'B', 6, 6, 6), (7, 'Topic 7', 'A', 7, 7, 7), (8, 'Topic 8', 'B', 8, 8, 8), (9, 'Topic 9', 'A', 9, 9, 9), (10, 'Topic 10', 'B', 10, 10, 10), (11, 'Topic 11', 'A', 11, 11, 11), (12, 'Topic 12', 'B', 12, 12, 12), (13, 'Topic 13', 'A', 13, 13, 13), (14, 'Topic 14', 'B', 14, 14, 14), (15, 'Topic 15', 'A', 15, 15, 15), (16, 'Topic 16', 'B', 16, 16, 16), (17, 'Topic 17', 'A', 17, 17, 17), (18, 'Topic 18', 'B', 18, 18, 18), (19, 'Topic 19', 'A', 19, 19, 19), (20, 'Topic 20', 'B', 20, 20, 20), (21, 'Topic 21', 'A', 21, 21, 21), (22, 'Topic 22', 'B', 22, 22, 22), (23, 'Topic 23', 'A', 23, 23, 23), (24, 'Topic 24', 'B', 24, 24, 24), (25, 'Topic 25', 'A', 25, 25, 25), (26, 'Topic 26', 'B', 26, 26, 26), (27, 'Topic 27', 'A', 27, 27, 27), (28, 'Topic 28', 'B', 28, 28, 28), (29, 'Topic 29', 'A', 29, 29, 29), (30, 'Topic 30', 'B', 30, 30, 30),
])

# Insert data for ps_users
cursor.executemany('''INSERT OR IGNORE INTO ps_users VALUES (?, ?, ?, ?)''', [
(1, 'admin1', 'admin123', 'admin'), (2, 'cust1', 'cust123', 'customer'),
])

conn.commit()
conn.close()
print('All tables created and populated!') 