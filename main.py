
import csv
import random
from parse import *
from students_class import Students

class Room:
	""" Adds features to room """

	def __init__(self, name, capacity): 
		self.name = name
		self.capacity = capacity
		self.booking = []

	def add_booking(self, timelock):
		""" Blocks time lock """

		self.booking.append(timelock)

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
		self.seminargroups = {0 : []}
		

	def addStudent(self, name):
		""" Add student to course """
		self.students += 1
		self.studentnames.append(name)

	def addSeminar(self):
		self.seminars += 1

	def addPractical(self):
		self.practicals += 1

	def createSeminarGroup(self, sem, studentlist):

		self.seminargroups[sem] = studentlist

	def updateSchedule(self, roomlock, activity):
		self.activities.append([roomlock, activity]) 

	def __str__(self):
		return "Name: %s \nNumber of lectures: %s\nNumber of seminars: %s \nNumber of practicals: %s \n" % (self.name, self.lectures, self.seminars, self.practicals)

# create empty list

if __name__=='__main__':

	chambers = []

	# reads csv file
	with open('zalen.csv', 'rt') as csvfile:
		
		# creates csvfile
		rooms = csv.reader(csvfile)

		# iterate over rows 
		for row in rooms:

			# extract text out of list
			for text in row: 

				# split features
				features = text.split(";")

				# initilize features for class 
				name = features[0] 
				capacity = features[1]

				# initilaze room using the class
				room = Room(name, capacity)

				# add room to list
				chambers.append(room)

	print(chambers)


# create list for courses
allcourses = []

# load courses as classes in allcourses-list
with open('vakken.csv', 'rt') as coursefile:
	courses = csv.reader(coursefile)
	for row in courses:
		for text in row:
			courseInfo = text.split(";")
			courseName = courseInfo[0]
			courseLectures = courseInfo[1]
			courseSeminars = courseInfo[2]
			courseMaxSem = courseInfo[3]
			if courseMaxSem == "nvt":
				courseMaxSem = 0 
			coursePracticals = courseInfo[4]
			courseMaxPrac = courseInfo[5]
			if courseMaxPrac == "nvt":
				courseMaxPrac = 0
			allcourses.append(Course(courseName, courseLectures, courseSeminars, courseMaxSem, coursePracticals, courseMaxPrac))

# import student classes
student_list = createStudentClass()

# create empty dictionary with all room-timelock combinations (roomlocks) as keys
roomlocks = list(range(0, 140))
schedule = dict.fromkeys(roomlocks)


def translateRoomlock(roomlock):
	""" Translates roomlock number to roomnumber and timelock """
	room = roomlock % 7
	timelock = int(roomlock/7)
	return room, timelock

def scheduleClass(course, typeClass, schedule):
	if typeClass == "lecture":
		activity = course.lectures
	elif typeClass == "seminar":
		activity = course.seminargroups
	elif typeClass == "practical":
		activity = course.practicals

	while activity > 0:
		# choose random roomlock
		pickroomlock = random.randint(0, 139)
		# pick new random roomlock if room is not empty at that time
		# dit errort trouwens soms, meestal niet (nog naar kijken!)
		while schedule[pickroomlock] is not None:
			pickroomlock = random.randint(0, 139)
		# schedule lecture in roomlock
		schedule[pickroomlock] = course.name + " " + typeClass
		activity -= 1
		# put scheduled lecture in course class
		course.updateSchedule(pickroomlock, course.name)
		# add scheduled lecture to room class
		room, timelock = translateRoomlock(pickroomlock)
		chambers[room].add_booking(timelock)


		# if typeClass == 
		for student in student_list:
			if course.name in student.courses:
				student.updateStudentSchedule(timelock, course.name)


		


# loop through courses to schedule classes of course one-by-one
for course in allcourses:

	for student in student_list:
		if course.name in student.courses:
			course.addStudent(student.last_name)

	if  course.seminars > 0:
		numofseminars = int(course.students/course.maxstudentssem)
		for i in range(numofseminars):
			course.addSeminar()



	if  course.practicals > 0:
		numofpracticals = int(course.students/course.maxstudentsprac)
		for i in range(numofpracticals):
			course.addPractical()

	# for student in course.studentnames:
	# 	sem = random.randint(0, course.seminars)
	# 	print(sem)
		# while len(course.seminargroups[sem]) >= course.maxstudentssem:
		# 	sem = random.randint(0, course.seminars)
		# createSeminarGroup(sem, student.last_name)
	# print(course.studentnames)
	# if len(course.studentnames) != 0:
	# 	pickstudent = random.choice(course.studentnames)
	# 	print(pickstudent)
	sem = 0
	print(course.maxstudentssem)
	if course.seminars > 0:
		for i in range(0, len(course.studentnames), course.maxstudentssem):
			studentlist = course.studentnames[i: i + course.maxstudentssem]
			course.createSeminarGroup(sem, studentlist)
			sem += 1

	# groupcounter = 0
	# sem = 0
	# studentlist = []
	# if course.seminars > 0:
	# 	for student in course.studentnames:
	# 		groupcounter += 1
	# 		studentlist.append(student)

	# 		if len(studentlist) >= course.maxstudentssem:
	# 			# print(course.maxstudentssem)
	# 			course.createSeminarGroup(sem, studentlist)
	# 			sem += 1
	# 			print(sem)
	# 			studentlist = []

	# print(course.seminargroups)


	# schedule lectures while course has still lectures left to schedule
	scheduleClass(course, "lecture", schedule)
	scheduleClass(course, "seminar", schedule)
	scheduleClass(course, "practical", schedule)

print(allcourses[1].studentnames)
print(allcourses[1].seminargroups)
# even voor visualisatie

print(schedule) # heel schedule
print(student_list[0].schedule)
# print(allcourses[5].activities) # activiteiten van vak
# # print(chambers[1].booking) # bookings van een zaal
# print(int(0.5))
# print(allcourses[5].studentnames)
# valid schedule has been made: 1000 points
points = 1000;

# subtract or add points based on schedule
# loop through courses
for course in allcourses:
	# print(course.name)
	dayActivity = []
	# loop trough activities of a course
	for activity in range(0, len(course.activities)):
		# determine day of activity
		timelock = course.activities[activity][0]
		day = int(timelock/28)
		# if day has more than one activity in one day: subtract 10 points
		if day in dayActivity:
			points -= 10
		# add day of activity to array of days of activities
		dayActivity.append(day)
	
	# check if classes are distributed over the week
	# if two activities in the week: mo-th, tu-fr or mo-fr?
	if (len(course.activities) == 2):
		if (abs(dayActivity[0] - dayActivity[1]) >= 3):
			points += 20
	# if three activities in the week: mo-we-fr?
	if (len(course.activities) == 3):
		if 0 in dayActivity and 2 in dayActivity and 4 in dayActivity:
			points += 20
	# if four activities in the week: mo-tu-th-fr?
	if (len(course.activities) == 4):
		if 0 in dayActivity and 1 in dayActivity and 3 in dayActivity and 4 in dayActivity:
			points += 20
	
	# laat even zien welke dagen er activiteiten zijn voor dit vak
	# print("dag(en): ", dayActivity)


	
# print(student_list[0].schedule)

# for student in student_list:
# 	timelocksStudent = []
# 	for activity in student.schedule:
# 		if activity[0] in timelocksStudent:
# 			points -= 1
# 		timelocksStudent.append(activity[0])

# for course in allcourses:
# 	for activity in course.activities:
# 		room, timelock = translateRoomlock(activity[0])
# 		if int(chambers[room].capacity) < course.students:
# 			print(chambers[room].capacity)
			# print(course.students)
			# print("te veel studenten: past niet in de zaal!")


# laat eindscore zien (so far)
print("Points: ", points)