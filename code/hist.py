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
import matplotlib.pyplot as plt
import plot
from scorefunction import calcScore
from hillclimber import hillclimbRoomlocks
from generateschedule import createSchedule
from plot import plot_random_schedules

# create empty array to hold scores
scores = []

# create 1000 random schedules
for i in range(0, 100):
	chambers, allcourses, student_list, schedule = createSchedule()	
	
	# calculate score of schedule
	# score = calcScore(allcourses, student_list, chambers)

	score = hillclimbRoomlocks(1000, chambers, allcourses, student_list, schedule)
	
	# append score to array
	scores.append(score)

# plot scores
plot_random_schedules(scores)
