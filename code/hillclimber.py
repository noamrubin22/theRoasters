#####################################################
# Heuristieken: Lectures & Lesroosters			  	#
#												  	#
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  	#
# 		 & Noam Rubin							  	#
#												  	#
# This code searchs for the optimal schedulescore 	#
# using a hillclimber algorithm where the only    	#
# swaps being accepted are the ones that increase 	#
# the score. The swaps are being made between	  	#
# two random courses.								#
#												  	#
#####################################################

import scorefunction
import random
import csv
import generateschedule
from generateschedule import translate_roomlock, update_classes_from_schedule
from scorefunction import calc_score


def swap_course(chambers, allcourses, student_list, schedule, course1 = None, activity1 = None, course2 = None, activity2 = None):
	""" Swaps roomlocks of 2 (random) courses """

	#* swap roomlock 2 (random) courses *#

	# if specific course is not chosen
	if course1 == None:
		
		# choose random course from courselist
		course1 = random.randint(0, len(allcourses) - 1)

	# same
	if course2 == None:
		course2 = random.randint(0, len(allcourses) - 1)

	# if specific activity is not chosen
	if activity1 == None:

		# choose random activity from course
		if len(allcourses[course1].activities) == 0:
			activity1 = 0
		else:
			activity1 = random.randint(0, len(allcourses[course1].activities) - 1)

	# same
	if activity2 == None:
		if len(allcourses[course2].activities) == 0:
			activity2 = 0
		else:
			activity2 = random.randint(0, len(allcourses[course2].activities) - 1)

	# store random activities
	randact1 = allcourses[course1].activities[activity1]
	randact2 = allcourses[course2].activities[activity2]

	# store roomlocks
	roomlock1 = randact1[0]
	roomlock2 = randact2[0]

	# swap the chosen activities from roomlock in schedule
	allcourses[course1].change_schedule(roomlock2, activity1)
	allcourses[course2].change_schedule(roomlock1, activity2)

	# translate to room and timelock for both roomlocks
	room1, timelock1 = translate_roomlock(roomlock1)
	room2, timelock2 = translate_roomlock(roomlock2)

	# store activity-groups
	coursegroup1 = allcourses[course1].activities[activity1][2]
	coursegroup2 = allcourses[course2].activities[activity2][2]


	#* change schedule of individual students*#

	# if first coursegroup has only one group (lecture)
	if coursegroup1 == 0:

		# for each student
		for student in student_list:

			# that follows the course
			if allcourses[course1].name in student.courses:

				# change individual schedule
				student.change_student_schedule(timelock1, timelock2, allcourses[course1].name)

	# for seminars and practicals (group > 1)
	else:

		# for each student
		for student in student_list:

			# if student follows the course
			if allcourses[course1].name in student.courses:

				# if course has seminar
				if allcourses[course1].seminars > 0 and allcourses[course1].practicals == 0:

					# if student is in seminargroup
					if student.last_name in allcourses[course1].seminargroups[coursegroup1]:

							# change individual schedule with swapped course
							student.change_student_schedule(timelock1, timelock2, allcourses[course1].name)

				# if course has practical
				elif allcourses[course1].practicals > 0 and allcourses[course1].seminars == 0:

					# if student is in practical-group
					if student.last_name in allcourses[course1].practicalgroups[coursegroup1]:

						# change individual schedule
						student.change_student_schedule(timelock1, timelock2, allcourses[course1].name)

				# if student has both practicals and seminarsa
				elif allcourses[course1].seminars > 0 and allcourses[course1].practicals > 0:

					# if student is in practical- or seminargroup
					if student.last_name in allcourses[course1].seminargroups[coursegroup1] or student.last_name in allcourses[course1].practicalgroups[coursegroup1]:
						
						# change individual schedule
						student.change_student_schedule(timelock1, timelock2, allcourses[course1].name)

	# same for the second coursegroup
	if coursegroup2 == 0:
		for student in student_list:
			if allcourses[course2].name in student.courses:
				student.change_student_schedule(timelock2, timelock1, allcourses[course2].name)

	# for seminars and practicals
	else:
		for student in student_list:

				# if course has seminar
				if allcourses[course2].seminars > 0 and allcourses[course2].practicals == 0:
					if student.last_name in allcourses[course2].seminargroups[coursegroup2]:
							student.change_student_schedule(timelock2, timelock1, allcourses[course2].name)

				# if course has practical
				elif allcourses[course2].practicals > 0 and allcourses[course2].seminars == 0:
					if student.last_name in allcourses[course2].practicalgroups[coursegroup2]:
						student.change_student_schedule(timelock2, timelock1, allcourses[course2].name)

				# if student has both practicals and seminars
				elif allcourses[course2].seminars > 0 and allcourses[course2].practicals > 0:
					if student.last_name in allcourses[course2].seminargroups[coursegroup2] or student.last_name in allcourses[course2].practicalgroups[coursegroup2]:
						student.change_student_schedule(timelock2, timelock1, allcourses[course2].name)

	#* update roomschedules *#

	chambers[room1].change_booking(timelock1, timelock2)
	chambers[room2].change_booking(timelock2, timelock1)

	# save content of schedule at swapped roomlocks
	schedulecontent1 = schedule[roomlock1]
	schedulecontent2 = schedule[roomlock2]

	# switch courses in schedule
	schedule[roomlock1] = schedulecontent2
	schedule[roomlock2] = schedulecontent1

	return course1, activity1, course2, activity2, schedule


def hillclimb_roomlocks(times, chambers, allcourses, student_list, schedule):
	""" Searches for the optimal score by swapping roomlocks """

	# amount of steps hillclimber
	for i in range(0, times):

		# calculate score before swap
		points = calc_score(allcourses, student_list, chambers)

		# perform swap
		course1, activity1, course2, activity2, schedule = swap_course(chambers, allcourses, student_list, schedule)

		# calculate new scores
		newpoints = calc_score(allcourses, student_list, chambers)

		# if new score lower than old score
		if newpoints < points:

			# swap back
			swap_course(chambers, allcourses, student_list, schedule, course1, activity1, course2, activity2)

			# calculate new score
			newpoints = calc_score(allcourses, student_list, chambers)

			# if back-swap didn't go well
			if points != newpoints:

				# print courses and break loop
				print(course2, course1)
				print("ERROR")
				break

	return newpoints
