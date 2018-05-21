import copy

class Students:

    def __init__(self, last_name, first_name, student_ID, courses):
        self.last_name = last_name
        self.first_name = first_name
        self.student_ID = student_ID
        self.courses = courses
        self.schedule = []

    def add_course(self, course):
        self.courses.append(self.course)

    def print_student(self):
        print("The name of the student is {} with student ID of {}, and takes the following courses: {}."
        .format(self.name, self.student_ID, self.courses))

    def updateStudentSchedule(self, timelock, course):
        self.schedule.append([timelock, course])

    def changeStudentSchedule(self, oldtimelock, newtimelock, course):
    	for activity in self.schedule:
    		if activity[0] == oldtimelock and activity[1] == course:
    			activity[0] = newtimelock
    			# lelijke fix: dit is voor dubbel resetten om een of andere reden
    			break



    def __str__(self):
        return "Name: %s %s, ID: %s" % (self.first_name, self.last_name, self.student_ID)


class Room:
	""" Adds features to room """

	def __init__(self, name, capacity):
		self.name = name
		self.capacity = capacity
		self.booking = []

	def add_booking(self, timelock):
		""" Blocks time lock """

		self.booking.append(timelock)

	def changeBooking(self, oldtimelock, newtimelock):
		for booking in self.booking:
			if booking == oldtimelock:
				# print("EERST ZAAL", self.name, booking)
				booking = newtimelock
				# print("DAARNA: ", self.name, booking)

	def __str__(self):
		return str(self.name)

	__repr__ = __str__


class Course:
	""" Add features to course """

	def __init__(self, name, lectures, seminar, maxstudentssem, practical, maxstudentsprac):
		self.name = name
		self.lectures = int(lectures)
		self.seminars = int(seminar)
		self.practicals = int(practical)
		self.activities = []
		self.maxstudentssem = int(maxstudentssem)
		self.maxstudentsprac = int(maxstudentsprac)
		self.students = 0
		self.studentnames = []
		self.seminargroups = {1 : []}
		self.practicalgroups = {1 : []}

	def addStudent(self, name):
		""" Add student to course """
		self.students += 1
		self.studentnames.append(name)

	def addSeminar(self, num):
		self.seminars = num

	def addPractical(self, num):
		self.practicals = num

	def createSeminarGroup(self, sem, studentlist):

		self.seminargroups[sem] = studentlist

	def switchSeminarStudent(self, sem1, sem2, student1, student2):

		student1name = self.seminargroups[sem1][student1]
		student2name = self.seminargroups[sem2][student2]

		self.seminargroups[sem1][student1] = student2name
		self.seminargroups[sem2][student2] = student1name

	def createPracticalGroup(self, prac, studentlist):

		self.practicalgroups[prac] = studentlist

	def switchPracticalStudent(self, prac1, prac2, student1, student2):

		student1name = self.practicalgroups[prac1][student1]
		student2name = self.practicalgroups[prac2][student2]

		self.practicalgroups[prac1][student1] = student2name
		self.practicalgroups[prac2][student2] = student1name

	def updateSchedule(self, roomlock, activity, group):
		self.activities.append([roomlock, activity, group])

	def changeSchedule(self, newroomlock, schedulespot):
		self.activities[schedulespot][0] = newroomlock 

	def __str__(self):
		return "Name: %s \nNumber of lectures: %s\nNumber of seminars: %s \nNumber of practicals: %s \n" % (self.name, self.lectures, self.seminars, self.practicals)
