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


def simulatedAnnealing(coolingscheme, min_iterations, chambers, allcourses, student_list, schedule):
	""" Searches for the optimal score by using a coolingscheme """

	# placeholders
	best_score = None
	best_course = None
	best_student_list = None
	best_chambers = None

	# initialize temperatures
	temp_start = 100000
	temp_final = 1

	# array for scores for visualization
	scores = []

	# set start temperature 
	temperature = temp_start

	# loop until system has cooled
	for i in range(min_iterations):

		# calculate score schedule
		points = calcScore(allcourses, student_list, chambers)

		print("Before swap: ", points)

		# append score to list for visualisation
		scores.append(points)

		# keep track of the best score and its variables
		if best_score == None or points > best_score: 
			best_score = points
			best_courses = allcourses
			best_student_list = student_list
			best_chambers = chambers

		# pick random neighbour by swapping 
		course1, activity1, course2, activity2, schedule = swapCourse(chambers, allcourses, student_list, schedule)

		# calculate new score
		newpoints = calcScore(allcourses, student_list, chambers)
		
		print("   New score: ", newpoints)

		# if new score is worst 
		if newpoints < points:

			# calculate acceptance chance
			acceptance_probability = math.exp((newpoints - points) / temperature)

			# if acceptance chance higher than random number
			if (acceptance_probability > random.random()):
			
				# accept the worst solution
				print("Accepted worst solution, score:", newpoints)
				points = newpoints

				# cool system
				temperature = coolingscheme(temperature, min_iterations, i)

			# if acceptance chance lower than random number
			else:

				# swap back
				swapCourse(chambers, allcourses, student_list, schedule, course1, activity1, course2, activity2)

				# calculate new score and print
				newpoints = calcScore(allcourses, student_list, chambers)

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
			points = newpoints 
			print("accepted score:" )


	print("bestscore:", best_score)


	return best_score, best_courses, best_student_list, best_chambers, scores