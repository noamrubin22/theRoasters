class Students:

    def __init__(self, last_name, first_name, student_ID, courses):
        self.last_name = last_name
        self.first_name = first_name
        self.student_ID = student_ID
        self.courses = courses

    def add_course(self, course):
        self.courses.append(self.course)

    def print_student(self):
        print("The name of the student is {} with student ID of {}, and takes the following courses: {}."
        .format(self.name, self.student_ID, self.courses))

    def updateStudentSchedule(self, timelock, course):
        self.schedule.append([timelock, course])

    def __str__(self):
        return "Name: %s %s, ID: %s" % (self.first_name, self.last_name, self.student_ID)
