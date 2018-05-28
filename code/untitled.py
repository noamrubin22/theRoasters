import csv
import random
import math
from classes import Students, Room, Course
from helpers import *
from algorithms import *
import matplotlib.pyplot as plt


chambers, allcourses, student_list, schedule = create_schedule()

for course in allcourses:
	print(len(allcourses))
	print(course.name, course.students, len(course.seminargroups) + len(course.practicalgroups), course.seminars + course.practicals)