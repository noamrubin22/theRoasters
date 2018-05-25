
input = [(scores, type), (scores, type), (scores, type), (scores, type)]


# perform geman
chambers, allcourses, student_list, schedule = createSchedule()
best_score, best_courses, best_student_list, best_chambers, scores = simulatedAnnealing(geman, 100000, chambers, allcourses, student_list, schedule)
plot_simulated_annealing(scores, geman)

input.append(scores, geman)

chambers, allcourses, student_list, schedule = createSchedule()
best_score, best_courses, best_student_list, best_chambers, scores = simulatedAnnealing(linear, 100000, chambers, allcourses, student_list, schedule)
plot_simulated_annealing(scores, linear)

input.append(scores, linear)

chambers, allcourses, student_list, schedule = createSchedule()
best_score, best_courses, best_student_list, best_chambers, scores = simulatedAnnealing(sigmoidal, 100000, chambers, allcourses, student_list, schedule)

input.append(scores, sigmoidal)

chambers, allcourses, student_list, schedule = createSchedule()
best_score, best_courses, best_student_list, best_chambers, scores = simulatedAnnealing(exponential, 100000, chambers, allcourses, student_list, schedule)
plot_simulated_annealing(scores, geman)
input.append(scores, exponential)