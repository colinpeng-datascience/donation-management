-- run this in shell to create database
-- sqlite3 var/donation_management.sqlite3 < sql/schema.sql

PRAGMA foreign_keys = ON;

-- Create the 'type' table
CREATE TABLE type (
    type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT
);

-- Create the 'subtype' table
CREATE TABLE subtype (
    subtype_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER,
    subtype_name TEXT,
    FOREIGN KEY (type_id) REFERENCES type(type_id)
    UNIQUE (type_id, subtype_name)
);

-- Create the 'donor' table
CREATE TABLE donor (
    donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_email TEXT UNIQUE,
    donor_name TEXT
);

-- Create the 'staff' table
CREATE TABLE staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_email TEXT,
    staff_password_hashed TEXT,
    staff_name TEXT,
    staff_created_by_staff_id INTEGER,
    FOREIGN KEY (staff_created_by_staff_id) REFERENCES staff(staff_id)
);

-- Create the 'donation' table
CREATE TABLE donation (
    donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    donor_id INTEGER,
    staff_id INTEGER,
    donation_date TEXT,
    donation_quantity INTEGER,
    subtype_id INTEGER,
    FOREIGN KEY (donor_id) REFERENCES donor(donor_id),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    FOREIGN KEY (subtype_id) REFERENCES subtype(subtype_id)
);

-- Create the 'distribution' table
CREATE TABLE distribution (
    distribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER,
    subtype_id INTEGER,
    distribution_date TEXT,
    distribution_amount INTEGER,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    FOREIGN KEY (subtype_id) REFERENCES subtype(subtype_id)
);
