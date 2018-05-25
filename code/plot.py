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
	plt.title("Simulated annealing")
	plt.text(5, max(scores)/ 2, best_score)
	plt.legend()
	plt.show()	


def plot_random_schedules(scores):
	""" Creates an histogram of random schedules"""

	plt.hist(scores, bins = len(scores))
	plt.ylabel("Score")
	plt.xlabel("Times")
	plt.title("Histogram random schedules")
	plt.show()


def plot_hillclimber(scores):
	""" Plots schedule score during hillclimber """

	plt.plot(range(0, len(scores)), scores)
	plt.ylabel("Score")
	plt.xlabel("Amount of swaps")
	plt.title("Hillclimber")
	plt.show()

