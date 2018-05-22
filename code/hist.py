import main
import scorefunction
import random
import subprocess
import sys
from scorefunction import calcScore
from main import complementCourse
from main import prepareData

scores = []





for i in range(0, 1000):
	chambers, allcourses, student_list, schedule = prepareData()
	allcourses, schedule, chambers, student_list = complementCourse(allcourses, schedule, chambers, student_list)
	score = calcScore(allcourses, student_list, chambers)
	scores.append(score)

print(scores)