######################################################
# Heuristieken: Lectures & Lesroosters               #
#                                                    #
# Names: Tessa Ridderikhof, Najib el Moussaoui       #
#       & Noam Rubin                                 #
#                                                    #
# This code is able to run different algorithms in   #
# order to solve the scheduleling optimalisation     #
# problem                                            #
#                                                    #
######################################################

import csv
import random
import math
from classes import Students, Room, Course
from helpers import *
from algorithms import *


def main():
    """ This function asks gives the user the possibility to choose between different algorithms to improve a schedule """

    # introduction
    print("\n\tWelcome to lectures! :)\n")

    # prompt for input selection algorithm
    algorithm = int(input("Select your algorithm:\n 1. Hillclimber Algorithm\n 2. Simulated Annealing Algorithm\n 3. Genetic Algorithm\n\n Algorithm (1/2/3): "))

    # prompt for input again when wrongly answered
    while algorithm < 0 or algorithm > 3:
        print("\n  That's not an option...\n")
        algorithm = int(input("Select your algorithm:\n1. Hillclimber Algorithm\n2. Simulated Annealing Algorithm\n3. Genetic Algorithm\n\n Algorithm (1/2/3): "))

    # if answer = 1
    if algorithm == 1:
        print("\nAfter climbing a great hill, one only finds that there are many more hills to climb. - Nelson Mandela\n")

        # let user choose hillclimber
        print("Choose what kind:\n")
        kind = int(input(" 1. Roomlock hillclimber\n 2. Student hillclimber\n 3. Combined (double the fun!)\n  Your choice (number): "))

        # let user choose amount of iterations
        iterations = int(input("\nAmount of iterations (integer): "))

        # if input incorrect, prompt again
        while kind < 1 or kind > 3 and iterations < 0:
            print("Incorrect input, try again.\n")
            kind = input(" 1. Roomlock hillclimber\n 2. Student hillclimber\n 3. Combined (double the fun!)\n  Your choice (number): ")
            iterations = input("\nAmount of iterations (integer): ")

        # create random schedule
        chambers, allcourses, student_list, schedule = create_schedule()

        print("\n\t\tClimbing...\n")

        # perform chosen hillclimber
        if kind == 1:
            hillclimb_roomlocks(iterations, chambers, allcourses, student_list, schedule)
        elif kind == 2:
            hillclimb_student(iterations, chambers, allcourses, student_list, schedule)
        elif kind == 3:
            hillclimb_roomlocks(iterations, chambers, allcourses, student_list, schedule)
            hillclimb_student(iterations, chambers, allcourses, student_list, schedule)

        # visualize schedule
        print_schedule(schedule, allcourses, student_list, chambers)

    # if simulated annealing is chosen
    elif algorithm == 2:
        print("\nIt's funny because we're all living in a simulation and free will is a lie.\n")

        # let user choose cooling scheme
        print("Choose your cooling scheme:\n")
        cooling = int(input(" 1. Linear\n 2. Exponential\n 3. Sigmoidal\n 4. Geman\n  Your choice (number): "))

        # if input is incorrect, let user choose again
        while cooling < 1 or cooling > 4:
            print("Incorrect input, try again.\n")
            cooling = int(input(" 1. Linear\n 2. Exponential\n 3. Sigmoidal\n 4. Geman\n  Your choice (number): "))

        # link numbers to cooling schemes
        if cooling == 1:
            cooling = linear
        elif cooling == 2:
            cooling = exponential
        elif cooling == 3:
            cooling = sigmoidal
        elif cooling == 4:
            cooling = geman

        # prompt user for amount iterations
        iterations = int(input("\nAmount of iterations (integer): "))

        # if input is incorreect, let user choose again
        while iterations is not int(iterations) and iterations < 0:
            print("Incorrect input, try again.\n")
            iterations = int(input("\nAmount of iterations (integer): "))

        # run simulated annealing with chosen cooling scheme
        print("\n\t\tSimulating...\n")
        chambers, allcourses, student_list, schedule = create_schedule()
        best_schedule, best_score, best_courses, best_student_list, best_chambers, scores = simulated_annealing(cooling, iterations, chambers, allcourses, student_list, schedule)

        # visualize schedule
        print_schedule(best_schedule, best_courses, best_student_list, best_chambers)

    # if genetic algorithm is chosen
    elif algorithm == 3:
        print("\nSo you think you're better than nature? Prove it!\n")

        # prompt for input genetic algorithm
        initial = int(input("\nInitial population (integer): "))
        survival = float(input("Survival rate per generation (0.0 - 1.0): "))
        offspring = int(input("Amount of offspring per generation (integer): "))
        generations = int(input("Amount of generations (integer): "))
        mutation = float(input("Mutation rate (0.0 - 1.0): "))
        type = int(input("\nChoose your mutation type: \n  1. Designer:\t timeslot hillclimber\n  2. Random:\t single timelock swap\n\n  Your choice: "))

        # run genetic algorithm with chosen variables
        schedule, allcourses, student_list, chambers = genetic(initial, survival, offspring, generations, mutation, type)

        # visualize schedule
        print("\n...\n")
        print_schedule(schedule, allcourses, student_list, chambers)

if __name__ == "__main__":
    main()
