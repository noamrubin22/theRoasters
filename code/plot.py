###################################################
# Heuristieken: Lectures & Lesroosters			  #
#												  #
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  #
# 		 & Noam Rubin							  #
#												  #
# This code consists of function that can plot	  #
# the schedule scores after using different		  #
# algorithms									  #
#												  #
###################################################

import csv
import matplotlib.pyplot as plt
from generateschedule import createSchedule
from SA import simulatedAnnealing

# input = [(scores, type), (scores,type)]
def plot_simulated_annealing(scores, coolingscheme, best_score): 
	""" Plots schedule score during simulated annealing """ 

	functionname = str(coolingscheme.__name__)
	plt.plot(range(0, len(scores)), scores, label=functionname)
	plt.ylabel("Score")
	plt.xlabel("Runs")
	plt.title("Simulated annealing")
	plt.text(5, (max(scores)/ 2), best_score)
	plt.legend()
	plt.show()	

def plot_random_schedules(scores):
	""" Creates an histogram of random schedules"""

	plt.hist(scores, bins = len(scores))
	plt.ylabel("Score")
	plt.xlabel("Times")
	plt.title("Histogram random schedules")
	plt.show()


def plot_hillclimber(scores, hillclimb_students_scores = None):
	""" Plots schedule score during hillclimber """

	plt.plot(range(0, len(scores)), scores)
	if hillclimb_students_scores:
		plt.plot(range(len(scores), len(scores) + len(hillclimb_students_scores)), hillclimb_students_scores)
	plt.ylabel("Score")
	plt.xlabel("Amount of swaps")
	plt.title("Hillclimber")
	plt.show()


def multiple_simulated_annealing(scores): 
	""" Plots schedule score during simulated annealing for different coolingschemes """ 

	plt.plot(range(0, len(scores[0])), scores[0], label = "geman")
	plt.plot(range(0, len(scores[1])), scores[1], label = "linear")
	plt.plot(range(0, len(scores[2])), scores[2], label = "sigmoidal")
	plt.plot(range(0, len(scores[3])), scores[3], label = "exponential")		
	plt.ylabel("Score")
	plt.xlabel("Runs")
	plt.title("Simulated annealing")
	# plt.text(5, max(scores[0]))
	plt.legend()
	plt.show()	
