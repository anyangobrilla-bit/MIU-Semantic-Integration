
import sqlite3
import csv
import xml.etree.ElementTree as ET

from pathlib import Path
from decimal import Decimal
from rdflib import Graph, Namespace, Literal, RDF, XSD


# --------------------------------------------------
# 1. DEFINE PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = BASE_DIR / "data" / "admissions.db"
XML_FILE = BASE_DIR / "data" / "academics.xml"
CSV_FILE = BASE_DIR / "data" / "finance.csv"

ONTOLOGY_FILE = BASE_DIR / "ontology" / "MIU_University_Ontology.owl"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "miu_integrated_data.ttl"


# --------------------------------------------------
# 2. DEFINE MIU ONTOLOGY NAMESPACE
# --------------------------------------------------

MIU = Namespace(
    "http://www.miu.ac.ke/ontology/university#"
)

g = Graph()

g.bind("miu", MIU)
g.bind("rdf", RDF)
g.bind("xsd", XSD)


# --------------------------------------------------
# 3. LOAD THE PROTÉGÉ OWL ONTOLOGY
# --------------------------------------------------

print("Loading MIU OWL ontology...")

if not ONTOLOGY_FILE.exists():
    raise FileNotFoundError(
        f"Ontology file not found: {ONTOLOGY_FILE}"
    )

g.parse(
    str(ONTOLOGY_FILE),
    format="xml"
)

print("OWL ontology loaded successfully.")


# --------------------------------------------------
# 4. CREATE UNIVERSITY INDIVIDUAL
# --------------------------------------------------

university = MIU["university"]

g.add((university, RDF.type, MIU.University))

g.add((
    university,
    MIU.universityName,
    Literal(
        "Meridian International University",
        datatype=XSD.string
    )
))


# --------------------------------------------------
# 5. READ ADMISSIONS DATA FROM SQLITE
# --------------------------------------------------

print("Reading admissions database...")

connection = sqlite3.connect(DATABASE_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("SELECT * FROM students")

students = cursor.fetchall()

connection.close()

for student in students:

    student_id = str(student["student_id"])

    student_uri = MIU[f"student/{student_id}"]

    department_name = student["department"]

    department_uri = MIU[
        f"department/{department_name.replace(' ', '_')}"
    ]

    # Create student
    g.add((student_uri, RDF.type, MIU.Student))

    g.add((
        student_uri,
        MIU.studentID,
        Literal(int(student_id), datatype=XSD.integer)
    ))

    g.add((
        student_uri,
        MIU.firstName,
        Literal(student["first_name"], datatype=XSD.string)
    ))

    g.add((
        student_uri,
        MIU.lastName,
        Literal(student["last_name"], datatype=XSD.string)
    ))

    # Convert date-only value to an XML Schema dateTime value
    admission_date = student["admission_date"] + "T00:00:00"

    g.add((
        student_uri,
        MIU.admissionDate,
        Literal(admission_date, datatype=XSD.dateTime)
    ))

    # Create department
    g.add((department_uri, RDF.type, MIU.Department))

    g.add((
        department_uri,
        MIU.departmentName,
        Literal(department_name, datatype=XSD.string)
    ))

    # Link student to department
    g.add((
        student_uri,
        MIU.belongsToDepartment,
        department_uri
    ))

    # Link university to department
    g.add((
        university,
        MIU.hasDepartment,
        department_uri
    ))


# --------------------------------------------------
# 6. READ ACADEMIC DATA FROM XML
# --------------------------------------------------

print("Reading academic XML records...")

tree = ET.parse(XML_FILE)
root = tree.getroot()

for record in root.findall("Enrolment"):

    student_id = record.findtext("StudentNumber")
    course_code = record.findtext("CourseCode")
    course_name = record.findtext("CourseName")

    student_uri = MIU[f"student/{student_id}"]

    course_uri = MIU[f"course/{course_code}"]

    enrolment_uri = MIU[
        f"enrolment/{student_id}_{course_code}"
    ]

    # Create course
    g.add((course_uri, RDF.type, MIU.Course))

    g.add((
        course_uri,
        MIU.courseCode,
        Literal(course_code, datatype=XSD.string)
    ))

    g.add((
        course_uri,
        MIU.courseName,
        Literal(course_name, datatype=XSD.string)
    ))

    # Create enrolment
    g.add((enrolment_uri, RDF.type, MIU.Enrolment))

    # Link student to enrolment
    g.add((
        student_uri,
        MIU.hasEnrolment,
        enrolment_uri
    ))

    # Link enrolment to course
    g.add((
        enrolment_uri,
        MIU.isForCourse,
        course_uri
    ))


# --------------------------------------------------
# 7. READ FINANCE DATA FROM CSV
# --------------------------------------------------

print("Reading finance CSV records...")

with open(
    CSV_FILE,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for record in reader:

        student_id = record["StudentRef"]

        student_uri = MIU[f"student/{student_id}"]

        fee_uri = MIU[f"feeRecord/{student_id}"]

        # Create fee record
        g.add((fee_uri, RDF.type, MIU.FeeRecord))

        # Add tuition fee
        g.add((
            fee_uri,
            MIU.tuitionFee,
            Literal(
                Decimal(record["TuitionFee"]),
                datatype=XSD.decimal
            )
        ))

        # Add amount paid
        g.add((
            fee_uri,
            MIU.amountPaid,
            Literal(
                Decimal(record["AmountPaid"]),
                datatype=XSD.decimal
            )
        ))

        # Add outstanding balance
        g.add((
            fee_uri,
            MIU.outstandingBalance,
            Literal(
                Decimal(record["OutstandingBalance"]),
                datatype=XSD.decimal
            )
        ))

        # Link student to fee record
        g.add((
            student_uri,
            MIU.hasFeeRecord,
            fee_uri
        ))


# --------------------------------------------------
# 8. SAVE THE COMBINED RDF GRAPH
# --------------------------------------------------

g.serialize(
    destination=str(OUTPUT_FILE),
    format="turtle"
)

print("\nSEMANTIC INTEGRATION COMPLETED SUCCESSFULLY!")

print("University: Meridian International University")
print(f"Students processed: {len(students)}")
print(f"Total RDF triples generated: {len(g)}")
print(f"Integrated RDF file saved at: {OUTPUT_FILE}")
