import main
import csv
from main import createSchedule
from scorefunction import calcScore
from printschedule import print_schedule
from generateschedule import createEmptySchedule
import random


def initial_population(amount):

    population = []
    parents_max = 10
    scores = []

    for i in range(amount):
        timetable_info = []
        score_info = []

        # create a new random schedule
        chambers, allcourses, student_list, schedule = createSchedule()

        # add all information about this specific schedule to an array
        score_info.append(allcourses)
        score_info.append(student_list)
        score_info.append(chambers)


        timetable_info.append(score_info)
        timetable_info.append(schedule)

        # add the array of information about this schedule to the timetable_info array
        population.append(timetable_info)

    return population


def selection(population):

    mating_pool = []
    scores = []

    def points_score(timetable_info):
        return calcScore(timetable_info[0][0],
                         timetable_info[0][1],
                         timetable_info[0][2])

    population = sorted(population, key=points_score, reverse=True)

    multiply = 10
    parents_max = 10

    for i in range(parents_max):
        for j in range(multiply):
            scores.append(calcScore(population[i][0][0], population[i][0][1], population[i][0][2]))
            mating_pool.append(population[i])
        multiply -= 1

    print(scores)

    return mating_pool


def cross_over(mating_pool):

    children = []

    for i in range(new_population):

        # first create an empty schedule
        schedule = createEmptySchedule()
        
        mother = mating_pool[random.randint(0, len(mating_pool))]
        father = mating_pool[random.randint(0, len(mating_pool))]

    print(mother, father)



mating_pool = selection(initial_population(100))

cross_over(mating_pool)


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
