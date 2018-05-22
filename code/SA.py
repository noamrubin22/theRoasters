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

# import main
import scorefunction
import random
import hillclimberstudents
import csv
import math
# import generateschedule
# from generateschedule import translateRoomlock
from scorefunction import calcScore
from hillclimber import swapCourse

def simulatedAnnealing(temperature, cooling_rate, chambers, allcourses, student_list, schedule):
	""" Searches for the optimal score by using a coolingscheme """

	# loop until system has cooled
	while temperature > 1:

		# calculate score before swap
		points = calcScore(allcourses, student_list, chambers)
		# print("Before swap: ", points)

		# perform swap
		print(points)
		course1, activity1, course2, activity2 = swapCourse(chambers, allcourses, student_list, schedule)

		# calculate new score
		newpoints = calcScore(allcourses, student_list, chambers)
		# print("   New score: ", newpoints)

		# # keep track of best score
		# if (newpoints > best_score):
		# 	best_score = newpoints
		# 	print("SA:", best_score)
			
		# if new score is worst 
		if newpoints < points:

			# calculate acceptance probability
			acceptance_probability = math.exp((newpoints - points) / temperature)

			# if acceptance chance higher than random number
			if (acceptance_probability > random.random()):
			
				# accept the worst solution
				print("Accepted worst solution, score:", newpoints)

				# cool system
				temperature *= 1 - cooling_rate

			# if acceptance chance lower than random number
			else:

				# swap back
				swapCourse(chambers, allcourses, student_list, schedule, course1, activity1, course2, activity2)

				# calculate new score and print
				newpoints = calcScore(allcourses, student_list, chambers)
				# print("      Back to normal?: ", newpoints)

				# if back-swap didn't go well 
				if points != newpoints:

					# print coursenames and break loop
					print(course2, course1)
					print("ERROR")
					break
	return