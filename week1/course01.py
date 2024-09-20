# week1
# propose: use one csv to store data of student(name, ID)
#         and use another csv to store data of course(name, ID)
#         and use another csv to store data of score of student in course(studentID, courseID, score)

import csv
import os


# add student
def add_student():
    student_name, student_id = input("Please input student name and ID: ").split(',')
    # use 'r' to check if student ID already exists
    with open('student.csv', 'r') as file:
        for row in csv.reader(file):
            if row[0] == student_id:
                print("Student ID already exists")
                return
    with open('student.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([student_id, student_name])
    print("Add student successfully")

# add course
def add_course():
    course_name, course_id = input("Please input course name and ID: ").split(',')
    with open('course.csv', 'a+', newline='') as file:
        # check if redundant
        for row in csv.reader(file):
            if row[0] == course_id:
                print("Course ID already exists")
                return
        writer = csv.writer(file)
        writer.writerow([course_id, course_name])
    print("Add course successfully")

# add data
def add_data():
    student_id, course_id, score = input("Please input student ID, course ID and score: ").split(',')
    # check if the student and course exist
    student_exist = False
    course_exist = False
    for row in csv.reader(open('student.csv', 'r')):
        if row[0] == student_id:
            student_exist = True
            break
    for row in csv.reader(open('course.csv', 'r')):
        if row[0] == course_id:
            course_exist = True
            break
    if not student_exist:
        print("Student not exist")
        return
    if not course_exist:
        print("Course not exist")
        return
    
    with open('data.csv', 'a+', newline='') as file:
        # if same student and course, update the score
        for row in csv.reader(file):
            if row[0] == student_id and row[1] == course_id:
                row[2] = score
                print("Update score successfully")
                return
        writer = csv.writer(file)
        writer.writerow([student_id, course_id, score])

# search student score
def search_student_score():
    student_name = input("Please input student name: ")
    print("Student ID\tCourse ID\tScore")
    # find student name in student.csv, get student ID
    student_id = None
    for row in csv.reader(open('student.csv', 'r')):
        if row[1] == student_name:
            student_id = row[0]
            break
    if student_id == None:
        print("Student not exist")
        return
    with open('data.csv', 'r') as file:
        for row in csv.reader(file):
            if row[0] == student_id:
                # print like table
                print(f"{row[0]}\t{row[1]}\t{row[2]}")
    print("Search successfully")

# main
def main():
    # use input options to choose the function
    # while loop to keep the program running
    # add three csv
    if not os.path.exists('student.csv'):
        with open('student.csv', 'w', newline='') as file:
            csv.writer(file)

    if not os.path.exists('course.csv'):
        with open('course.csv', 'w', newline='') as file:
            csv.writer(file)

    if not os.path.exists('data.csv'):
        with open('data.csv', 'w', newline='') as file:
            csv.writer(file)

    while True:
        print("a. Add student \n b. Add course \n c. Add data \n d. Search student score \n e. Exit")
        option = input("Please choose the function: ")
        if option == 'a':
            add_student()
        elif option == 'b':
            add_course()
        elif option == 'c':
            add_data()
        elif option == 'd':
            search_student_score()
        elif option == 'e':
            break
        else:
            print("Invalid option")


if __name__ == '__main__':
    main()