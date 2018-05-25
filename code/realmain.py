from __future__ import division
import csv
import random
import math
# <<<<<<< HEAD
# import generateschedule
# import scorefunction
# import hillclimber
# from parse import createStudentClass, parse
from parse import *
from classes import Students, Room, Course
from helpers import *
from algorithms import *
# from generateschedule import createSchedule, updateClassesFromSchedule
# from scorefunction import calcScore
# from hillclimber import hillclimbRoomlocks
# from hillclimberstudents import hillclimbStudent
# from SA import simulatedAnnealing
# from coolingschemes import linear, exponential, sigmoidal, geman, lin_exp
# from printschedule import print_schedule
# from plot import plot_simulated_annealing
# from genetic import genetic
# =======
# import hillclimber
# from parse import createStudentClass, parse, gimme_students
# from classes import Students, Room, Course
# from helpers import createSchedule, updateClassesFromSchedule, calcScore
# from hillclimber import hillclimbRoomlocks
# from hillclimberstudents import hillclimbStudent
# from SA import simulatedAnnealing
# from helpers import linear, exponential, sigmoidal, geman, lin_exp
# from printschedule import print_schedule
# from plot import plot_simulated_annealing
# from genetic import genetic
# >>>>>>> 0776b41f76caddcecdb50c1a1360d02c2bdce87c

def main():

    print("\n\tWelcome to lectures! :)\n")
    algorithm = int(input("Select your algorithm:\n 1. Hillclimber Algorithm\n 2. Simulated Annealing Algorithm\n 3. Genetic Algorithm\n\n Algorithm (1/2/3): "))

    while algorithm < 0 or algorithm > 3:
        print("\n  That's not an option...\n")
        algorithm = int(input("Select your algorithm:\n1. Hillclimber Algorithm\n2. Simulated Annealing Algorithm\n3. Genetic Algorithm\n\n Algorithm (1/2/3): "))


    if algorithm == 1:
        print("\nAfter climbing a great hill, one only finds that there are many more hills to climb. - Nelson Mandela\n")

        print("Choose what kind:\n")
        kind = int(input(" 1. Roomlock hillclimber\n 2. Student hillclimber\n 3. Combined (double the fun!)\n  Your choice (number): "))
        iterations = int(input("\nAmount of iterations (integer): "))

        while kind < 1 or kind > 3 and iterations < 0:
            print("Incorrect input, try again.\n")
            kind = input(" 1. Roomlock hillclimber\n 2. Student hillclimber\n 3. Combined (double the fun!)\n  Your choice (number): ")
            iterations = input("\nAmount of iterations (integer): ")

        chambers, allcourses, student_list, schedule = create_schedule()

        print("\n\t\tClimbing...\n")

        if kind == 1:
            hillclimb_roomlocks(iterations, chambers, allcourses, student_list, schedule)
        elif kind == 2:
            hillclimb_student(iterations, chambers, allcourses, student_list, schedule)
        elif kind == 3:
            hillclimb_roomlocks(iterations, chambers, allcourses, student_list, schedule)
            hillclimb_student(iterations, chambers, allcourses, student_list, schedule)

        print_schedule(schedule, allcourses, student_list, chambers)


    elif algorithm == 2:
        print("\nIt's funny because we're all living in a simulation and free will is a lie.\n")


        print("Choose your cooling scheme:\n")
        cooling = int(input(" 1. Linear\n 2. Exponential\n 3. Sigmoidal\n 4. Geman\n  Your choice (number): "))

        while cooling < 1 or cooling > 4:
            print("Incorrect input, try again.\n")
            cooling = int(input(" 1. Linear\n 2. Exponential\n 3. Sigmoidal\n 4. Geman\n  Your choice (number): "))

        if cooling == 1:
            cooling = linear
        elif cooling == 2:
            cooling = exponential
        elif cooling == 3:
            cooling = sigmoidal
        elif cooling == 4:
            cooling = geman

        iterations = int(input("\nAmount of iterations (integer): "))

        while iterations is not int(iterations) and iterations < 0:
            print("Incorrect input, try again.\n")
            iterations = int(input("\nAmount of iterations (integer): "))

        print("\n\t\tSimulating...\n")
        chambers, allcourses, student_list, schedule = create_schedule()
        best_schedule, best_score, best_courses, best_student_list, best_chambers, scores = simulated_annealing(cooling, iterations, chambers, allcourses, student_list, schedule)

        print_schedule(best_schedule, best_courses, best_student_list, best_chambers)

    elif algorithm == 3:
        print("\nSo you think you're better than nature? Prove it!\n")
        initial = int(input("\nInitial population (integer): "))
        survival = int(float(input("Survival rate per generation (0.0 - 1.0): ")))
        offspring = int(input("Amount of offspring per generation (integer): "))
        generations = int(input("Amount of generations (integer): "))
        mutation = int(float(input("Mutation rate (0.0 - 1.0): ")))

        schedule, allcourses, student_list, chambers = genetic(initial, survival, offspring, generations, mutation)

        print("\n...\n")
        print_schedule(schedule, allcourses, student_list, chambers)

if __name__ == "__main__":
    main()
