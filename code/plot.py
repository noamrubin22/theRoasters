import csv
import random
import math
from classes import Students, Room, Course
from helpers import *
from algorithms import *
import matplotlib.pyplot as plt



def plot_average_SA(repetitions, runs):
	""" Performs all cooling schemes of simulated annealing a certain number of times (repetitions) and
	plots the average scores """

	totalscores = []

	# for each repetition
	for i in range(repetitions):

		# create empty list
		algorithm_scores = []
		
		# create random schedule and perform simulated annealing with geman coolingscheme
		chambers, allcourses, student_list, schedule = create_schedule()
		best_schedule, best_score, best_courses, best_student_list, best_chambers, geman_scores = simulated_annealing(geman, runs, chambers, allcourses, student_list, schedule)
		
		# create random schedule and perform simulated annealing with linear coolingscheme
		chambers, allcourses, student_list, schedule = create_schedule()
		best_schedule, best_score, best_courses, best_student_list, best_chambers, linear_scores = simulated_annealing(linear, runs, chambers, allcourses, student_list, schedule)
		
		# create random schedule and perform simulated annealing with sigmoidal coolingscheme
		chambers, allcourses, student_list, schedule = create_schedule()
		best_schedule, best_score, best_courses, best_student_list, best_chambers, sigmoidal_scores = simulated_annealing(sigmoidal, runs, chambers, allcourses, student_list, schedule)
		
		# create random schedule and perform simulated annealing with exponential coolingscheme
		chambers, allcourses, student_list, schedule = create_schedule()
		best_schedule, best_score, best_courses, best_student_list, best_chambers, exponential_scores = simulated_annealing(exponential, runs, chambers, allcourses, student_list, schedule)
		
		# add scores to alogrithm list
		algorithm_scores.append([geman_scores, linear_scores, sigmoidal_scores, exponential_scores])
		
		# add algorithm list to totalscore
		totalscores.append(algorithm_scores)

	# create empty lists for score per coolingscheme
	all_geman_scores = []
	all_linear_scores = []
	all_sigmoidal_scores = []
	all_exponential_scores = []

	# add single scores coolingschem into lists with all scores
	for i in range(repetitions):
		all_geman_scores.append(totalscores[i][0][0])
		all_linear_scores.append(totalscores[i][0][1])
		all_sigmoidal_scores.append(totalscores[i][0][2])
		all_exponential_scores.append(totalscores[i][0][3])

	# create empty lists for sorted scores
	geman_sorted_scores = []
	linear_sorted_scores = []
	sigmoidal_sorted_scores = []
	exponential_sorted_scores = []

	# for each run
	for i in range(runs):

		# create empty lists for selected scores
		geman_selected_score = []
		linear_selected_score = []
		sigmoidal_selected_score = []
		exponential_selected_score = []

		# for each repetition
		for j in range(repetitions):

			# add selected score to all score list of coolingscheme
			geman_selected_score.append(all_geman_scores[j][i])
			linear_selected_score.append(all_linear_scores[j][i])
			sigmoidal_selected_score.append(all_sigmoidal_scores[j][i])
			exponential_selected_score.append(all_exponential_scores[j][i])

		# add selected scores into sorted score
		geman_sorted_scores.append(geman_selected_score)
		linear_sorted_scores.append(linear_selected_score)
		sigmoidal_sorted_scores.append(sigmoidal_selected_score)
		exponential_sorted_scores.append(exponential_selected_score)

	# calculate average for each sorted scores
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

	# store average scores in one list
	average_scores = [geman_average_scores, linear_average_scores, sigmoidal_average_scores, exponential_average_scores]

	# create plot with multiple lines of all coolingschemes
	multiple_simulated_annealing(average_scores)

def multiple_simulated_annealing(scores):
	""" Plots schedule score during simulated annealing for different coolingschemes """

	plt.plot(range(0, len(scores[0])), scores[0], label = "geman")
	plt.plot(range(0, len(scores[1])), scores[1], label = "linear")
	plt.plot(range(0, len(scores[2])), scores[2], label = "sigmoidal")
	plt.plot(range(0, len(scores[3])), scores[3], label = "exponential")
	plt.ylabel("Score")
	plt.xlabel("Runs")
	plt.title("Simulated annealing")
	plt.legend()
	plt.show()


# plot_average_SA(20, 5000)
# multiple_simulated_annealing(scores)
# print_schedule(best_schedule, best_courses, best_student_list, best_chambers)

chambers, allcourses, student_list, schedule = create_schedule()
print(allcourses.students)
# print(course.names, course.students)
