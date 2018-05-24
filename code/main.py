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
# import SA
from parse import createStudentClass, parse, gimme_students
from classes import Students, Room, Course
from generateschedule import createSchedule, updateClassesFromSchedule
from scorefunction import calcScore
from hillclimber import hillclimbRoomlocks
from hillclimberstudents import hillclimbStudent
# from SA import simulatedAnnealing

# create schedule
chambers, allcourses, student_list, schedule = createSchedule()



# print original score
originalscore, allcoursespoints = calcScore(allcourses, student_list, chambers)
print("Started with: ", originalscore)
print(allcoursespoints)

# perform hillclimber for roomlocks

hillclimbRoomlocks(3000, chambers, allcourses, student_list, schedule)

# show intermediate score
intermediate_score, allcoursespoints = calcScore(allcourses, student_list, chambers)
print("After roomlock hillclimber:", intermediate_score)


# perform hillclimber for students
hillclimbStudent(1000, chambers, allcourses, student_list, schedule)

# calculate and show final score
endscore, allcoursespoints = calcScore(allcourses, student_list, chambers)

print("Final score:", endscore)
print(allcoursespoints)





