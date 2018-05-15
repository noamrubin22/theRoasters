
import csv
import random
import math
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

	def createPracticalGroup(self, prac, studentlist):

		self.practicalgroups[prac] = studentlist

	def updateSchedule(self, roomlock, activity, group):
		self.activities.append([roomlock, activity, group]) 

	def __str__(self):
		return "Name: %s \nNumber of lectures: %s\nNumber of seminars: %s \nNumber of practicals: %s \n" % (self.name, self.lectures, self.seminars, self.practicals)

# create empty list

if __name__=='__main__':

	chambers = []

	# reads csv file
	with open('../data/zalen.csv', 'rt') as csvfile:
		
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

	# print(chambers)


# create list for courses
allcourses = []

# load courses as classes in allcourses-list
with open('../data/vakken.csv', 'rt') as coursefile:
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
		activity = course.seminars
	elif typeClass == "practical":
		activity = course.practicals

	while activity > 0:
		# choose random roomlock
		pickroomlock = random.randint(0, 139)
		# pick new random roomlock if room is not empty at that time
		while schedule[pickroomlock] is not None:
			pickroomlock = random.randint(0, 139)

		room, timelock = translateRoomlock(pickroomlock)

		if typeClass == "lecture":
			while (course.students > int(chambers[room].capacity)) or schedule[pickroomlock] is not None:
				pickroomlock = random.randint(0, 139)
				room, timelock = translateRoomlock(pickroomlock)
		elif typeClass == "seminar": 
			while course.maxstudentssem > int(chambers[room].capacity) or schedule[pickroomlock] is not None:
				pickroomlock = random.randint(0, 139)
				room, timelock = translateRoomlock(pickroomlock)
		elif typeClass == "practical": 
			while course.maxstudentsprac > int(chambers[room].capacity) or schedule[pickroomlock] is not None:
				pickroomlock = random.randint(0, 139)
				room, timelock = translateRoomlock(pickroomlock)

		# schedule lecture in roomlock
		schedule[pickroomlock] = course.name + " " + typeClass

		if typeClass == "lecture":
			group = 0
		else:
			group = activity

		# put scheduled lecture in course class
		course.updateSchedule(pickroomlock, (course.name + " " + typeClass), group)
		# add scheduled lecture to room class
		room, timelock = translateRoomlock(pickroomlock)
		chambers[room].add_booking(timelock)


		if typeClass == "lecture":
			for student in student_list:
				if course.name in student.courses:
					student.updateStudentSchedule(timelock, course.name)

		if typeClass == "seminar":
			for student in student_list:
				if course.name in student.courses:
					if student.last_name in course.seminargroups[activity]:
						student.updateStudentSchedule(timelock, course.name)

		if typeClass == "practical":
			for student in student_list:
				if course.name in student.courses:
					if student.last_name in course.practicalgroups[activity]:
						student.updateStudentSchedule(timelock, course.name)

		activity -= 1


		


# loop through courses to schedule classes of course one-by-one
for course in allcourses:

	for student in student_list:
		if course.name in student.courses:
			course.addStudent(student.last_name)

	if  course.seminars > 0:
		numofseminars = math.ceil(course.students/course.maxstudentssem)
		course.addSeminar(numofseminars)

	if  course.practicals > 0:
		numofpracticals = math.ceil(course.students/course.maxstudentsprac)
		course.addPractical(numofpracticals)

	sem = 1
	if course.seminars > 0:
		for i in range(0, len(course.studentnames), course.maxstudentssem):
			studentlist = course.studentnames[i: i + course.maxstudentssem]
			course.createSeminarGroup(sem, studentlist)
			sem += 1

	prac = 1
	if course.practicals > 0:
		for i in range(0, len(course.studentnames), course.maxstudentsprac):
			studentlist = course.studentnames[i: i + course.maxstudentsprac]
			course.createPracticalGroup(prac, studentlist)
			prac += 1


	# schedule lectures while course has still lectures left to schedule
	scheduleClass(course, "lecture", schedule)
	scheduleClass(course, "seminar", schedule)
	scheduleClass(course, "practical", schedule)

# print(allcourses[1].studentnames)

print(schedule) # heel schedule
# print(student_list[0].schedule)
print(allcourses[4].activities)
# print(allcourses[4].practicalgroups[3])
# print(allcourses[4].practicals)
# print(student_list[511].schedule)

# print(allcourses[5].seminargroups[0]) # activiteiten van vak
# # print(chambers[1].booking) # bookings van een zaal
# print(allcourses[5].studentnames)

# valid schedule has been made: 1000 points
points = 1000;

# subtract or add points based on schedule
# loop through courses
for course in allcourses:
	# print(course.name)
	if course.seminars > 0:
		groups = list(range(1, course.seminars + 1))
	elif course.practicals > 0:
		groups = list(range(1, course.practicals + 1))
		# print(groups)
	else:
		groups = [1]

	dayActivity = {k: [] for k in groups}

	# loop trough activities of a course
	for activity in course.activities:
		day = int(activity[0]/28)
		if activity[2] == 0:
			if day in dayActivity[1]:
				points -= 10	
			for group in groups:	
				dayActivity[group].append(day)
		else:
			if day in dayActivity[activity[2]]:
				points -= 10
			dayActivity[activity[2]].append(day) 
	# print(course.name, dayActivity)

	for group in groups:
		if (len(dayActivity[group]) == 2):
			if (abs(dayActivity[group][0] - dayActivity[group][1]) >= 3):
				points += 20
		# if three activities in the week: mo-we-fr?
		if (len(dayActivity[group]) == 3):
			if 0 in dayActivity[group] and 2 in dayActivity[group] and 4 in dayActivity[group]:
				points += 20
		# if four activities in the week: mo-tu-th-fr?
		if (len(dayActivity[group]) == 4):
			if 0 in dayActivity[group] and 1 in dayActivity[group] and 3 in dayActivity[group] and 4 in dayActivity[group]:
				points += 20


	
print(student_list[0].schedule)

for student in student_list:
	timelocksStudent = []
	for activity in student.schedule:
		if activity[0] in timelocksStudent:
			points -= 1
		timelocksStudent.append(activity[0])

for course in allcourses:
	for activity in course.activities:
		room, timelock = translateRoomlock(activity[0])
		if activity[2] == 0:
			if int(chambers[room].capacity) < course.students:
				print(chambers[room].capacity)
				print(course.students)
				print("te veel studenten: past niet in de zaal!")
				maluspoints = course.students - int(chambers[room].capacity)
				print(maluspoints)
				points -= maluspoints
		else:
			if course.seminars > 0:
				if int(chambers[room].capacity) < course.maxstudentssem:
					print(chambers[room].capacity)
					print(course.maxstudentssem)
					maluspoints = course.maxstudentssem - int(chambers[room].capacity)
					print(maluspoints)
					points -= maluspoints

# laat eindscore zien (so far)
print("Points: ", points)
