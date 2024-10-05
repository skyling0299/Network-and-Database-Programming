import sqlite3

# link to the database
conn = sqlite3.connect('./test.db')
# create a cursor
cursor = conn.cursor()

# insert a data to student table
def insert_student(SID, fname, lname, grade, sex):
    cursor.execute("INSERT INTO student (SID, fname, lname, grade, sex) VALUES (?, ?, ?, ?, ?)", (SID, fname, lname, grade, sex))
    conn.commit()

# insert a data to course table
def insert_course(CID, fname):
    cursor.execute("INSERT INTO course (CID, fname) VALUES (?, ?)", (CID, fname))
    conn.commit()

# insert a data to enrollment table
def insert_enrollment(SID, CID, midscore=None, finalscore=None):
    SIDCID = SID + CID
    # search if the SIDCID already exists, update the data
    # if midscore or finalscore is None, don't update that column

    cursor.execute("SELECT * FROM enrollment WHERE SIDCID = ?", (SIDCID,))
    if cursor.fetchone():
        if midscore == None:
            # get midscore from cursor
            cursor.execute("SELECT midscore FROM enrollment WHERE SIDCID = ?", (SIDCID,))
            midscore = cursor.fetchone()[0]
        if finalscore == None:
            cursor.execute("SELECT finalscore FROM enrollment WHERE SIDCID = ?", (SIDCID,))
            finalscore = cursor.fetchone()[0]
        cursor.execute("UPDATE enrollment SET midscore = ?, finalscore = ? WHERE SIDCID = ?", (midscore, finalscore, SIDCID))
        conn.commit()
        return
    # if the SIDCID does not exist, insert the data
    else:
        cursor.execute("INSERT INTO enrollment (SID, CID, midscore, finalscore, SIDCID) VALUES (?, ?, ?, ?, ?)", (SID, CID, midscore, finalscore, SIDCID))
        conn.commit()

def get_course_score(CID):
    cursor.execute("SELECT SID, midscore, finalscore FROM enrollment WHERE CID = ?", (CID,))
    # print a table of SID, TotalScore
    # Totalscore will be 0.4 * midscore + 0.6 * finalscore
    print("SID\t\tMidterm\tFinal\tTotalScore")
    for row in cursor.fetchall():
        print(row[0], "\t", row[1], "\t", row[2], "\t", 0.4 * row[1] + 0.6 * row[2])
    return cursor.fetchall()

def main():
    # let user chose what to input, option 1, 2, 3, 4
    while True:
        print("1. Insert student")
        print("2. Insert course")
        print("3. Insert enrollment")
        print("4. Get course score")
        print("5. Exit")
        option = input("Enter the option: ")
        if option == "1":
            SID = input("Enter SID: ")
            fname = input("Enter first name: ")
            lname = input("Enter last name: ")
            grade = input("Enter grade: ")
            sex = input("Enter sex: ")
            insert_student(SID, fname, lname, grade, sex)
        elif option == "2":
            CID = input("Enter CID: ")
            fname = input("Enter course name: ")
            insert_course(CID, fname)
        elif option == "3":
            SID = input("Enter SID: ")
            CID = input("Enter CID: ")
            midscore = input("Enter mid score: ")
            finalscore = input("Enter final score: ")
            insert_enrollment(SID, CID, midscore, finalscore)
        elif option == "4":
            CID = input("Enter CID: ")
            get_course_score(CID)
        elif option == "5":
            break

if __name__ == "__main__":
    main()
    conn.close()