import csv
import matplotlib.pyplot as plt
from generateschedule import createSchedule
from SA import simulatedAnnealing

# create random schedule
chambers, allcourses, student_list, schedule = createSchedule()

temperature = 10000
coolingRate = 0.02

# perform simulated annealing, store scores
best_score, best_courses, best_student_list, best_chambers, scores = simulatedAnnealing(temperature, coolingRate, chambers, allcourses, student_list, schedule)

# plot scores
plt.plot(range(0, len(scores)), scores)
plt.ylabel("Score")
plt.title("Simulated annealing")
plt.text(1000, 0.025, "Temperature: 1000, Coolingrate = 0.02")
plt.show()