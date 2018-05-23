# import main
import csv
# from main import createSchedule
from scorefunction import calcScore
from printschedule import print_schedule
from generateschedule import createEmptySchedule, createSchedule
import random
from hillclimber import swapCourse

def genetic(initial, offspring, generations, mutation):
    """ Implements a genetic algorithm on scheduling problem """

    genesis = initial_population(initial)
    fittest = selection(genesis)
    children = cross_over(fittest, offspring)

    for i in range(generations):
        fittest = selection(children)
        children = cross_over(fittest, offspring)

    fittest = selection(children)
    best_schedule = fittest[0]


def initial_population(amount):
    """ Creates an intial population and returns the parents """

    # create empty list
    population = []
    scores = []

    for i in range(amount):
        # rara = random.random()
        # if rara < 0.5:
        #     print("0101010010001001011    [ generating initial population ]     101001000100100111")
        # else:
        #     print("1100101010000100001    [ generating initial population ]     000101010100010010")
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
        # rara = random.random()
        # if rara < 0.5:
        #     print("1010101010100010101    [ calculating fitness scores ]     101001101010001010")
        # else:
        #     print("0100101010101010101    [ calculating fitness scores ]     000101010100010101")

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

def mutation(schedule, chance):

    random = random.random()

    if random < chance:
        course1,
        activity1,
        course2,
        activity2,
        schedule = swapCourse(chambers, allcourses, student_list, schedule)




def cross_over(mating_pool, offspring):
    """ Creates offspring by exchanging genes from mating pool """

    # create empty list for children
    children = []

    # iterate over offspring
    for i in range(offspring):
        # create an empty schedule
        schedule = createEmptySchedule()
        placed_courses = []
        activities = 125


        # get a mother and father from the mating pool
        parents = []
        mother = mating_pool[random.randint(0, len(mating_pool) - 1)]
        father = mating_pool[random.randint(0, len(mating_pool) - 1)]
        parents.append(mother)
        parents.append(father)

        while activities > 0:
            # rara = random.random()
            # if rara < 0.5:
            #     print("0101010101010010010   [ placing courses in schedule ]     101001010100010101")
            # else:
            #     print("0011110101010010101   [ placing courses in schedule ]     010100101000101000")

            if activities % 2 == 0:
                parent_schedule = mother[1]  # >>> [[allcourses, chambers, studentlist], schedule]
            else:
                parent_schedule = father[1]

            random_course = random.randint(0, len(parent_schedule) - 1)


            # check if roomlock is free
            while parent_schedule[random_course] is None:
                random_course = random.randint(0, len(parent_schedule) - 1)
            while schedule[random_course] is not None:
                random_course = random.randint(0, len(parent_schedule) - 1)

            courses = []

            for key, value in schedule.items():
                courses.append(value)

            while parent_schedule[random_course] in courses:
                random_course = random.randint(0, len(parent_schedule) - 1)

            schedule[random_course] = parent_schedule[random_course]

            activities -= 1

        children.append(schedule)

    return children

initial = initial_population(10)

selectie = selection(initial)

cross_over(selectie, 1)

student = initial[0][0][1][0]

print(student.show_schedule())
