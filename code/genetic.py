# import main
import csv
import re
# from main import create_schedule
from scorefunction import calc_score
from generateschedule import create_empty_schedule, create_schedule
import random
from hillclimber import swapCourse, hillclimb_roomlocks
from generateschedule import updateClassesFromSchedule
from hillclimberscheduleplaces import swapCourse2, hillclimb_roomlocks2

total_gen_scores = {}

def genetic(initial, survival_rate, offspring, generations, mutation):
    """ Implements a genetic algorithm on the scheduling problem """

    # creates initial population
    print("Creating initial population...")
    genesis = initial_population(initial)

    # selects fittest individuals
    print("Selecting fittest individuals...")
    fittest = selection(genesis, survival_rate)

    # performs cross over
    print("Mating :)))))))")
    children = cross_over(fittest, offspring, 0, mutation)

    # for amount of generations
    for i in range(generations):

        # select fittest children (that survived)
        fittest = selection(children, survival_rate)

        # perform cross over, add mutation
        children = cross_over(fittest, offspring, i + 1, mutation)
        # print("fittest: ", calc_score(fittest[0][0][0], fittest[0][0][1], fittest[0][0][2]))

    # select fittest children
    fittest = selection(children, survival_rate)

    # extracting varibles best schedule
    allcourses = fittest[0][0][0]
    chambers = fittest[0][0][2]
    student_list = fittest[0][0][1]
    schedule = fittest[0][1]

    # calculate score 
    fittest_score = calc_score(allcourses, student_list, chambers)
    print("fittest: ", fittest_score)
    print("schedule: ", schedule)
    print("Start hillclimbing on fittest schedule...")

    # write scores in txt file
    score_file = open('scores.txt', 'w')
    score_file.write(str(total_gen_scores))

    # swap between roomlocks using a hillclimber
    hillclimb_roomlocks2(1000, chambers, allcourses, student_list, schedule)

    # if algorithm == "GA":
    #     return fittest, fittest_score, initial, survival_rate, offspring, generations, mutation

    # print("fittest: ", calc_score(fittest[0][0][0], fittest[0][0][1], fittest[0][0][2]))


def initial_population(amount):
    """ Creates an intial population and returns the parents """

    population = []
    scores = []

    for i in range(amount):

        # print("Generating initial population...")

        timetable_info = []
        score_info = []

        # create a new random schedule
        chambers, allcourses, student_list, schedule = create_schedule()

        # print("Hillclimbing on schedule {}...".format(i))
        # hillclimb_roomlocks2(20, chambers, allcourses, student_list, schedule)

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

        return calc_score(timetable_info[0][0],
                         timetable_info[0][1],
                         timetable_info[0][2])

    # choose the fittest individuals
    population = sorted(population, key=fitness, reverse=True)

    # set max and range
    probability = int(rate * len(population))
    rate = int(rate * 100)

    for i in range(rate):

        # fittest schedules have highest probabilities
        scores.append(calc_score(population[i][0][0], population[i][0][1], population[i][0][2]))
        mating_pool.append(population[i])

    # iterate over parents
    # for i in range(rate):
    #
    #     # create matingpool
    #     for j in range(probability):
    #
    #         # fittest schedules have highest probabilities
    #         scores.append(calc_score(population[i][0][0], population[i][0][1], population[i][0][2]))
    #         mating_pool.append(population[i])
    #
    #     # decrease probability
    #     probability -= 1

    return mating_pool


def mutation(schedule, chambers, allcourses, student_list, chance):
    """ Creates a mutation by performing a hillclimber for roomlocks """

    # determine probability
    probability = random.random()

    # if probability is smaller than given chance
    if probability < chance:

        # swap between roomlocks using hillclimber
        hillclimb_roomlocks2(int(probability * 100), chambers, allcourses, student_list, schedule)

    return



def cross_over(mating_pool, offspring, generation, chance):
    """ Creates offspring by exchanging genes from mating pool """

    # create empty list for children
    children = []
    fittest_score = 0
    chance_array = []
    gen_scores = []

    # determine probability
    probability = len(mating_pool)

    # iterate over mating pool
    for i in range(len(mating_pool)):

        # iterate over probability
        for j in range(probability):

            # append iteration
            chance_array.append(i)

        # decrease probability
        probability -= 1

    # set fittest_score
    fittest_score = 0

    # iterate over offspring
    for i in range(offspring):

        # create an empty schedule
        schedule = create_empty_schedule()

        # amount of activites that have to be scheduled
        activities = 125

        # choose a mother and father from the mating pool
        parents = []
        parents = mating_pool
        random_parent = chance_array[random.randint(0, len(chance_array) - 1)]
        parent_schedule = parents[random_parent][1]
        
        # until no activities are left
        while activities > 0:

            # print("Applying crossover between parents...")

            # if activities % 2 == 0:
            #     parent_schedule = parents[0][1]  # >>> [[allcourses, chambers, studentlist], schedule]
            # else:
            #     parent_schedule = parents[1][1]

            # choose random course from parent schedule
            random_course = random.randint(0, len(parent_schedule) - 1)

            # create empty course list
            courses = []

            # iterate over values in schedule
            for key, value in schedule.items():

                # if roomlock is not empty
                if value is not None:

                    # add to course list
                    courses.append(value)

            # initialize counters
            counter = 0
            newparentcounter = 0

            # if schedule has no place for the random course, a None value is chosen, or the random course is already chosen
            while schedule[random_course] is not None or parent_schedule[random_course] is None or parent_schedule[random_course] in courses:
                
                # choose new random course from parent schedule
                random_course = random.randint(0, len(parent_schedule) - 1)

                # increase counter
                counter += 1
        
                # if random course still not scheduled
                if counter > 100:

                    # choose new parent
                    parent_schedule = parents[random.randint(0, len(parents) - 1)][1]
                    
                    # reset counter
                    counter = 0

                    # increase parent-counter
                    newparentcounter += 1

                    # if 500 new parents weren't enough
                    if newparentcounter > 500:
                        break

            # schedule random course on same place as parent
            schedule[random_course] = parent_schedule[random_course]

            # decrease activities
            activities -= 1

        # update classes from schedule
        allcourses, student_list, chambers = update_classes_from_schedule(schedule)

        # create new arrays schedule properties
        timetable_info = []
        score_info = []

        # add all information about this specific schedule
        score_info.append(allcourses)
        score_info.append(student_list)
        score_info.append(chambers)

        # perform mutatation if chance is higher than probability
        mutation(schedule, chambers, allcourses, student_list, chance)

        # add individual schedule-info to timetable array
        timetable_info.append(score_info)
        timetable_info.append(schedule)

        # calculate score
        score = calc_score(allcourses, student_list, chambers)

        # add to score file
        gen_scores.append(score)

        # if score is better than the fittest
        if score > fittest_score:

            # adjust fittest score
            fittest_score = score
            
            print("New best found ---> Schedule: {}, generation: {}, score: {}".format(i, generation, score))

        # add the array with individual timetable-info to the population
        children.append(timetable_info)

    # create score dict
    total_gen_scores[generation] = gen_scores

    return children
