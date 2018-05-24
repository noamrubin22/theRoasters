import math


start_temp = 1000000
final_temp = 1
sig_const = 0.3
reheats = 4


def linear_temperature(current_temp, min_iterations, i):
    """ Returns temperature calculated with a linear function """

    temperature = current_temp - i * (current_temp - final_temp) / min_iterations
    
    return temperature


def exponential_temperature(current_temp, min_iterations, i, start = start_temp):
    """ Returns temperature calculated with an exponential function """

    temperature = (current_temp * (final_temp / start) ** (i / min_iterations))
 
    return temperature 


