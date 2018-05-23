# import main
import csv
# from main import createSchedule
from scorefunction import calcScore
<<<<<<< HEAD
from generateschedule import createEmptySchedule
=======
from printschedule import print_schedule
from generateschedule import createEmptySchedule, createSchedule
>>>>>>> aa2c9024ed0decb77b7ab0156431da0195817c84
import random


def initial_population(amount):
    """ Creates an intial population and returns the parents """

    # create empty list 
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

<<<<<<< HEAD
        # add the array with individual timetable-info to the population
=======
        # add the array with the indivudual timetable-info to the population
>>>>>>> aa2c9024ed0decb77b7ab0156431da0195817c84
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

<<<<<<< HEAD
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
=======
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
>>>>>>> aa2c9024ed0decb77b7ab0156431da0195817c84

        # decrease probability
        probability -= 1

    return mating_pool


<<<<<<< HEAD
def cross_over(mating_pool, amount_of_offspring):
    """ Creates amount_of_offspring from mating pool by exchanging genes """

    # create empty list for children
    children = []

    # amount of activities
    activities = 125

    for i in range(amount_of_offspring):

        # amount of activities
        activities = 125

        placed_courses = []
=======
def cross_over(mating_pool, offspring):
    """ Creates offspring by exchanging genes from mating pool """
    
    # create empty list for children
    children = []

    # iterate over offspring
    for i in range(offspring):
>>>>>>> aa2c9024ed0decb77b7ab0156431da0195817c84

        # create an empty schedule
        schedule = createEmptySchedule()
        placed_courses = []

        # get a mother and father from the mating pool
        parents = []
        mother = mating_pool[random.randint(0, len(mating_pool))]
        father = mating_pool[random.randint(0, len(mating_pool))]
        parents.append(mother)
        parents.append(father)

        while activities > 0:

            if activities % 2 == 0:
                parent_schedule = parents[0][1]  # >>> [[allcourses, chambers, studentlist], schedule]
            else:
                parent_schedule = parents[1][1]

            random_course = random.randint(0, len(parent_schedule) - 1)


            # check if roomlock is free
            while parent_schedule[random_course] is None:
                random_course = random.randint(0, len(parent_schedule) - 1)
            while schedule[random_course] is not None:
                random_course = random.randint(0, len(parent_schedule) - 1)

            placed = False
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

<<<<<<< HEAD
print("CHILD ===== ", cross_over(selectie, 1))
=======
    print(mother, father)



mating_pool = selection(initial_population(100))

cross_over(mating_pool)

>>>>>>> aa2c9024ed0decb77b7ab0156431da0195817c84
