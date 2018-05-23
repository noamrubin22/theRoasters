###################################################
# Heuristieken: Lectures & Lesroosters			  #
#												  #
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  #
# 		 & Noam Rubin							  #
#												  #
# This code creates a random schedule and 		  #
# performs the hillclimber algorithm 1000 times,  #
# and saves all scores of every step to a csv     #
# file.											  #
#												  #
###################################################

import csv 
import scorefunction
import hillclimber
import matplotlib.pyplot as plt
import hillclimberstudents
from scorefunction import calcScore
from hillclimberstudents import hillclimbStudent
from hillclimber import hillclimbRoomlocks
from generateschedule import createSchedule

# create empty array to hold the score of the schedule after every roomlock swap
scores = []

# create random schedule
chambers, allcourses, student_list, schedule = createSchedule()

# calculate the first score and add to array
points = calcScore(allcourses, student_list, chambers)
scores.append(points)

# swap roomlocks 1000 times (using the hillclimber algorithm)
for i in range(1000):
	
	# save score after every swap
	score = hillclimbRoomlocks(1, chambers, allcourses, student_list, schedule)
	
	# add score to array
	scores.append(score)

# plot scores
plt.plot(range(0, len(scores)), scores)
plt.ylabel("Score")
plt.xlabel("Amount of swaps")
plt.title("Hillclimber roomlocks")
plt.show()

# # write all scores to csv
# with open("hillclimberstudent.csv", "w") as resultFile:
# 	wr = csv.writer(resultFile, dialect = 'excel')
# 	wr.writerow(scores)