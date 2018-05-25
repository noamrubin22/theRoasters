#####################################################
# Heuristieken: Lectures & Lesroosters			  	#
#												  	#
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  	#
# 		 & Noam Rubin							  	#
#												  	#
# This code 						   				#
# 												  	#
#####################################################

from __future__ import division
import csv
import random
import math
import generateschedule
import scorefunction
import hillclimber
# import SA
from parse import create_student_class, parse, gimme_students
from classes import Students, Room, Course
from generateschedule import create_schedule, update_classes_from_schedule
from scorefunction import calc_score
from hillclimber import hillclimb_roomlocks
from hillclimberstudents import hillclimb_student
from SA import simulated_annealing
from coolingschemes import linear, exponential, sigmoidal, geman, lin_exp, gem_lin, gem_exp, lin_exp_gem
from printschedule import print_schedule
from plot import plot_simulated_annealing

# create schedule
chambers, allcourses, student_list, schedule = create_schedule()
chambers1, allcourses1, student_list1, schedule1 = chambers, allcourses, student_list, schedule

# print(schedule1)
# print original score
originalscore = calc_score(allcourses, student_list, chambers)
print("Started with: ", originalscore)


# perform hillclimber for roomlocks

# hillclimbStudent(1000, chambers, allcourses, student_list, schedule)

# show intermediate score
# intermediate_score = calc_score(allcourses, student_list, chambers)
# print("After roomlock hillclimber:", intermediate_score)

# hillclimbRoomlocks(5000, chambers, allcourses, student_list, schedule)



# show intermediate score
intermediate_score = calc_score(allcourses, student_list, chambers)
print("After roomlock hillclimber:", intermediate_score)


# # perform hillclimber for students
# hillclimbStudent(10000, chambers, allcourses, student_list, schedule)

# hillclimbRoomlocks(2000, chambers, allcourses, student_list, schedule)

# calculate and show final score
endscore = calc_score(allcourses, student_list, chambers)

print("Final score:", endscore)

# print_schedule(schedule, allcourses, student_list, chambers)
# print(schedule1)

input = []


# perform geman
chambers, allcourses, student_list, schedule = create_schedule()
best_score, best_courses, best_student_list, best_chambers, scores = simulated_annealing(lin_exp_gem, 10, chambers, allcourses, student_list, schedule)
plot_simulated_annealing(scores, gem_lin, best_score)

# input.append(scores)
# print("........................................hoi")

# chambers, allcourses, student_list, schedule = create_schedule()
# best_score, best_courses, best_student_list, best_chambers, scores = simulated_annealing(linear, 100, chambers, allcourses, student_list, schedule)
# # plot_simulated_annealing(scores, linear, best_score)

# input.append(scores)
# print("              .............................................hallo")
# chambers, allcourses, student_list, schedule = create_schedule()
# best_score, best_courses, best_student_list, best_chambers, scores = simulated_annealing(sigmoidal, 100, chambers, allcourses, student_list, schedule)

# input.append(scores)
# print("...............................................................................hey")

# chambers, allcourses, student_list, schedule = create_schedule()
# best_score, best_courses, best_student_list, best_chambers, scores = simulated_annealing(exponential, 100, chambers, allcourses, student_list, schedule)
# # plot_simulated_annealing(scores, geman, best_score)
# input.append(scores)
# print(len(scores))
# print(scores)