import csv
from classes import Students

MY_FILE = "../data/studenten_roostering.csv"

# create empty list for students
student_list = []

def parse(raw_file, delimiter):

    # open CSV file
    opened_file = open(raw_file)

    # read and clean CSV data
    csv_data = csv.reader((x.replace('\0', '') for x in opened_file), delimiter=delimiter)

    # Read the CSV data
#    csv_data = csv.reader(opened_file, delimiter=delimiter)

    # setup an empty list
    parsed_data = []

    # skip over the first line of the file for the headers
    fields = next(csv_data)

    # iterate over each row of the csv file, zip together field -> value
    for row in csv_data:
        parsed_data.append(dict(zip(fields, row)))

    # close the CSV file
    opened_file.close()

    return parsed_data

def gimme_students():
    return student_list;

def createStudentClass():

    # call our parse function and give it the needed parameters
    new_data = parse(MY_FILE, ";")

    # iterate over new data
    for i in range(len(new_data)):

        # extract all information
        last_name = new_data[i]['lastName']
        first_name = new_data[i]['firstName']
        student_id = new_data[i]['studentID']
        courses = []

        # dict1_values = {k*2:v for (k,v) in dict1.items()}
        # extract all courses from all students and add to list
        if new_data[i]['course_1'] is not '':
            courses.append(new_data[i]['course_1'])
        if new_data[i]['course_2'] is not '':
            courses.append(new_data[i]['course_2'])
        if new_data[i]['course_3'] is not '':
            courses.append(new_data[i]['course_3'])
        if new_data[i]['course_4'] is not '':
            courses.append(new_data[i]['course_4'])
        if new_data[i]['course_5'] is not '':
            courses.append(new_data[i]['course_5'])

        # append students to list with extracted info
        student_list.append(Students(last_name, first_name, student_id, courses))

    return student_list


if __name__ == "__main__":
    student_list = createStudentClass()
