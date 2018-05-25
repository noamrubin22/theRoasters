# import main
import csv
import re
# from main import createSchedule
from scorefunction import calcScore
from generateschedule import createEmptySchedule, createSchedule
import random
from hillclimber import swapCourse, hillclimbRoomlocks
from generateschedule import updateClassesFromSchedule
from hillclimberscheduleplaces import swapCourse2, hillclimbRoomlocks2

total_gen_scores = {}

def genetic(initial, survival_rate, offspring, generations, mutation):
    """ Implements a genetic algorithm on scheduling problem """
    print("\n\t\tCreating initial population...\n")
    genesis = initial_population(initial)
    print("\t\tSelecting fittest individuals...\n")
    fittest = selection(genesis, survival_rate)
    print("\t\tSomething about the birds and the bees...\n")
    children = cross_over(fittest, offspring, 0, mutation)

    for i in range(generations):
        fittest = selection(children, survival_rate)
        children = cross_over(fittest, offspring, i + 1, mutation)
        # print("fittest: ", calcScore(fittest[0][0][0], fittest[0][0][1], fittest[0][0][2]))

    fittest = selection(children, survival_rate)
    allcourses = fittest[0][0][0]
    chambers = fittest[0][0][2]
    student_list = fittest[0][0][1]
    schedule = fittest[0][1]
    fittest_score = calcScore(allcourses, student_list, chambers)
    print("\t\tFittest: ", fittest_score)

    score_file = open('scores.txt', 'w')

    score_file.write(str(total_gen_scores))

    return schedule, allcourses, student_list, chambers

    print_schedule(schedule, allcourses, student_list, chambers)

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

        # print("Hillclimbing on schedule {}...".format(i))
        # hillclimbRoomlocks2(20, chambers, allcourses, student_list, schedule)


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


def selection(population, rate):
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
    probability = int(rate * len(population))
    rate = int(rate * 100)

    for i in range(rate):
        # fittest schedules have highest probabilities
        scores.append(calcScore(population[i][0][0], population[i][0][1], population[i][0][2]))
        mating_pool.append(population[i])

    # iterate over parents
    # for i in range(rate):
    #
    #     # create matingpool
    #     for j in range(probability):
    #
    #         # fittest schedules have highest probabilities
    #         scores.append(calcScore(population[i][0][0], population[i][0][1], population[i][0][2]))
    #         mating_pool.append(population[i])
    #
    #     # decrease probability
    #     probability -= 1

    return mating_pool


def mutation(schedule, chambers, allcourses, student_list, chance):


    probability = random.random()

    if probability < chance:
        hillclimbRoomlocks2(int(probability * 100), chambers, allcourses, student_list, schedule)

    return



def cross_over(mating_pool, offspring, generation, chance):
    """ Creates offspring by exchanging genes from mating pool """

    # create empty list for children
    children = []
    fittest_score = 0
    chance_array = []
    gen_scores = []

    probability = len(mating_pool)

    for i in range(len(mating_pool)):
        for j in range(probability):
            chance_array.append(i)
        probability -= 1



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
        random_parent = chance_array[random.randint(0, len(chance_array) - 1)]
        parent_schedule = parents[random_parent][1]
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
                    if newparentcounter > 500:
                        break
                    # print("nieuwe parent gekozen")

            schedule[random_course] = parent_schedule[random_course]

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
        gen_scores.append(score)



        if score > fittest_score:
            fittest_score = score
            print("New best found ---> Schedule: {}, generation: {}, score: {}".format(i, generation, score))


        # add the array with individual timetable-info to the population
        children.append(timetable_info)


    total_gen_scores[generation] = gen_scores
    return children


# genetic(50, 0.20, 50, 2, 0.2)
