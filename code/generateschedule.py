#####################################################
# Heuristieken: Lectures & Lesroosters			  	#
#												  	#
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  	#
# 		 & Noam Rubin							  	#
#												  	#
# This code consists of functions that are needed   #
# to generate an empty schedule and complement it   #
# with courses, students and rooms.   				#
# 												  	#
#####################################################

import random
import math
import re
from classes import Students, Room, Course
from parse import *

def create_rooms():
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


def create_courses():
	""" Substracts course information and puts into list """

	# create list for courses
	allcourses = []

	# load courses as classes in allcourses-list
	with open('../data/vakken.csv', 'rt') as coursefile:

		# clean text
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

def create_students():
	""" Creates a list with students """

	# create empty list
	student_list = []

	# import student classes
	student_list = create_student_class()

	return student_list

def create_empty_schedule():
	""" Prepare dictionary that represents schedule """

	# create empty dictionary with all room-timelock combinations (roomlocks) as keys
	roomlocks = list(range(0, 140))
	schedule = dict.fromkeys(roomlocks)

	return schedule

def create_student_groups(allcourses, student_list):
	"""" Divides students into practical and seminar groups """

	# for each course
	for course in allcourses:

		# check all students
		for student in student_list:

			# if student is attenting course
			if course.name in student.courses:

				# add student to course class
				course.add_student(student.last_name)

		# if course has seminars
		if course.seminars > 0:

			# count and add amount to course class
			numofseminars = math.ceil(course.students/course.maxstudentssem)
			course.add_seminar(numofseminars)

		# if course has practicals
		if course.practicals > 0:

			# count and add to course class
			numofpracticals = math.ceil(course.students/course.maxstudentsprac)
			course.add_practical(numofpracticals)


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
				course.create_seminar_group(sem, studentlist)

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

def translate_roomlock(roomlock):
	""" Translates roomlock number into roomnumber and timelock """

	# amount of rooms per timelock
	total_amount_rooms = 7

	# determine the room
	room = roomlock % total_amount_rooms

	# determine timelock
	timelock = int(roomlock / total_amount_rooms)

	return room, timelock


def schedule_class(course, type_class, schedule, chambers, student_list):
	"""" Schedules activities of a course """

	# group activities by type
	if type_class == "lecture":
		activity = course.lectures
	elif type_class == "seminar":
		activity = course.seminars
	elif type_class == "practical":
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
		schedule[pickroomlock] = course.name + " " + type_class + " " + str(activity)

		#* determine group number *#

		# lecture has only 1 group
		if type_class == "lecture":
			group = 0

		# seminars and practicals > 1 group,
		else:

			# activity number decreases as we schedule it, which gives different group number
			group = activity

		# update course class with new activity
		course.update_schedule(pickroomlock, (course.name + " " + type_class), group)

		# update room class with new activity
		room, timelock = translate_roomlock(pickroomlock)
		chambers[room].add_booking(timelock)

		# update student class with new activity
		if type_class == "lecture":
			for student in student_list:
				if course.name in student.courses:
					student.update_student_schedule(timelock, course.name)

		if type_class == "seminar":
			for student in student_list:
				if course.name in student.courses:
					if student.last_name in course.seminargroups[activity]:
						student.update_student_schedule(timelock, course.name)

		if type_class == "practical":
			for student in student_list:
				if course.name in student.courses:
					if student.last_name in course.practicalgroups[activity]:
						student.update_student_schedule(timelock, course.name)

		# decrease activity counter
		activity -= 1

	return

def complement_course(allcourses, schedule, chambers, student_list):
	""" Schedules activities for each course into schedule """

	# for each course
	for course in allcourses:

		# schedule activities
		schedule_class(course, "lecture", schedule, chambers, student_list)
		schedule_class(course, "seminar", schedule, chambers, student_list)
		schedule_class(course, "practical", schedule, chambers, student_list)

	return allcourses, schedule, chambers, student_list

def create_schedule():
	""" Creates a schedule """

	# creates list available rooms
	chambers = create_rooms()

	# creates list of all courses
	allcourses = create_courses()

	# creates student_list
	student_list = create_students()

	# create empty schedule with roomlocks as keys
	schedule = create_empty_schedule()

	# divide students over courses-groups
	allcourses, student_list = create_student_groups(allcourses, student_list)

	# complement schedule with activities from courses
	complement_course(allcourses, schedule, chambers, student_list)

	return chambers, allcourses, student_list, schedule

def update_classes_from_schedule(schedule):
	""" Updates classes from new schedule """ 

	# load all student, courses and room -information into variables
	allcourses = create_courses()
	chambers = create_rooms()
	student_list = create_students()

	# create student groups
	allcourses, student_list = create_student_groups(allcourses, student_list)

	# for each activity in new schedule
	for roomlock, activity in schedule.items():

		# if it's not an empty roomlock
		if activity is not None:

			# if lecture
			if "lecture" in activity:

				# split text 
				splittext = activity.split(" lecture ")

				# assign class
				type_class = "lecture"

				# split text and determine group
				coursename = splittext[0]
				group = 0

			# same for seminar
			if "seminar" in activity:
				splittext = activity.split(" seminar ")
				type_class = "seminar"
				coursename = splittext[0]
				group = int(float(splittext[1]))

			# and practical
			if "practical" in activity:
				splittext = activity.split(" practical ")
				type_class = "practical"
				coursename = splittext[0]
				group = int(float(splittext[1]))

			# for each course in course-list
			for course in allcourses:

				# find adjusted course
				if coursename == course.name:

				# update course class with new activity
					course.update_schedule(roomlock, (coursename + " " + type_class), group)

					# update room class with new activity
					room, timelock = translate_roomlock(roomlock)
					chambers[room].add_booking(timelock)

					# update student class with new activity
					if type_class == "lecture":
						for student in student_list:
							if course.name in student.courses:
								student.update_student_schedule(timelock, course.name)

					if type_class == "seminar":
						for student in student_list:
							if course.name in student.courses:
								if student.last_name in course.seminargroups[group]:
									student.updat_student_schedule(timelock, course.name)

					if type_class == "practical":
						for student in student_list:
							if course.name in student.courses:
								if student.last_name in course.practicalgroups[group]:
									student.updat_student_schedule(timelock, course.name)

	return allcourses, student_list, chambers
