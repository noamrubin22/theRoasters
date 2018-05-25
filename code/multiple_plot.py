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
from plot import multiple_simulated_annealing, plot_hillclimber


# averaging(geman, 14, 10)
def plot_average_hillclimb(repetitions, runs):
	totalscores = []
	for i in range(repetitions):
		algorithm_scores = []
		chambers, allcourses, student_list, schedule = createSchedule()
		for i in range(runs):
			score = hillclimbRoomlocks(1, chambers, allcourses, student_list, schedule)
			algorithm_scores.append(score)
		totalscores.append(algorithm_scores)

	sorted_scores = []
	for i in range(runs):
		selected_score = []
		for j in range(repetitions):
			selected_score.append(totalscores[j][i])
		sorted_scores.append(selected_score)

	average_scores = []
	for scores in sorted_scores:
		average_scores.append(sum(scores)/len(scores))

	plot_hillclimber(average_scores)

# plot_average_hillclimb(10, 100)

def plot_average_SA(repetitions, runs):
	totalscores = []
	for i in range(repetitions):
		algorithm_scores = []
		chambers, allcourses, student_list, schedule = createSchedule()
		best_score, best_courses, best_student_list, best_chambers, geman_scores = simulatedAnnealing(geman, runs, chambers, allcourses, student_list, schedule)
		chambers, allcourses, student_list, schedule = createSchedule()
		best_score, best_courses, best_student_list, best_chambers, linear_scores = simulatedAnnealing(linear, runs, chambers, allcourses, student_list, schedule)
		chambers, allcourses, student_list, schedule = createSchedule()
		best_score, best_courses, best_student_list, best_chambers, sigmoidal_scores = simulatedAnnealing(sigmoidal, runs, chambers, allcourses, student_list, schedule)
		chambers, allcourses, student_list, schedule = createSchedule()
		best_score, best_courses, best_student_list, best_chambers, exponential_scores = simulatedAnnealing(exponential, runs, chambers, allcourses, student_list, schedule)
		algorithm_scores.append([geman_scores, linear_scores, sigmoidal_scores, exponential_scores])
		totalscores.append(algorithm_scores)

	print(totalscores)

	all_geman_scores = []
	all_linear_scores = []
	all_sigmoidal_scores = []
	all_exponential_scores = []

	for i in range(repetitions):
		all_geman_scores.append(totalscores[i][0][0])
		all_linear_scores.append(totalscores[i][0][1])
		all_sigmoidal_scores.append(totalscores[i][0][2])
		all_exponential_scores.append(totalscores[i][0][3])

	geman_sorted_scores = []
	linear_sorted_scores = []
	sigmoidal_sorted_scores = []
	exponential_sorted_scores = []
	for i in range(runs):
		geman_selected_score = []
		linear_selected_score = []
		sigmoidal_selected_score = []
		exponential_selected_score = []
		for j in range(repetitions):
			geman_selected_score.append(all_geman_scores[j][i])
			linear_selected_score.append(all_linear_scores[j][i])
			sigmoidal_selected_score.append(all_sigmoidal_scores[j][i])
			exponential_selected_score.append(all_exponential_scores[j][i])
		geman_sorted_scores.append(geman_selected_score)
		linear_sorted_scores.append(linear_selected_score)
		sigmoidal_sorted_scores.append(sigmoidal_selected_score)
		exponential_sorted_scores.append(exponential_selected_score)

	geman_average_scores = []
	for scores in geman_sorted_scores:
		geman_average_scores.append(sum(scores)/len(scores))

	linear_average_scores = []
	for scores in linear_sorted_scores:
		linear_average_scores.append(sum(scores)/len(scores))

	sigmoidal_average_scores = []
	for scores in sigmoidal_sorted_scores:
		sigmoidal_average_scores.append(sum(scores)/len(scores))

	exponential_average_scores = []
	for scores in exponential_sorted_scores:
		exponential_average_scores.append(sum(scores)/len(scores))

	average_scores = [geman_average_scores, linear_average_scores, sigmoidal_average_scores, exponential_average_scores]

	multiple_simulated_annealing(average_scores)

plot_average_SA(10, 3000)

