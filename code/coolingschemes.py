import math


start_temp = 1000000
final_temp = 1
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

    temperature = final_temp + (start_temp - final_temp) / (1 + math.exp(0.3 * (i - min_iterations / 2)))
    
    return temperature