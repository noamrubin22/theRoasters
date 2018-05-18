
import csv
import random
import math
from parse import *
from classes import Students, Room, Course

# create empty list



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


print(allcourses[9].practicals)
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

		# if typeClass == "lecture":
		# 	while (course.students > int(chambers[room].capacity)) or schedule[pickroomlock] is not None:
		# 		pickroomlock = random.randint(0, 139)
		# 		room, timelock = translateRoomlock(pickroomlock)
		# elif typeClass == "seminar":
		# 	while course.maxstudentssem > int(chambers[room].capacity) or schedule[pickroomlock] is not None:
		# 		pickroomlock = random.randint(0, 139)
		# 		room, timelock = translateRoomlock(pickroomlock)
		# elif typeClass == "practical":
		# 	while course.maxstudentsprac > int(chambers[room].capacity) or schedule[pickroomlock] is not None:
		# 		pickroomlock = random.randint(0, 139)
		# 		room, timelock = translateRoomlock(pickroomlock)

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

	print(allcourses[9].practicals)
	if  course.practicals > 0:
		numofpracticals = math.ceil(course.students/course.maxstudentsprac)
		print("students: ", allcourses[9].students)
		print("maxstud: ", allcourses[9].maxstudentsprac)
		print("num of prac ", numofpracticals)
		course.addPractical(numofpracticals)
	print(allcourses[9].practicals)
	print(student_list[170].courses)
	

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

# print(schedule) # heel schedule
# # print(student_list[0].schedule)
# print(allcourses[4].activities)
# print(chambers)
# print(allcourses[4].practicalgroups[3])
# print(allcourses[4].practicals)
# print(student_list[511].schedule)

# print(allcourses[5].seminargroups[0]) # activiteiten van vak
# # print(chambers[1].booking) # bookings van een zaal
# print(allcourses[5].studentnames)
