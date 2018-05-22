import csv
import random
import math
import generateschedule
import scorefunction
import hillclimber
import SA
# import creategraphs
from parse import *
from classes import Students, Room, Course
from generateschedule import complementCourse, createRooms, createCourses, createStudents, createEmptySchedule, createStudentGroups
from scorefunction import calcScore
from hillclimber import hillclimbRoomlocks
from hillclimberstudents import hillclimbStudent
from SA import simulatedAnnealing

def createSchedule():
	""" Creates a schedule """

	# creates lists for rooms, students and courses and schedule dict
	chambers = createRooms()

	# creates list with course information
	allcourses = createCourses()

	# create list with student information
	student_list = createStudents()

	# creates empty dict with roomlocks (schedule without courses)
	schedule = createEmptySchedule()

	# create student groups
	allcourses, student_list = createStudentGroups(allcourses, student_list)

	# schedule activities of each course
	complementCourse(allcourses, schedule, chambers, student_list)

	return chambers, allcourses, student_list, schedule

# create random schedule	
chambers, allcourses, student_list, schedule = createSchedule()

# print original score
originalscore = calcScore(allcourses, student_list, chambers)
print("Started with: ", originalscore)

# # perform hillclimber for roomlocks
# hillclimbRoomlocks(1000, chambers, allcourses, student_list, schedule)

# # show intermediate score
# intermediate_score = calcScore(allcourses, student_list, chambers)
# print("After roomlock hillclimber:", intermediate_score)

# # perform hillclimber for students
# hillclimbStudent(1000, chambers, allcourses, student_list, schedule)

# perform simulated annealing 
simulatedAnnealing(10000, 0.002, chambers, allcourses, student_list, schedule)

# calculate and show final score 
endscore = calcScore(allcourses, student_list, chambers)

print("Final score:", endscore)
