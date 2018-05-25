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
# two random courses								#
#												  	#
#####################################################

import scorefunction
import random
import csv
import generateschedule
from generateschedule import translateRoomlock, createSchedule, updateClassesFromSchedule
from scorefunction import calcScore


def swapCourse2(chambers, allcourses, student_list, schedule, roomlock1 = None, roomlock2 = None):
	""" Swaps roomlocks of 2 (random) courses """

	#* swap roomlock 2 (random) courses *#

	# if specific activity is not chosen
	if roomlock1 == None:
		# chose random activity from schedule
			roomlock1 = random.randint(0, len(schedule) - 1)

	# same
	if roomlock2 == None:
			roomlock2 = random.randint(0, len(schedule) - 1)

	while True:
		# store random activities
		activity1 = schedule[roomlock1]
		activity2 = schedule[roomlock2]

		# determine coursename of swapped course
		if activity1 == None:
			coursename1 = "None"

		else:
			splittext = activity1.split(" lecture | seminar | practical ")
			coursename1 = splittext[0]

		if activity2 == None:
			coursename2 = "None"

		else:
			splittext = activity2.split(" lecture | seminar | practical ")
			coursename2 = splittext[0]

		if activity1 != activity2:
			break

		roomlock1 = random.randint(0, len(schedule) - 1)
		roomlock2 = random.randint(0, len(schedule) - 1)


	# elif "lecture" in activity1:
	# 	splittext = activity1.split(" lecture ")
	# 	coursename1 = splittext[0]

	# elif "seminar" in activity1:
	# 	splittext = activity1.split(" seminar ")
	# 	coursename1 = splittext[0]

	# elif "practical" in activity1:
	# 	splittext = activity1.split(" practical ")
	# 	coursename1 = splittext[0]

	# if activity2 == None:
	# 	coursename2 = "None"

	# elif "lecture" in activity2:
	# 	splittext = activity2.split(" lecture ")
	# 	coursename2 = splittext[0]

	# elif "seminar" in activity2:
	# 	splittext = activity2.split(" seminar ")
	# 	coursename2 = splittext[0]

	# elif "practical" in activity2:
	# 	splittext = activity2.split(" practical ")
	# 	coursename2 = splittext[0]




	# switch courses in schedule
	schedule[roomlock1] = activity2
	schedule[roomlock2] = activity1

	allcourses1, student_list, chambers = updateClassesFromSchedule(schedule)



	count_course1_numbers = 0
	count_course2_numbers = 0
	for course in allcourses:
		
		if course.name == coursename1:
			course1 = count_course1_numbers
			count_activities_course = 0
			for activity in course.activities:
				if roomlock1 == activity[0]:
					activityswapped1 = count_activities_course
					allcourses[course1].changeSchedule(roomlock2, activityswapped1)
				count_activities_course += 1
		count_course1_numbers += 1

		if course.name == coursename2:
			course2 = count_course2_numbers
			count_activities_course = 0
			for activity in course.activities:
				if roomlock2 == activity[0]:
					activityswapped2 = count_activities_course
					allcourses[course2].changeSchedule(roomlock1, activityswapped2)
				count_activities_course += 1
		count_course2_numbers += 1

	print(activity1, activity2)







	# swap the chosen activities from roomlock in schedule
	# allcourses[course1].changeSchedule(roomlock2, activity1)
	# allcourses[course2].changeSchedule(roomlock1, activity2)

	# return chambers, allcourses, student_list, schedule

	return roomlock1, roomlock2, chambers, allcourses, student_list, schedule


def hillclimbRoomlocks2(times, chambers, allcourses, student_list, schedule):
	""" Searches for the optimal score by swapping roomlocks """

	# amount of steps hillclimber
	for i in range(0, times):

		# calculate score before swap
		points = calcScore(allcourses, student_list, chambers)
		print("Before swap: ", points)

		# perform swap
		roomlock1, roomlock2, chambers, allcourses, student_list, schedule = swapCourse2(chambers, allcourses, student_list, schedule)
		# print("Roomlocks switched: ", roomlock1, roomlock2)

		# calculate new scores
		newpoints = calcScore(allcourses, student_list, chambers)
		print("   After swap: ", newpoints)

		# if new score lower than old score
		if newpoints < points:

			# swap back
			roomlock1, roomlock2, chambers, allcourses, student_list, schedule = swapCourse2(chambers, allcourses, student_list, schedule, roomlock2, roomlock1)

			# calculate new score
			newpoints = calcScore(allcourses, student_list, chambers)
			print("      Back to normal: ", newpoints)

			# if back-swap didn't go well
			if points != newpoints:

				# print courses and break loop
				print(roomlock2, roomlock1)
				print("ERROR")
				break

	# return newpoints

chambers, allcourses, student_list, schedule = createSchedule()
hillclimbRoomlocks2(1000, chambers, allcourses, student_list, schedule)
