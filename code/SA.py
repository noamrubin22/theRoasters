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

def simulatedAnnealing(temperature, cooling_rate, chambers, allcourses, student_list, schedule):
	""" Searches for the optimal score by using a coolingscheme """

	# intialize best_score counter
	best_score = 0

	# create array for scores (visualization)
	scores = []

	# loop until system has cooled
	while temperature > 1:

		# calculate score before swap
		points = calcScore(allcourses, student_list, chambers)

		print("Before swap: ", points)

		# append score to list (visualisation)
		scores.append(points)

		# keep track of the best score and its variables
		if points > best_score: 
			best_score = points
			best_courses = allcourses
			best_student_list = student_list
			best_chambers = chambers

		# pick random neighbour by swapping 
		course1, activity1, course2, activity2 = swapCourse(chambers, allcourses, student_list, schedule)

		# calculate new score
		newpoints = calcScore(allcourses, student_list, chambers)
		
		print("   New score: ", newpoints)

		# keep track of best score and variables
		if newpoints > best_score:
			best_score = newpoints
			best_courses = allcourses
			best_student_list = student_list
			best_chambers = chambers

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
				temperature *= 1 - cooling_rate

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

			# accept
			points = newpoints 


	print("bestscore:", best_score)
	# print(scores)

	return best_score, best_courses, best_student_list, best_chambers, scores


# create schedule
chambers, allcourses, student_list, schedule = createSchedule()
simulatedAnnealing(1000, 0.002, chambers, allcourses, student_list, schedule)

