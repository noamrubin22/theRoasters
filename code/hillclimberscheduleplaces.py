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

	# print(roomlock1, roomlock2)
	# print(schedule[roomlock1], schedule[roomlock2])

	# store random activities
	activity1 = schedule[roomlock1]
	activity2 = schedule[roomlock2]


	# switch courses in schedule
	schedule[roomlock1] = activity2
	schedule[roomlock2] = activity1

	allcourses, student_list, chambers = updateClassesFromSchedule(schedule)


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
		print("Roomlocks switched: ", roomlock1, roomlock2)

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

# chambers, allcourses, student_list, schedule = createSchedule()
# hillclimbRoomlocks2(1000, chambers, allcourses, student_list, schedule)
