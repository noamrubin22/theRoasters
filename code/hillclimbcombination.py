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
from parse import createStudentClass, parse, gimme_students
from classes import Students, Room, Course
from generateschedule import createSchedule, updateClassesFromSchedule
from scorefunction import calcScore
from hillclimber import hillclimbRoomlocks
from hillclimberstudents import hillclimbStudent
from SA import simulatedAnnealing
from coolingschemes import linear, exponential, sigmoidal, geman, lin_exp 
from printschedule import print_schedule
from plot import plot_simulated_annealing

# create schedule
chambers, allcourses, student_list, schedule = createSchedule()
chambers1, allcourses1, student_list1, schedule1 = chambers, allcourses, student_list, schedule

# print(schedule1)
# print original score
originalscore = calcScore(allcourses, student_list, chambers)
print("Started with: ", originalscore)


# perform hillclimber for roomlocks

# hillclimbStudent(1000, chambers, allcourses, student_list, schedule)

# show intermediate score
# intermediate_score = calcScore(allcourses, student_list, chambers)
# print("After roomlock hillclimber:", intermediate_score)

for i in range(3000):
	# print(allcourses[1].seminargroups)
	hillclimbRoomlocks(1, chambers, allcourses, student_list, schedule)
	hillclimbStudent(10, chambers, allcourses, student_list, schedule)
	
	# show intermediate score
	intermediate_score = calcScore(allcourses, student_list, chambers)
	print("After loop:", intermediate_score)

# calculate and show final score
endscore = calcScore(allcourses, student_list, chambers)

print("Final score:", endscore)
