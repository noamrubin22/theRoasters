import main
import csv
from main import prepareData, complementCourse
from scorefunction import calcScore

def initial_population(amount):

    population = []
    parents = []
    parents_max = 10
    scores = []

    for i in range(amount):
        timetable = []
        score_info = []

        # create a new random schedule
        chambers, allcourses, student_list, schedule = prepareData()
        complementCourse(allcourses, schedule, chambers, student_list)

        # add all information about this specific schedule to an array
        score_info.append(allcourses)
        score_info.append(student_list)
        score_info.append(chambers)


        timetable.append(score_info)
        timetable.append(schedule)

        # add the array of information about this schedule to the timetable array
        population.append(timetable)


    def points_score(timetable):
        return calcScore(timetable[0][0], timetable[0][1], timetable[0][2])

    # sort the population array by score
    population = sorted(population, key=points_score, reverse=True)

    # print(calcScore(population[0][0][0], population[0][0][1], population[0][0][2]))

    for i in range(parents_max):
        scores.append(calcScore(population[i][0][0], population[i][0][1], population[i][0][2]))
        parents.append(population[i])

    # now only top 10, later have the amount of schedules pushed be based on score
    return scores # parents <<< uncomment either a) scores or b) parents to return a) top 10 scores b) top 10 schedules

print("Initial population: ", initial_population(1000))

# def cross_over(parents, new_population):
#
#     parents = initial_population(10)
#     chambers, allcourses, student_list, schedule = prepareData()
#
#
#     random_parent = random.randint(0, len(parents))
#     pickroomlock = random.randint(0, 139)
#
#     while new_population > 0:
#
#         parent = [random.randint(0, len(parents))]
#         pickroomlock = random.randint(0, 139)
#
#         ...
#
#         new_population -= 1
