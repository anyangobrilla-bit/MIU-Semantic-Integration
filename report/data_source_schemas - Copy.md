# Meridian International University (MIU)
## Data Source Schema Documentation

### 1. Admissions Database – SQLite

**File:** `admissions.db`  
**Table:** `students`

| Field | Data Type | Description |
|---|---|---|
| student_id | INTEGER | Unique student identifier |
| first_name | TEXT | Student's first name |
| last_name | TEXT | Student's surname |
| admission_date | TEXT | Date of admission |
| department | TEXT | Academic department |

### 2. Academic Records – XML

**File:** `academics.xml`  
**Root element:** `UniversityAcademicRecords`

| XML Element | Data Type | Description |
|---|---|---|
| University | TEXT | University name |
| StudentNumber | TEXT | Student identifier |
| CourseCode | TEXT | Course identification code |
| CourseName | TEXT | Course title |

Each `Enrolment` element represents one student's course enrolment.

### 3. Finance Records – CSV

**File:** `finance.csv`

| Field | Data Type | Description |
|---|---|---|
| StudentRef | INTEGER | Student identifier |
| TuitionFee | INTEGER | Total tuition fee |
| AmountPaid | INTEGER | Amount already paid |
| OutstandingBalance | INTEGER | Remaining fee balance |

### 4. Relationships Between the Data Sources

The three data sources share a common student identifier:

- SQLite: `student_id`
- XML: `StudentNumber`
- CSV: `StudentRef`

These fields refer to the same student and will be used to connect the three datasets during semantic integration.

### 5. Summary

The project uses three heterogeneous data sources: SQLite for admissions, XML for academic enrolments, and CSV for financial records. Semantic integration will bring these separate sources together into a unified representation of student information at Meridian International University.