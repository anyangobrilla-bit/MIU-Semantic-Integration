
import sqlite3
import csv
from pathlib import Path
from lxml import etree

# Locate the project's data folder
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ==========================================
# 1. ADMISSIONS DATA - SQLITE DATABASE
# ==========================================

database_path = DATA_DIR / "admissions.db"

students = [
    (1001, "Mary", "Wanjiku", "2024-01-15", "Computing"),
    (1002, "John", "Kamau", "2024-01-16", "Business"),
    (1003, "Grace", "Achieng", "2024-01-18", "Computing"),
    (1004, "Peter", "Mwangi", "2024-01-20", "Communication"),
    (1005, "Faith", "Njeri", "2024-01-22", "Business"),
]

with sqlite3.connect(database_path) as connection:

    connection.execute("DROP TABLE IF EXISTS students")

    connection.execute("""
        CREATE TABLE students (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            admission_date TEXT,
            department TEXT
        )
    """)

    connection.executemany("""
        INSERT INTO students
        (student_id, first_name, last_name, admission_date, department)
        VALUES (?, ?, ?, ?, ?)
    """, students)

print("1. Admissions database created successfully.")


# ==========================================
# 2. ACADEMICS DATA - XML FILE
# ==========================================

academic_records = [
    ("1001", "CS101", "Introduction to Programming"),
    ("1002", "BUS201", "Principles of Management"),
    ("1003", "CS102", "Database Systems"),
    ("1004", "COM101", "Introduction to Communication"),
    ("1005", "BUS202", "Business Research Methods"),
]

root = etree.Element("UniversityAcademicRecords")

university = etree.SubElement(root, "University")
university.text = "Meridian International University"

for student_id, course_code, course_name in academic_records:

    enrolment = etree.SubElement(root, "Enrolment")

    etree.SubElement(
        enrolment, "StudentNumber"
    ).text = student_id

    etree.SubElement(
        enrolment, "CourseCode"
    ).text = course_code

    etree.SubElement(
        enrolment, "CourseName"
    ).text = course_name

xml_path = DATA_DIR / "academics.xml"

tree = etree.ElementTree(root)

tree.write(
    str(xml_path),
    encoding="UTF-8",
    xml_declaration=True,
    pretty_print=True
)

print("2. Academics XML file created successfully.")


# ==========================================
# 3. FINANCE DATA - CSV FILE
# ==========================================

finance_records = [
    ["StudentRef", "TuitionFee", "AmountPaid", "OutstandingBalance"],
    ["1001", 50000, 50000, 0],
    ["1002", 60000, 40000, 20000],
    ["1003", 50000, 30000, 20000],
    ["1004", 55000, 55000, 0],
    ["1005", 60000, 45000, 15000],
]

csv_path = DATA_DIR / "finance.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerows(finance_records)

print("3. Finance CSV file created successfully.")

print("\nAll three MIU datasets have been generated!")
print("Files saved in:", DATA_DIR)
