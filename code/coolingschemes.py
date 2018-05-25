#####################################################
# Heuristieken: Lectures & Lesroosters			  	#
#												  	#
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  	#
# 		 & Noam Rubin							  	#
#												  	#
# This code consist of function that present the   	#
# different cooling schemes recommended for     	#
# the simulated annealing alogirthm 			 	#
#												  	#
#####################################################

import math

# initiliaze temperatures
start_temp = 10
final_temp = 0.0001


def linear(min_iterations, i, start = start_temp, final = final_temp):
    """ Returns temperature calculated using a linear function """

    temperature = start - i * (start - final) / min_iterations
    
    return temperature


def exponential(min_iterations, i, start = start_temp, final = final_temp):
    """ Returns temperature calculated using an exponential function """

    temperature = (start * (final / start) ** (i / min_iterations))
 
    return temperature 


def sigmoidal(min_iterations, i, start = start_temp, final = final_temp ):
    """ Returns temperature, calculated using a sigmoidal function """

    # to prevent a math overflow a scale (x^(1/ (i - min_iterations))) is used
    temperature = final + ((start - final)**( 1/ (i - min_iterations))) / \
    				(1 **(i - min_iterations)) + math.exp(0.3 * ((i - min_iterations / 2) /(i - min_iterations)))

    return temperature

def geman(min_iterations, i, start = start_temp):
	""" Returns temperature, calculated using a geman function """
 
	temperature = start / (math.log(i + 1) + 1) 
	
	return temperature


def lin_exp(min_iterations, i): 
    """ Temperature is calculated using an exponential and linear function """

    # vary between the functions
    if i % 2 == 0: 
        return exponential(current_temp, min_iterations, i)
    else: 
        return linear(current_temp, min_iterations, i)

def exp_sig(min_iterations, i): 
    """ Temperature is calculated using an exponential and linear function """

    # vary between the functions
    if i % 2 == 0: 
        return sigmoidal(current_temp, min_iterations, i)
    else: 
        return exponential(current_temp, min_iterations, i)


def gem_lin(min_iterations, i): 
    """ Temperature is calculated using an exponential and linear function """

    # vary between the functions
    if i % 2 == 0: 
        return linear(current_temp, min_iterations, i)
    else: 
        return geman(current_temp, min_iterations, i)



def gem_exp(min_iterations, i): 
    """ Temperature is calculated using an exponential and linear function """

    # vary between the functions
    if i % 2 == 0: 
        return geman(current_temp, min_iterations, i)
    else: 
        return exponential(current_temp, min_iterations, i)



