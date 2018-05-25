#####################################################
# Heuristieken: Lectures & Lesroosters			  	#
#												  	#
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  	#
# 		 & Noam Rubin							  	#
#												  	#
# This code consists of classes that are needed for	#
# the storage of features of students, rooms and	#
# courses. 											#
#										  			#
#####################################################

import copy

class Students:
	""" Adds features to students """

	def __init__(self, last_name, first_name, student_ID, courses):
		self.last_name = last_name
		self.first_name = first_name
		self.student_ID = student_ID
		self.courses = courses
		self.schedule = []

	def add_course(self, course):
		""" Adds course to courselist """

		self.courses.append(self.course)


	def print_student(self):
		""" Prints studentname, ID and the courses that he/she follows """

		print("The name of the student is {} with student ID of {}, and takes the following courses: {}."
		.format(self.name, self.student_ID, self.courses))

	def update_student_schedule(self, timelock, course):
		""" Updates changes in schedule of student """

		self.schedule.append([timelock, course])

	def change_student_schedule(self, oldtimelock, newtimelock, course):
		""" Changes timelock in student's schedule """

		# for specific activity in schedule
		for activity in self.schedule:

			# exchange old roomlock with new
			if activity[0] == oldtimelock and activity[1] == course:
				activity[0] = newtimelock

				# exchange only one activity
				break

				
	# returns name and student- ID
	def __str__(self):
	    return "Name: %s %s, ID: %s" % (self.first_name, self.last_name, self.student_ID)


class Room:
	""" Adds features to room """

	def __init__(self, name, capacity):
		self.name = name
		self.capacity = capacity
		self.booking = []

	def add_booking(self, timelock):
		""" Occupies time lock """

		self.booking.append(timelock)

	def change_booking(self, oldtimelock, newtimelock):
		""" Updates/changes booking schedule """

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

	def add_student(self, name):
		""" Add student to course """

		self.students += 1
		self.studentnames.append(name)

	def add_seminar(self, num):
		""" Adds amount of seminars """

		self.seminars = num

	def add_practical(self, num):
		""" Adds amount of practicals """

		self.practicals = num

	def create_seminar_group(self, sem, studentlist):
		""" Creates a seminar group """

		self.seminargroups[sem] = studentlist

	def switch_seminar_student(self, sem1, sem2, student1, student2):
		""" Switches students between seminar-groups """

		student1name = self.seminargroups[sem1][student1]
		student2name = self.seminargroups[sem2][student2]

		self.seminargroups[sem1][student1] = student2name
		self.seminargroups[sem2][student2] = student1name

	def create_practical_group(self, prac, studentlist):
		""" Creates practical group """

		self.practicalgroups[prac] = studentlist

	def switch_practical_student(self, prac1, prac2, student1, student2):
		""" Switches students between practical-groups """

		student1name = self.practicalgroups[prac1][student1]
		student2name = self.practicalgroups[prac2][student2]

		self.practicalgroups[prac1][student1] = student2name
		self.practicalgroups[prac2][student2] = student1name

	def update_schedule(self, roomlock, activity, group):
		""" Adds activity with features to activity- list schedule  """

		self.activities.append([roomlock, activity, group])

	def change_schedule(self, newroomlock, schedulespot):
		""" Changes roomlock of activity """

		self.activities[schedulespot][0] = newroomlock

	# returns amount of lectures, seminars and pracitcals
	def __str__(self):
		return "Name: %s \nNumber of lectures: %s\nNumber of seminars: %s \nNumber of practicals: %s \n" % (self.name, self.lectures, self.seminars, self.practicals)
