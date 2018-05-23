import main
import csv
from main import createSchedule
from scorefunction import calcScore
from printschedule import print_schedule
from generateschedule import createEmptySchedule
import random


def initial_population(amount):

    population = []
    scores = []

    for i in range(amount):
        timetable_info = []
        score_info = []

        # create a new random schedule
        chambers, allcourses, student_list, schedule = createSchedule()

        # add all information about this specific schedule
        score_info.append(allcourses)
        score_info.append(student_list)
        score_info.append(chambers)

        # add individual schedule-info to timetable array
        timetable_info.append(score_info)
        timetable_info.append(schedule)

        # add the array with individual timetable-info to the population
        population.append(timetable_info)

    return population


def selection(population):
    """ Calculates the fitness of an individual by returning the schedule score """

    mating_pool = []
    scores = []

    def fitness(timetable_info):
        """ Calculates the fitness of an individual """

        return calcScore(timetable_info[0][0],
                         timetable_info[0][1],
                         timetable_info[0][2])

    # choose the fittest individuals
    population = sorted(population, key=fitness, reverse=True)

    # set max and range
    probability = 10
    parents_max = 10

    # create mating pool, with the fittest schedules
    for i in range(parents_max):
        for j in range(probability):

            # fittest schedules have highest probability
            scores.append(calcScore(population[i][0][0], population[i][0][1], population[i][0][2]))
            mating_pool.append(population[i])

        # decrease probability
        probability -= 1

    print(scores)

    return mating_pool


def cross_over(mating_pool, offspring):
    """ Creates offspring from mating pool by exchanging genes """

    # create empty list for children
    children = []

    for i in range(offspring):

        # first create an empty schedule
        schedule = createEmptySchedule()

        print(schedule)

        # get a mother and father from the mating pool
        mother = mating_pool[random.randint(0, len(mating_pool))]
        father = mating_pool[random.randint(0, len(mating_pool))]







mating_pool = selection(initial_population(100))


#     for i in range(new_population):
#         schedule = createEmptySchedule()
#
#
#
#
#
#
# cross_over(2)
#
#
#
#
#     # random_parent = random.randint(0, len(mating_pool))
#     pickroomlock = random.randint(0, 139)
#
#     while new_population > 0:
#
#         parent = [random.randint(0, len(mating_pool))]
#         pickroomlock = random.randint(0, 139)
#
#         ...
#
#         new_population -= 1
