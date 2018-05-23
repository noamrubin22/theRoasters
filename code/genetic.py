from generateschedule import createSchedule

def initial_population(amount):
    """ Creates an intial population and returns the parents """

    # create empty list 
    population = []
    parents = []

    # set maximum parents
    parents_max = 10

    for i in range(amount):

        timetable_info_info = []
        score_info = []

        # create a new random schedule
        createSchedule()

        # add all information about this specific schedule to an array
        score_info.append(allcourses, student_list, chambers)

        # add scorinformation and schedule 
        timetable_info.append(score_info)
        timetable_info.append(schedule)

        # add the array of information about this schedule to the timetable_info array
        population.append(timetable_info)

    return timetable_info

def selection(timetable_info):
    """ Calculates the fitness of an individual by returning the schedule score """

    # calculates the fitness of an individual 
    calcScore(timetable_info[0])

    # sort the population array by score
    population = sorted(population, key=fitness_score, reverse=True)

    for i in range(parents_max):

        # choose the fittest individuals 
        parents.append(population[i])  # now only top 10, later have the amount of schedules pushed be based on score
  
    return parents


def cross_over(parents, new_population):
    """ Creates offspring by exchanging the genes of parents among themselves """


    createSchedule()

    # choose random parent 
    random_parent = random.randint(0, len(parents))

    # choose random roomlock
    pickroomlock = random.randint(0, 139)

    # until new population does not exist
    while new_population > 0:

        # choose random parent
        parent = [random.randint(0, len(parents))]
        pickroomlock = random.randint(0, 139)

        ...

        # decrease amount new population
        new_population -= 1
