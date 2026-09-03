import sqlite3
import re
from difflib import SequenceMatcher
def clean_name(name):
    if name is None:
        return "Unknown"
    return " ".join(name.split()).title()
def clean_gender(gender):
    if gender is None:
        return "Unknown"

    gender = gender.strip().lower()

    if gender in ["male", "m"]:
        return "Male"
    elif gender in ["female", "f"]:
        return "Female"
    else:
        return "Unknown"
def validate_phone(phone):
    if phone is None:
        return False
    phone = str(phone).strip()
    pattern = r"^[6-9]\d{9}$"
    return bool(re.fullmatch(pattern, phone))
def validate_email(email):
    if email is None or email.strip() == "":
        return False
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email))
def validate_age(age):
    if age is None:
        return False
    return 0 <= age <= 120
def find_fuzzy_duplicates(records):
    print("\nPOTENTIAL DUPLICATES USING FUZZY MATCHING")
    print("-" * 60)
    found = False
    for i in range(len(records)):

        for j in range(i + 1, len(records)):

            record1 = records[i]
            record2 = records[j]

            name1 = record1[1]
            name2 = record2[1]

            phone1 = record1[4]
            phone2 = record2[4]

            email1 = record1[5]
            email2 = record2[5]

            similarity = SequenceMatcher(
                None,
                name1.lower(),
                name2.lower()
            ).ratio() * 100

            if similarity >= 80:

                if phone1 == phone2 or email1 == email2:

                    print(
                        "Possible duplicate:",
                        name1,
                        "<->",
                        name2
                    )

                    print(
                        "Name similarity:",
                        round(similarity, 2),
                        "%"
                    )

                    found = True

    if not found:
        print("No potential duplicates found.")


# --------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------
def main():

    try:

        # ------------------------------------------
        # DATABASE CONNECTION
        # ------------------------------------------

        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()

        print("Database connected successfully!")


        # ------------------------------------------
        # CREATE PATIENT TABLE
        # ------------------------------------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Patient (
            Patient_ID INTEGER PRIMARY KEY,
            Name TEXT,
            Age INTEGER,
            Gender TEXT,
            Phone TEXT,
            Email TEXT,
            Diagnosis TEXT
        )
        """)


        # ------------------------------------------
        # CREATE CLEAN_PATIENT TABLE
        # ------------------------------------------

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clean_Patient (
            Patient_ID INTEGER PRIMARY KEY,
            Name TEXT,
            Age INTEGER,
            Gender TEXT,
            Phone TEXT,
            Email TEXT,
            Diagnosis TEXT
        )
        """)


        # Clear old records
        cursor.execute("DELETE FROM Patient")
        cursor.execute("DELETE FROM Clean_Patient")

        conn.commit()

        print("Tables created successfully!")


        # ------------------------------------------
        # DIRTY PATIENT RECORDS
        # ------------------------------------------

        patients = [

            (1, "RAHUL kumar", 25, "male",
             "9876543210", "rahul@gmail.com", "Fever"),

            (2, "rahul KUMAR", 25, "Male",
             "9876543210", "rahul@gmail.com", "Fever"),

            (3, "Anitha Devi", 30, "FEMALE",
             "987654321", "anitha@gmail.com", "Diabetes"),

            (4, "Ramesh Kumar", -5, "Male",
             "9876543211", "ramesh@gmail.com", "Cold"),

            (5, "Priya Sharma", 135, "female",
             "9876543212", "priya@gmail.com", "Headache"),

            (6, "Arun Kumar", 28, "M",
             None, "arun@gmail.com", "Fever"),

            (7, "Meena", 35, "Female",
             "9876543213", None, "Diabetes"),

            (8, "  Karthik   Raj  ", 40, "MALE",
             "abcdefghij", "karthik@gmail.com", "Cold"),

            (9, "Suresh Kumar", 45, "Male",
             "9876543214", "suresh@gmail.com",
             "Heart Problem"),

            (10, "Suresh Kumaar", 45, "male",
             "9876543214", "suresh123@gmail.com",
             "Heart Problem")
        ]


        # ------------------------------------------
        # INSERT RECORDS
        # ------------------------------------------

        cursor.executemany("""
        INSERT INTO Patient
        (Patient_ID, Name, Age, Gender, Phone, Email, Diagnosis)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, patients)

        conn.commit()

        print("Patient records inserted successfully!")


        # ------------------------------------------
        # DISPLAY ORIGINAL RECORDS
        # ------------------------------------------

        print("\n")
        print("=" * 70)
        print("ORIGINAL PATIENT RECORDS")
        print("=" * 70)

        cursor.execute("SELECT * FROM Patient")

        original_records = cursor.fetchall()

        for row in original_records:
            print(row)


        # ------------------------------------------
        # DATA CLEANING
        # ------------------------------------------

        cleaned_records = []
        seen_records = set()

        print("\n")
        print("=" * 70)
        print("DATA CLEANING PROCESS")
        print("=" * 70)


        for record in original_records:

            patient_id = record[0]
            name = record[1]
            age = record[2]
            gender = record[3]
            phone = record[4]
            email = record[5]
            diagnosis = record[6]


            # Clean name
            name = clean_name(name)


            # Clean gender
            gender = clean_gender(gender)


            # Validate age
            if not validate_age(age):

                print(
                    "Invalid age record removed:",
                    name,
                    "| Age:",
                    age
                )

                continue


            # Validate phone
            if not validate_phone(phone):

                print(
                    "Invalid or missing phone:",
                    name
                )

                phone = "Not Available"


            # Validate email
            if not validate_email(email):

                print(
                    "Invalid or missing email:",
                    name
                )

                email = "Not Available"


            # --------------------------------------
            # EXACT DUPLICATE DETECTION
            # --------------------------------------

            duplicate_key = (
                name.lower(),
                age,
                gender.lower(),
                phone,
                email.lower(),
                diagnosis.lower()
            )


            if duplicate_key in seen_records:

                print(
                    "Exact duplicate removed:",
                    name
                )

                continue


            seen_records.add(duplicate_key)


            cleaned_records.append(
                (
                    patient_id,
                    name,
                    age,
                    gender,
                    phone,
                    email,
                    diagnosis
                )
            )


        # ------------------------------------------
        # FUZZY MATCHING
        # ------------------------------------------

        find_fuzzy_duplicates(cleaned_records)


        # ------------------------------------------
        # STORE CLEAN RECORDS
        # ------------------------------------------

        cursor.executemany("""
        INSERT INTO Clean_Patient
        (Patient_ID, Name, Age, Gender, Phone, Email, Diagnosis)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, cleaned_records)

        conn.commit()

        print("\nCleaned records stored successfully!")


        # ------------------------------------------
        # DISPLAY CLEANED RECORDS
        # ------------------------------------------

        print("\n")
        print("=" * 70)
        print("CLEANED PATIENT RECORDS")
        print("=" * 70)

        cursor.execute("SELECT * FROM Clean_Patient")

        for row in cursor.fetchall():
            print(row)


        # ------------------------------------------
        # UPDATE OPERATION
        # ------------------------------------------

        print("\n")
        print("=" * 70)
        print("UPDATE OPERATION")
        print("=" * 70)

        cursor.execute("""
        UPDATE Clean_Patient
        SET Diagnosis = ?
        WHERE Patient_ID = ?
        """, ("Recovered", 1))

        conn.commit()

        cursor.execute("""
        SELECT * FROM Clean_Patient
        WHERE Patient_ID = 1
        """)

        print("Updated Record:")
        print(cursor.fetchone())


        # ------------------------------------------
        # DELETE OPERATION
        # ------------------------------------------

        print("\n")
        print("=" * 70)
        print("DELETE OPERATION")
        print("=" * 70)

        cursor.execute("""
        DELETE FROM Clean_Patient
        WHERE Name = ?
        """, ("Karthik Raj",))

        conn.commit()

        print("Record deletion operation completed.")


        # ------------------------------------------
        # TEST WITH NEW UNSEEN DIRTY DATA
        # ------------------------------------------

        print("\n")
        print("=" * 70)
        print("TESTING WITH NEW DIRTY DATA")
        print("=" * 70)


        test_patients = [

            (101, "rajesh KUMAR", 32, "male",
             "9876543299", "rajesh@gmail.com",
             "Fever"),

            (102, "RAJESH kumar", 32, "M",
             "9876543299", "rajesh@gmail.com",
             "Fever"),

            (103, "Divya", -10, "Female",
             "9876543201", "divya@gmail.com",
             "Cold"),

            (104, "Kiran", 26, "Male",
             "12345", None,
             "Headache")
        ]


        test_cleaned = []
        test_seen = set()


        for record in test_patients:

            patient_id = record[0]
            name = clean_name(record[1])
            age = record[2]
            gender = clean_gender(record[3])
            phone = record[4]
            email = record[5]
            diagnosis = record[6]
            if not validate_age(age):
                print(
                    "TEST FAILED - Invalid age removed:",
                    name
                )
                continue
            if not validate_phone(phone):

                print(
                    "Invalid phone detected:",
                    name
                )
                phone = "Not Available"
            if not validate_email(email):
                print(
                    "Missing or invalid email detected:",
                    name
                )
                email = "Not Available"
            duplicate_key = (
                name.lower(),
                age,
                gender.lower(),
                phone,
                email.lower(),
                diagnosis.lower()
            )
            if duplicate_key in test_seen:
                print(
                    "Duplicate test record removed:",
                    name
                )
                continue
            test_seen.add(duplicate_key)
            test_cleaned.append(
                (
                    patient_id,
                    name,
                    age,
                    gender,
                    phone,
                    email,
                    diagnosis
                )
            )
            print(
                "Clean test record:",
                name
            )
        print("\n")
        print("=" * 70)
        print("TEST RESULTS")
        print("=" * 70)
        print("Total test records:", len(test_patients))
        print("Successfully processed:", len(test_cleaned))
        print("\nFinal Clean Test Records:")
        for record in test_cleaned:
            print(record)
        conn.close()
        print("\nDatabase connection closed.")
        print("Program executed successfully!")
    except sqlite3.Error as error:
        print("Database Error:", error)
if __name__ == "__main__":
    main()
