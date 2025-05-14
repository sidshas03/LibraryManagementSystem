
-- MySQL-compatible schema generated for library_booking project

CREATE TABLE ps_author (
    a_id INT PRIMARY KEY,
    a_fname VARCHAR(50) NOT NULL,
    a_lname VARCHAR(50) NOT NULL,
    em_add VARCHAR(100),
    add_c VARCHAR(50),
    add_s VARCHAR(50),
    add_ci VARCHAR(50),
    add_str VARCHAR(100)
);

CREATE TABLE ps_book (
    b_id INT PRIMARY KEY,
    bname VARCHAR(100) NOT NULL,
    top_id INT
);

CREATE TABLE ps_topic (
    top_id INT PRIMARY KEY,
    tname VARCHAR(100),
    top_ty VARCHAR(1),
    b_id INT,
    re_id INT,
    eve_id INT
);

CREATE TABLE ps_client (
    c_id INT PRIMARY KEY,
    fname VARCHAR(50),
    lname VARCHAR(50),
    phone_num VARCHAR(15),
    email VARCHAR(100),
    id_ty VARCHAR(10),
    re_id INT
);

CREATE TABLE ps_event (
    eve_id INT PRIMARY KEY,
    name VARCHAR(100),
    s_date DATE,
    eve_type VARCHAR(10),
    e_date DATE,
    top_id INT
);

CREATE TABLE ps_invoice (
    in_id INT PRIMARY KEY,
    in_date DATE,
    amount DECIMAL(10,2),
    ren_id INT
);

CREATE TABLE ps_payment (
    pay_id INT PRIMARY KEY,
    pdate DATE,
    met VARCHAR(10),
    cardn VARCHAR(50),
    p_amount DECIMAL(10,2),
    in_id INT
);

CREATE TABLE ps_rental (
    ren_id INT PRIMARY KEY,
    bdate DATE,
    er_date DATE,
    ar_date DATE,
    rstatus VARCHAR(10),
    c_id INT,
    in_id INT
);

CREATE TABLE ps_reserve (
    re_id INT PRIMARY KEY,
    stime DATETIME,
    etime DATETIME,
    date DATE,
    gsize INT,
    top_id INT
);

CREATE TABLE ps_study_room (
    room_id INT PRIMARY KEY,
    capacity INT,
    re_id INT
);

-- Add Foreign Keys
ALTER TABLE ps_book ADD FOREIGN KEY (top_id) REFERENCES ps_topic(top_id);
ALTER TABLE ps_topic ADD FOREIGN KEY (b_id) REFERENCES ps_book(b_id);
ALTER TABLE ps_event ADD FOREIGN KEY (top_id) REFERENCES ps_topic(top_id);
ALTER TABLE ps_client ADD FOREIGN KEY (re_id) REFERENCES ps_reserve(re_id);
ALTER TABLE ps_invoice ADD FOREIGN KEY (ren_id) REFERENCES ps_rental(ren_id);
ALTER TABLE ps_payment ADD FOREIGN KEY (in_id) REFERENCES ps_invoice(in_id);
ALTER TABLE ps_rental ADD FOREIGN KEY (c_id) REFERENCES ps_client(c_id);
ALTER TABLE ps_rental ADD FOREIGN KEY (in_id) REFERENCES ps_invoice(in_id);
ALTER TABLE ps_study_room ADD FOREIGN KEY (re_id) REFERENCES ps_reserve(re_id);
