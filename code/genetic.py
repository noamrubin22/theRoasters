def initial_population(amount):

    population = []
    parents = []
    parents_max = 10

    for i in range(amount):
        timetable = []
        score_info = []

        # create a new random schedule
        chambers, allcourses, student_list, schedule = prepareData()
        complementCourse(allcourses, schedule, chambers, student_list)

        # add all information about this specific schedule to an array
        score_info.append(allcourses, student_list, chambers)

        timetable.append(score_info)
        timetable.append(schedule)

        # add the array of information about this schedule to the timetable array
        population.append(timetable)

    def points_score(timetable):
        return calcScore(timetable[0])

    # sort the population array by score
    population = sorted(population, key=points_score, reverse=True)

    for i in range(parents_max):
        parents.append(population[i])

    # now only top 10, later have the amount of schedules pushed be based on score
    return parents


def cross_over(parents, new_population):

    chambers, allcourses, student_list, schedule = prepareData()

    random_parent = random.randint(0, len(parents))
    pickroomlock = random.randint(0, 139)

    while new_population > 0:

        parent = [random.randint(0, len(parents))]
        pickroomlock = random.randint(0, 139)

        ...

        new_population -= 1
