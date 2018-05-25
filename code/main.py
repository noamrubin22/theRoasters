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
from coolingschemes import linear, exponential, sigmoidal
from printschedule import print_schedule

# create schedule
chambers, allcourses, student_list, schedule = createSchedule()


# print original score
originalscore = calcScore(allcourses, student_list, chambers)
print("Started with: ", originalscore)


# # perform hillclimber for roomlocks

# hillclimbRoomlocks(5000, chambers, allcourses, student_list, schedule)

# show intermediate score
intermediate_score = calcScore(allcourses, student_list, chambers)
print("After roomlock hillclimber:", intermediate_score)


# # perform hillclimber for students
# hillclimbStudent(1000, chambers, allcourses, student_list, schedule)

# calculate and show final score
endscore = calcScore(allcourses, student_list, chambers)

print("Final score:", endscore)

# print_schedule(schedule, allcourses, student_list, chambers)


simulatedAnnealing(sigmoidal, 100000, chambers, allcourses, student_list, schedule)


