
from pathlib import Path
from rdflib import Graph

# Locate the project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RDF_FILE = BASE_DIR / "output" / "miu_integrated_data.ttl"

# Load the integrated RDF graph
g = Graph()
g.parse(RDF_FILE, format="turtle")

print("MIU SEMANTIC DATA INTEGRATION - SPARQL QUERIES")
print("=" * 55)


# QUERY 1: Retrieve all students and their departments
query1 = """
PREFIX miu: <http://www.miu.ac.ke/ontology/university#>

SELECT ?studentID ?firstName ?lastName ?department
WHERE {
    ?student a miu:Student ;
             miu:studentID ?studentID ;
             miu:firstName ?firstName ;
             miu:lastName ?lastName ;
             miu:belongsToDepartment ?department .
}
ORDER BY ?studentID
"""

print("\nQUERY 1: STUDENTS AND DEPARTMENTS")
print("-" * 55)

for row in g.query(query1):
    print(row.studentID, row.firstName, row.lastName, row.department.split("/")[-1])


# QUERY 2: Retrieve students and their enrolled courses
query2 = """
PREFIX miu: <http://www.miu.ac.ke/ontology/university#>

SELECT ?studentID ?firstName ?courseCode ?courseName
WHERE {
    ?student a miu:Student ;
             miu:studentID ?studentID ;
             miu:firstName ?firstName ;
             miu:hasEnrolment ?enrolment .

    ?enrolment miu:isForCourse ?course .

    ?course miu:courseCode ?courseCode ;
            miu:courseName ?courseName .
}
ORDER BY ?studentID
"""

print("\nQUERY 2: STUDENT ENROLMENTS AND COURSES")
print("-" * 55)

for row in g.query(query2):
    print(row.studentID, row.firstName, row.courseCode, row.courseName)


# QUERY 3: Retrieve student fee records
query3 = """
PREFIX miu: <http://www.miu.ac.ke/ontology/university#>

SELECT ?studentID ?firstName ?tuitionFee ?amountPaid ?outstandingBalance
WHERE {
    ?student a miu:Student ;
             miu:studentID ?studentID ;
             miu:firstName ?firstName ;
             miu:hasFeeRecord ?fee .

    ?fee miu:tuitionFee ?tuitionFee ;
         miu:amountPaid ?amountPaid ;
         miu:outstandingBalance ?outstandingBalance .
}
ORDER BY ?studentID
"""

print("\nQUERY 3: STUDENT FINANCIAL RECORDS")
print("-" * 55)

for row in g.query(query3):
    print(
        row.studentID,
        row.firstName,
        row.tuitionFee,
        row.amountPaid,
        row.outstandingBalance
    )


# QUERY 4: Retrieve students with outstanding balances
query4 = """
PREFIX miu: <http://www.miu.ac.ke/ontology/university#>

SELECT ?studentID ?firstName ?outstandingBalance
WHERE {
    ?student a miu:Student ;
             miu:studentID ?studentID ;
             miu:firstName ?firstName ;
             miu:hasFeeRecord ?fee .

    ?fee miu:outstandingBalance ?outstandingBalance .

    FILTER (?outstandingBalance > 0)
}
ORDER BY DESC(?outstandingBalance)
"""

print("\nQUERY 4: STUDENTS WITH OUTSTANDING FEES")
print("-" * 55)

for row in g.query(query4):
    print(row.studentID, row.firstName, row.outstandingBalance)


print("\n" + "=" * 55)
print("SPARQL QUERIES EXECUTED SUCCESSFULLY")
print("Total RDF triples:", len(g))
