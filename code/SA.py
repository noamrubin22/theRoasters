###################################################
# Heuristieken: Lectures & Lesroosters			  #
#												  #
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  #
# 		 & Noam Rubin							  #
#												  #
# This code searchs for the optimal schedulescore #
# using the simulated annealing algorithm whereby #
# a coolingscheme is used to accept swaps 		  #
#												  #
###################################################

import scorefunction
import random
import hillclimberstudents
import csv
import math
from scorefunction import calcScore
from hillclimber import swapCourse
from generateschedule import createSchedule


def simulated_annealing(coolingscheme, min_iterations, chambers, allcourses, student_list, schedule):
	""" Searches for the optimal score by using a coolingscheme """

	# placeholders
	best_score = None
	best_course = None
	best_student_list = None
	best_chambers = None

	# initialize temperatures
	temp_start = 10

	# array for scores (visualization)
	scores = []

	# set start temperature
	temperature = temp_start

	# loop until system has cooled
	for i in range(min_iterations):

		# calculate score schedule
<<<<<<< HEAD
		points = calcScore(allcourses, student_list, chambers)
=======
		points = calc_score(allcourses, student_list, chambers)
>>>>>>> 43617eef6741eaabc7c9e660abd76464970905ef

		# append score to list for visualisation
		scores.append(points)

		# keep track of the best score and its variables
		if best_score == None or points > best_score:
			best_score = points
			best_courses = allcourses
			best_student_list = student_list
			best_chambers = chambers
			best_schedule = schedule

<<<<<<< HEAD
		# pick random neighbour by swapping
		course1, activity1, course2, activity2, schedule = swapCourse(chambers, allcourses, student_list, schedule)

		# calculate new score
		newpoints = calcScore(allcourses, student_list, chambers)

		# if new score is worst
=======
		# pick random neighbour by swapping 
		course1, activity1, course2, activity2, schedule = swap_course(chambers, allcourses, student_list, schedule)

		# calculate new score
		newpoints = calc_score(allcourses, student_list, chambers)
		
		# if new score is worst 
>>>>>>> 43617eef6741eaabc7c9e660abd76464970905ef
		if newpoints < points:

			# calculate acceptance chance
			acceptance_probability = math.exp((newpoints - points) /temperature)

			# if acceptance chance higher than random number
			if (acceptance_probability > random.random()):

				# accept the worst solution
				points = newpoints

				# cool system
				temperature = coolingscheme(min_iterations, i)

			# if acceptance chance lower than random number
			else:

				# swap back
				swap_course(chambers, allcourses, student_list, schedule, course1, activity1, course2, activity2)

				# calculate new score and print
				newpoints = calc_score(allcourses, student_list, chambers)

				# if back-swap didn't go well
				if points != newpoints:

					# print coursenames and break loop
					print(course2, course1)
					print("ERROR")
					break

				# continue with previous score
				points = newpoints

		# if new score is better
		else:

			# accept it
<<<<<<< HEAD
			points = newpoints
=======
			points = newpoints 
>>>>>>> 43617eef6741eaabc7c9e660abd76464970905ef

	return best_score, best_courses, best_student_list, best_chambers, best_schedule, scores
