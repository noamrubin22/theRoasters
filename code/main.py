import csv
import random
import math
import generateschedule
import scorefunction
from parse import *
from classes import Students, Room, Course
from generateschedule import complementCourse, createRooms, createCourses, createStudents, createEmptySchedule, createStudentGroups
from scorefunction import calcScore

def createSchedule():
	chambers = createRooms()
	allcourses = createCourses()
	student_list = createStudents()
	schedule = createEmptySchedule()
	allcourses, student_list = createStudentGroups(allcourses, student_list)
	complementCourse(allcourses, schedule, chambers, student_list)
	return chambers, allcourses, student_list, schedule

for i in range(10):
	chambers, allcourses, student_list, schedule = createSchedule()
