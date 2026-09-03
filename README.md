# Hospital Patient Data Management

## Project Description

This project is developed using Python and SQLite to manage hospital patient information and perform data cleaning operations.

## Features

* Python and SQLite database connectivity
* Patient table creation
* Patient data insertion
* SQL CRUD operations
* Duplicate record detection
* Name normalization and standardization
* Gender value standardization
* Phone number validation using Regular Expressions
* Missing value handling
* Invalid age detection
* Fuzzy matching for potential duplicate patients
* Cleaned data storage in a separate table
* Testing with previously unseen dirty data

## Technologies Used

* Python
* SQLite
* Regular Expressions
* Difflib for fuzzy matching

## Project Structure

```text
Hospital-Patient-Data-Management/
│
├── hospital_patient_management.py
├── hospital.db
├── README.md
│
└── screenshots/
    ├── original_records.png
    ├── cleaned_records.png
    └── test_results.png
```

## How to Run

1. Download or clone the repository.
2. Open the project folder.
3. Run the following command:

```bash
python hospital_patient_management.py
```

## Output

The program creates the Patient and Clean_Patient tables, cleans invalid and inconsistent patient data, detects duplicates, and stores valid records in the Clean_Patient table.
