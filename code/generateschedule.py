##################################################### 
# Heuristieken: Lectures & Lesroosters			  	#
#												  	#
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  	#
# 		 & Noam Rubin							  	#
#												  	#
# This code consists of function that are needed to	#
# generate an empty schedule and complement it   	#
# with courses, students and rooms.   				#
# 												  	#
#####################################################

import random
import math
from classes import Students, Room, Course
from parse import *

def createRooms():
	""" Creates lists for rooms """

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

	return chambers

def createCourses():
	""" Substracts course information and put into list """

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

	return allcourses

def createStudents():
	""" Creates a list with students """

	# create empty list
	student_list = []

	# import student classes
	student_list = createStudentClass()

	return student_list

def createEmptySchedule():
	""" Prepare dictionary that represents schedule """

	# create empty dictionary with all room-timelock combinations (roomlocks) as keys
	roomlocks = list(range(0, 140))
	schedule = dict.fromkeys(roomlocks)

	return schedule

def createStudentGroups(allcourses, student_list):
	"""" Divides students into practical and seminar groups """

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


	return allcourses, student_list

def translateRoomlock(roomlock):
	""" Translates roomlock number into roomnumber and timelock """

	# amount of rooms per timelock
	total_amount_rooms = 7

	# determine the room
	room = roomlock % total_amount_rooms

	# determine timelock
	timelock = int(roomlock / total_amount_rooms)


	return room, timelock


def scheduleClass(course, typeClass, schedule, chambers, student_list):
	"""" Schedules """

	# group activities by type
	if typeClass == "lecture":
		activity = course.lectures
	elif typeClass == "seminar":
		activity = course.seminars
	elif typeClass == "practical":
		activity = course.practicals

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

def complementCourse(allcourses, schedule, chambers, student_list):
	""" Schedules activities for each course into schedule """

	# for each course
	for course in allcourses:

		# schedule activities 
		scheduleClass(course, "lecture", schedule, chambers, student_list)
		scheduleClass(course, "seminar", schedule, chambers, student_list)
		scheduleClass(course, "practical", schedule, chambers, student_list)

	return allcourses, schedule, chambers, student_list

def createSchedule():
	chambers = createRooms()
	allcourses = createCourses()
	student_list = createStudents()
	schedule = createEmptySchedule()
	allcourses, student_list = createStudentGroups(allcourses, student_list)
	complementCourse(allcourses, schedule, chambers, student_list)
	return chambers, allcourses, student_list, schedule

