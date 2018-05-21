import main
import scorefunction
import random
import subprocess
import sys
from scorefunction import calcScore
from main import complementCourse
from main import prepareData


scores = []

for i in range(0, 10):
	# chambers, allcourses, student_list, schedule = prepareData()
	# complementCourse()
	score = calcScore(main.allcourses, main.student_list, main.chambers)
	scores.append(score)

print(scores)