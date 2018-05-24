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



#mega slecht
# def geman_temperature(current_temp, total_iters, i):

#     return start_temp/(math.log(i+1) + 1)


def lin_sig(current_temp, min_iterations, i):
    if i < min_iterations/2:
        return linear(temperature, total_iters, i)
    return sigmoidal(temperature, total_iters, i)

# def exp_sig_full(temperature, total_iters, i):
#     if i < total_iters/2:
#         return exponential(temperature, total_iters, i)
#     return sigmoidal(temperature, total_iters - total_iters/2, \
#             i - total_iters/2)

# def exp_sig_part(temperature, total_iters, i):
#     if i < total_iters/2:
#         return exponential(temperature, total_iters, i)
#     return sigmoidal(temperature, total_iters, i)

# def exp_reheat(temperature, total_iters, i):
#     for j in range(REHEATS-1,-1,-1):
#         if i == int(total_iters * j/REHEATS):
#             return START_TEMP * (1 - j/REHEATS)
#         elif i > int(total_iters * j/REHEATS):
#             return exponential(temperature, total_iters * (1 - j/REHEATS), \
#                     i - total_iters * (j/REHEATS), START_TEMP * (1 - j/REHEATS))

# def exp_lin(temperature, total_iters, i):
#     if i == int(total_iters/2):
#         return START_TEMP/2
#     elif i < total_iters/2:
#         return exponential(temperature, total_iters, i)
#     else:
#         return linear(temperature, total_iters, i)