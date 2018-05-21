import csv
import random
import math
from parse import *
from classes import Students, Room, Course
import cProfile, pstats, io
import time

# global storage variables
allcourses = []
chambers = []
schedule = {}

def prepareData():
	""" Creates lists for rooms, students and courses and schedule dict """

	#* substract room information *#

	# create empty list
	chambers = []

	# read csv file with rooms
	with open('../data/zalen.csv', 'rt') as csvfile:

		# create csvfile
		rooms = csv.reader(csvfile)

		# iterate over rows
		for row in rooms:

			# extract text out of list
			for text in row:

				# split features
				features = text.split(";")

				# initialize features for class
				name = features[0]
				capacity = features[1]

				# initilaze room using the class
				room = Room(name, capacity)

				# add room to list
				chambers.append(room)

	# print(chambers)

	#* substract course information *#

	# create list for courses
	allcourses = []

	# load courses as classes in allcourses-list
	with open('../data/vakken.csv', 'rt') as coursefile:
		courses = csv.reader(coursefile)
		for row in courses:
			for text in row:
				courseInfo = text.split(";")

				# add course name
				courseName = courseInfo[0]

				# add amount of lectures
				courseLectures = courseInfo[1]

				# add amount of seminars
				courseSeminars = courseInfo[2]

				# add max amount seminars
				courseMaxSem = courseInfo[3]
				if courseMaxSem == "nvt":
					courseMaxSem = 0

				# add amount of practicals
				coursePracticals = courseInfo[4]

				# add max amount practicals
				courseMaxPrac = courseInfo[5]
				if courseMaxPrac == "nvt":
					courseMaxPrac = 0

				# add course to list
				allcourses.append(Course(courseName, courseLectures, courseSeminars, courseMaxSem, coursePracticals, courseMaxPrac))

	# import student classes
	student_list = createStudentClass()


	# create empty dictionary with all room-timelock combinations (roomlocks) as keys
	roomlocks = list(range(0, 140))
	schedule = dict.fromkeys(roomlocks)
		#* prepare dict that represents schedule *#

	return chambers, allcourses, student_list, schedule


def translateRoomlock(roomlock):
	""" Translates roomlock number into roomnumber and timelock """

	# amount of rooms per timelock
	total_amount_rooms = 7

	# determine the room 
	room = roomlock % total_amount_rooms

	# determine timelock
	timelock = int(roomlock / total_amount_rooms)


	return room, timelock


def scheduleClass(course, typeClass, schedule):
	"""" Schedules """

	# group activities by type
	if typeClass == "lecture":
		activity = course.lectures
	elif typeClass == "seminar":
		activity = course.seminars
	elif typeClass == "practical":
		activity = course.practicals

	# intiliaze counter to keep track of tempts to schedule lecture
	counter = 0

	# untill no activities are left
	while activity > 0:

		# choose random roomlock
		pickroomlock = random.randint(0, 139)

		# until an unoccupied roomlock is found
		while schedule[pickroomlock] is not None:

			# pick new random roomlock 
			pickroomlock = random.randint(0, 139)

		# if room is free, substract the room and timelock
		room, timelock = translateRoomlock(pickroomlock)

		# print("free roomlock chosen")
		# print(room, timelock)
		# for lectures 
		# if typeClass == "lecture":

		# 	# until an unoccupied roomlock is found with enough capacity (with a max of 20 times)
		# 	while (course.students > int(chambers[room].capacity)) or (schedule[pickroomlock] is not None):

		# 		# pick new random roomlock
		# 		pickroomlock = random.randint(0, 139)

		# 		# increase counter with every tempt 
		# 		counter += 1

		# 		# substract room and timelock 
		# 		room, timelock = translateRoomlock(pickroomlock)

		# 		# print(room,  timelock)
		# 		print(counter)
		# 		print("lectures stuck")

		# 		# start over if too many temps are being done
		# 		if counter > 50:
		# 			return 1 

		# # same for seminars and practicals
		# elif typeClass == "seminar":
		# 	while course.maxstudentssem > int(chambers[room].capacity) or schedule[pickroomlock] is not None:
		# 		pickroomlock = random.randint(0, 139)
		# 		room, timelock = translateRoomlock(pickroomlock)
		# 		print("stuck with seminars")

		# elif typeClass == "practical":
		# 	while course.maxstudentsprac > int(chambers[room].capacity) or schedule[pickroomlock] is not None:
		# 		pickroomlock = random.randint(0, 139)
		# 		room, timelock = translateRoomlock(pickroomlock)
		# 		print("stuck with practica")

		# add activity to schedule at roomlock
		schedule[pickroomlock] = course.name + " " + typeClass

		#* determine group number *#

		# lecture has only 1 group
		if typeClass == "lecture":
			group = 0

		# seminars and practicals > 1 group, 
		else:

			# activity number decreases as we schedule it, which gives different group number 
			group = activity

		# update course class with new activity
		course.updateSchedule(pickroomlock, (course.name + " " + typeClass), group)

		# update room class with new activity
		room, timelock = translateRoomlock(pickroomlock)
		chambers[room].add_booking(timelock)

		# update student class with new activity
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

		# decrease activity counter
		activity -= 1


	return 

def complementCourse():
	#* add studentnames, amount of seminars and practicals to course class *#


	# another counter for check
	amount_of_tries = 0

	# for each course
	for course in allcourses:

		# check all students
		for student in student_list:

			# if student is attenting course
			if course.name in student.courses:

				# add student to course class
				course.addStudent(student.last_name)

		# if course has seminars
		if course.seminars > 0:

			# count and add amount to course class
			numofseminars = math.ceil(course.students/course.maxstudentssem)
			course.addSeminar(numofseminars)

		# if course has practicals
		if course.practicals > 0:

			# count and add to course class
			numofpracticals = math.ceil(course.students/course.maxstudentsprac)
			course.addPractical(numofpracticals)


		#* divide students over groups *#

		# start with group '1'
		sem = 1

		# if course has seminars
		if course.seminars > 0:

			# iterate over students in course with steps of max amount of students
			for i in range(0, len(course.studentnames), course.maxstudentssem):

				# create list with names of students 
				studentlist = course.studentnames[i: i + course.maxstudentssem]

				# add studentlist to course class
				course.createSeminarGroup(sem, studentlist)
	
				# go on to the next group
				sem += 1

		# same for practical
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
	
		# increase counter
		amount_of_tries += 1
		# print(amount_of_tries)
		# print(allcourses[1].studentnames)

		# print(schedule) # heel schedule
		# print(student_list[0].schedule)
		# print(allcourses[4].activities)
		# print(chambers)
	

	return
		# print(allcourses[4].practicalgroups[3])
		# print(allcourses[4].practicals)
		# print(student_list[511].schedule)

		# print(allcourses[5].seminargroups[0]) # activiteiten van vak
		# # print(chambers[1].booking) # bookings van een zaal
		# print(allcourses[5].studentnames)

## calculate profiler time
# pr = cProfile.Profile()
# pr.enable()

chambers, allcourses, student_list, schedule = prepareData()
complementCourse()

# pr.disable()
# pr.print_stats(sort='time')


