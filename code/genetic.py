
# import main
import csv
import re
# from main import createSchedule
from scorefunction import calcScore
from generateschedule import createEmptySchedule, createSchedule
import random
from hillclimber import swapCourse
from generateschedule import updateClassesFromSchedule

def genetic(initial, offspring, generations, mutation):
    """ Implements a genetic algorithm on scheduling problem """
    print("Creating initial population...")
    genesis = initial_population(initial)
    print("Selecting fittest individuals...")
    fittest = selection(genesis)
    print("Mating :)))))))")
    children = cross_over(fittest, offspring, 0, mutation)

    for i in range(generations):
        fittest = selection(children)
        children = cross_over(fittest, offspring, i + 1, mutation)

    # print(children[1])
    fittest = selection(children)
    # print("fittest: ", calcScore(fittest[0][0][0], fittest[0][0][1], fittest[0][0][2]))

def initial_population(amount):
    """ Creates an intial population and returns the parents """

    # create empty list
    population = []
    scores = []

    for i in range(amount):

        # print("Generating initial population...")

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

        # print("Calculating fitness scores...")

        return calcScore(timetable_info[0][0],
                         timetable_info[0][1],
                         timetable_info[0][2])


    # choose the fittest individuals
    population = sorted(population, key=fitness, reverse=True)

    # set max and range
    probability = 10
    parents_max = 10

    # iterate over parents
    for i in range(parents_max):

        # create matingpool
        for j in range(probability):

            # fittest schedules have highest probabilities
            scores.append(calcScore(population[i][0][0], population[i][0][1], population[i][0][2]))
            mating_pool.append(population[i])

        # decrease probability
        probability -= 1

    return mating_pool

<<<<<<< HEAD
def mutation(schedule, chance):
=======
def mutation(schedule, chambers, allcourses, student_list, chance):
>>>>>>> 823e13e2ce2d6150a60998bae3f1f1fcca01f720

    probability = random.random()

    if probability < chance:
        swapCourse(chambers, allcourses, student_list, schedule)

    return


<<<<<<< HEAD
def cross_over(mating_pool, offspring, generation):
=======
def cross_over(mating_pool, offspring, generation, chance):
>>>>>>> 823e13e2ce2d6150a60998bae3f1f1fcca01f720
    """ Creates offspring by exchanging genes from mating pool """

    # create empty list for children
    children = []

    # iterate over offspring
    for i in range(offspring):

        # create an empty schedule
        schedule = createEmptySchedule()
        activities = 125


        # get a mother and father from the mating pool
        parents = []

        parents = mating_pool

        # for j in range(10):
        #     parents.append(mating_pool[random.randint(0, len(mating_pool) - 1)])

        parent_schedule = parents[random.randint(0, len(parents) - 1)][1]
        # print(parent_schedule)


        while activities > 0:

            # print("Applying crossover between parents...")

            # if activities % 2 == 0:
            #     parent_schedule = parents[0][1]  # >>> [[allcourses, chambers, studentlist], schedule]
            # else:
            #     parent_schedule = parents[1][1]

            random_course = random.randint(0, len(parent_schedule) - 1)


            courses = []

            for key, value in schedule.items():
                if value is not None:
                    courses.append(value)

            counter = 0
            newparentcounter = 0
            while schedule[random_course] is not None or parent_schedule[random_course] is None or parent_schedule[random_course] in courses:
                random_course = random.randint(0, len(parent_schedule) - 1)
                counter += 1
                # print(counter)
                if counter > 100:
                    parent_schedule = parents[random.randint(0, len(parents) - 1)][1]
                    counter = 0
                    newparentcounter += 1
<<<<<<< HEAD
                    if newparentcounter > 100:
                        break

=======
                    if newparentcounter > 500:
                        break
>>>>>>> 823e13e2ce2d6150a60998bae3f1f1fcca01f720
                    # print("nieuwe parent gekozen")




            # print("Amount of activities left: {}, courses array[{}]: {}".format(activities, len(courses), courses))

            # while parent_schedule[random_course] in courses:
            #     random_course = random.randint(0, len(parent_schedule) - 1)

            # print(schedule[random_course], end="")
            schedule[random_course] = parent_schedule[random_course]
            # print(" ----> wordt ----> {}".format(schedule[random_course], parent_schedule[random_course]))

            # if activities == 1:
            #     print("Courses[{}]: {}".format(len(courses), courses))

            activities -= 1

        allcourses, student_list, chambers = updateClassesFromSchedule(schedule)

        timetable_info = []
        score_info = []

        # add all information about this specific schedule
        score_info.append(allcourses)
        score_info.append(student_list)
        score_info.append(chambers)

        mutation(schedule, chambers, allcourses, student_list, chance)

        # add individual schedule-info to timetable array
        timetable_info.append(score_info)
        timetable_info.append(schedule)

        score = calcScore(allcourses, student_list, chambers)

        print("\n\n\n\nSchedule: {}, generation: {}, score: {}\n\n\n\{}\n\n\n\n".format(i, generation, score, schedule))

        # add the array with individual timetable-info to the population
        children.append(timetable_info)

    return children

<<<<<<< HEAD
genetic(1000, 100, 6, 0)




# initial = initial_population(10)
#
# selectie = selection(initial)
#
# cross_over(selectie, 1)
#
# student = initial[0][0][1][0]
#
# print(student.show_schedule())
#
# print("CHILD ===== ", cross_over(selectie, 2))
=======
genetic(1000, 50, 1, 0.2)
>>>>>>> 823e13e2ce2d6150a60998bae3f1f1fcca01f720
