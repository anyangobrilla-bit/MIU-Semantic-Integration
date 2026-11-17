
from pathlib import Path
from rdflib import Graph, Namespace, RDF

# Locate the integrated RDF file
BASE_DIR = Path(__file__).resolve().parent.parent
RDF_FILE = BASE_DIR / "output" / "miu_integrated_data.ttl"

# Load RDF graph
g = Graph()
g.parse(RDF_FILE, format="turtle")

MIU = Namespace("http://www.miu.ac.ke/ontology/university#")

print("MIU SEMANTIC INTEGRATION VALIDATION")
print("=" * 50)

# Test 1: Check student records
students = set(g.subjects(RDF.type, MIU.Student))
student_count = len(students)

print("\nTEST 1: STUDENT RECORDS")
print("Students found:", student_count)
print("Expected: 5")
print("Result:", "PASS" if student_count == 5 else "FAIL")

# Test 2: Check academic enrolment records
enrolments = set(g.subjects(RDF.type, MIU.Enrolment))
enrolment_count = len(enrolments)

print("\nTEST 2: ACADEMIC ENROLMENT RECORDS")
print("Enrolments found:", enrolment_count)
print("Expected: 5")
print("Result:", "PASS" if enrolment_count == 5 else "FAIL")

# Test 3: Check fee records
fee_records = set(g.subjects(RDF.type, MIU.FeeRecord))
fee_count = len(fee_records)

print("\nTEST 3: FINANCIAL RECORDS")
print("Fee records found:", fee_count)
print("Expected: 5")
print("Result:", "PASS" if fee_count == 5 else "FAIL")

# Test 4: Check student-enrolment relationships
student_enrolment_links = list(g.triples(
    (None, MIU.hasEnrolment, None)
))

print("\nTEST 4: STUDENT-ENROLMENT LINKS")
print("Links found:", len(student_enrolment_links))
print("Expected: 5")
print(
    "Result:",
    "PASS" if len(student_enrolment_links) == 5 else "FAIL"
)

# Test 5: Check student-fee relationships
student_fee_links = list(g.triples(
    (None, MIU.hasFeeRecord, None)
))

print("\nTEST 5: STUDENT-FINANCE LINKS")
print("Links found:", len(student_fee_links))
print("Expected: 5")
print(
    "Result:",
    "PASS" if len(student_fee_links) == 5 else "FAIL"
)

# Test 6: Check course relationships
course_links = list(g.triples(
    (None, MIU.isForCourse, None)
))

print("\nTEST 6: ENROLMENT-COURSE LINKS")
print("Links found:", len(course_links))
print("Expected: 5")
print(
    "Result:",
    "PASS" if len(course_links) == 5 else "FAIL"
)

# Test 7: Check outstanding financial balances
outstanding_balances = [
    float(balance)
    for balance in g.objects(None, MIU.outstandingBalance)
]

total_outstanding = sum(outstanding_balances)

print("\nTEST 7: OUTSTANDING BALANCE CHECK")
print("Total outstanding: KES", total_outstanding)
print("Expected: KES 55000")
print(
    "Result:",
    "PASS" if total_outstanding == 55000 else "FAIL"
)

# Final validation summary
tests = [
    student_count == 5,
    enrolment_count == 5,
    fee_count == 5,
    len(student_enrolment_links) == 5,
    len(student_fee_links) == 5,
    len(course_links) == 5,
    total_outstanding == 55000
]

passed = sum(tests)
failed = len(tests) - passed

print("\n" + "=" * 50)
print("VALIDATION SUMMARY")
print("Total tests:", len(tests))
print("Passed:", passed)
print("Failed:", failed)
print("Total RDF triples:", len(g))

if failed == 0:
    print("OVERALL RESULT: ALL VALIDATION TESTS PASSED")
else:
    print("OVERALL RESULT: SOME VALIDATION TESTS FAILED")
