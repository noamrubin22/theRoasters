###################################################
# Heuristieken: Lectures & Lesroosters			  #
#												  #
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  #
# 		 & Noam Rubin							  #
#												  #
# This code creates 1000 random schedules and 	  #
# saves their scores in a csv file.				  # 					  
#												  #
###################################################

import scorefunction
import csv
from scorefunction import calcScore
from generateschedule import createSchedule

# create empty array to hold scores
scores = []

# create 1000 random schedules
for i in range(0, 1000):
	chambers, allcourses, student_list, schedule = createSchedule()	
	
	# calculate score of schedule
	score = calcScore(allcourses, student_list, chambers)
	
	# append score to array
	scores.append(score)

# write score array to csv
with open("histscores.csv", "w") as resultFile:
	wr = csv.writer(resultFile, dialect = 'excel')
	wr.writerow(scores)