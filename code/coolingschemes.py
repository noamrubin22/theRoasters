import math


start_temp = 1000000
final_temp = 1
sig_const = 0.3
reheats = 4


def linear(current_temp, min_iterations, i):
    """ Returns temperature calculated using a linear function """

    temperature = current_temp - i * (current_temp - final_temp) / min_iterations
    
    return temperature


def exponential(current_temp, min_iterations, i, start = start_temp):
    """ Returns temperature calculated using an exponential function """

    temperature = (current_temp * (final_temp / start) ** (i / min_iterations))
 
    return temperature 


def sigmoidal(current_temp, min_iterations, i):
    """ Returns temperature, calculated using a sigmoidal function """

    # to prevent a math overflow a scale (x^(1/ (i - min_iterations))) is used
    temperature = final_temp + ((start_temp - final_temp)**( 1/ (i - min_iterations))) / \
    				(1 **(i - min_iterations)) + math.exp(0.3 * ((i - min_iterations / 2) /(i - min_iterations)))

    return temperature

# def geman(current_temp, min_iterations, i):
# 	""" Returns temperature, calculated using a geman function """
 
# 	temperature = start_temp / (log(i + 1)) + 1) 
	
# 	return temperature