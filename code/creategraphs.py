import csv 
# import main
import scorefunction
# import hillclimber
import hillclimberstudents
from scorefunction import calcScore
from hillclimberstudents import hillclimbStudent
from hillclimber import hillclimbRoomlocks

scores = []
points = calcScore(allcourses, student_list, chambers)
scores.append(points)

for i in range(10):
	score = hillclimbRoomlocks(1)
	scores.append(score)

print(scores)