from __future__ import division
import csv
import random
import math
import generateschedule
import scorefunction
import hillclimber
# import SA
from parse import createStudentClass, parse, gimme_students
from classes import Students, Room, Course
from generateschedule import createSchedule, updateClassesFromSchedule
from scorefunction import calcScore
from hillclimber import hillclimbRoomlocks
from hillclimberstudents import hillclimbStudent
from SA import simulatedAnnealing
from coolingschemes import linear, exponential, sigmoidal, geman, lin_exp
from printschedule import print_schedule
from plot import multiple_simulated_annealing



# # input = [[[scores], type], [[scores], type], [[scores], type] [[scores], type]]
# input = []

# # perform geman
# chambers, allcourses, student_list, schedule = createSchedule()
# best_score, best_courses, best_student_list, best_chambers, scores_geman = simulatedAnnealing(geman, 10, chambers, allcourses, student_list, schedule)
# # plot_simulated_annealing(scores, geman, best_score)

# input.append(scores_geman)

# chambers, allcourses, student_list, schedule = createSchedule()
# best_score, best_courses, best_student_list, best_chambers, scores_linear = simulatedAnnealing(linear, 10, chambers, allcourses, student_list, schedule)
# # plot_simulated_annealing(scores, linear, best_score)

# input.append(scores_linear)
# chambers, allcourses, student_list, schedule = createSchedule()
# best_score, best_courses, best_student_list, best_chambers, scores_sigmoidal = simulatedAnnealing(sigmoidal, 10, chambers, allcourses, student_list, schedule)

# input.append(scores_sigmoidal)

# chambers, allcourses, student_list, schedule = createSchedule()
# best_score, best_courses, best_student_list, best_chambers, scores_exponential = simulatedAnnealing(exponential, 10, chambers, allcourses, student_list, schedule)

# input.append(scores_exponential)

# multiple_simulated_annealing(input)


def averaging(coolingscheme, iterations_in_algorithm, amount):
	""" Takes the average of """ 
	
	total_score = []

	# for amount of times
	for i in range(amount):
		print(i)


		# create random schedule
		chambers, allcourses, student_list, schedule = createSchedule()

		# perform algorithm
		best_score, best_courses, best_student_list, best_chambers, scores_geman = simulatedAnnealing(coolingscheme, iterations_in_algorithm, chambers, allcourses, student_list, schedule)
		# plot_simulated_annealing(scores, geman, best_score)

		# add scores to total score array
		total_score.append(scores_geman)
		# print(i, score[i])
	print(total_score)

	average_array= []
	new_score = 0
	print(total_score[0][0])
	print(total_score[1][0])

	for i in range(amount):
		for j in range(iterations_in_algorithm):
			new_score += total_score[j][i] 
			print("hoi")
			print(new_score)
			# total_score[i] 
		
		# for j in scores_geman: 
			# print(total_score[i][j])
			# print(new_score)

		# average_array.append(new_score / len(scores_geman)


averaging(geman, 14, 10)




