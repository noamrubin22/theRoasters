#####################################################
# Heuristieken: Lectures & Lesroosters			  	#
#												  	#
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  	#
# 		 & Noam Rubin							  	#
#												  	#
# This code 						   				#
# 												  	#
#####################################################

import csv
import random
import math
import generateschedule
import scorefunction
import hillclimber
import SA
from parse import createStudentClass, parse, gimme_students
from classes import Students, Room, Course
from generateschedule import createSchedule, updateClassesFromSchedule
from scorefunction import calcScore
from hillclimber import hillclimbRoomlocks
from hillclimberstudents import hillclimbStudent
from SA import simulatedAnnealing

# create schedule
chambers, allcourses, student_list, schedule = createSchedule()



# print original score
originalscore = calcScore(allcourses, student_list, chambers)
print("Started with: ", originalscore)


# # perform hillclimber for roomlocks
<<<<<<< HEAD
# hillclimbRoomlocks(3000, chambers, allcourses, student_list, schedule)

# # show intermediate score
# intermediate_score = calcScore(allcourses, student_list, chambers)
# print("After roomlock hillclimber:", intermediate_score)
=======
# hillclimbRoomlocks(1000, chambers, allcourses, student_list, schedule)

# # show intermediate score
# intermediate_score = calcScore(allcourses, student_list, chambers)
# # print("After roomlock hillclimber:", intermediate_score)
>>>>>>> f1c0473244e59b2f212fa402e6d03ee4f4c18d05

# # perform hillclimber for students
# hillclimbStudent(1000, chambers, allcourses, student_list, schedule)

# # calculate and show final score
# endscore = calcScore(allcourses, student_list, chambers)

# print("Final score:", endscore)

simulatedAnnealing(1000, 0.002, chambers, allcourses, student_list, schedule)

