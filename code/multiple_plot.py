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



# input = [[[scores], type], [[scores], type], [[scores], type] [[scores], type]]
input = []

# perform geman
chambers, allcourses, student_list, schedule = createSchedule()
best_score, best_courses, best_student_list, best_chambers, scores_geman = simulatedAnnealing(geman, 10000, chambers, allcourses, student_list, schedule)
# plot_simulated_annealing(scores, geman, best_score)

input.append(scores_geman)

chambers, allcourses, student_list, schedule = createSchedule()
best_score, best_courses, best_student_list, best_chambers, scores_linear = simulatedAnnealing(linear, 10000, chambers, allcourses, student_list, schedule)
# plot_simulated_annealing(scores, linear, best_score)

input.append(scores_linear)
chambers, allcourses, student_list, schedule = createSchedule()
best_score, best_courses, best_student_list, best_chambers, scores_sigmoidal = simulatedAnnealing(sigmoidal, 10000, chambers, allcourses, student_list, schedule)

input.append(scores_sigmoidal)

chambers, allcourses, student_list, schedule = createSchedule()
best_score, best_courses, best_student_list, best_chambers, scores_exponential = simulatedAnnealing(exponential, 10000, chambers, allcourses, student_list, schedule)

input.append(scores_exponential)

multiple_simulated_annealing(input)

def average(coolingscheme, iterations_in_algorithm, amount):
	""" Takes the average of """ 
 	
 	d = {}

	for i in range(amount):
		d["score{0}".format(i)] = []
		
		chambers, allcourses, student_list, schedule = createSchedule()
		best_score, best_courses, best_student_list, best_chambers, scores_geman = simulatedAnnealing(geman, 10000, chambers, allcourses, student_list, schedule)
		# plot_simulated_annealing(scores, geman, best_score)

		scores[i].append(scores_geman)

	


