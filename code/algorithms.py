import helpers 
from helpers import *

def hillclimbStudent(times, chambers, allcourses, student_list, schedule):
	""" Performs student swap and changes back if it does not lead to a better score """
	
	# perform swap a given number of times
	for i in range(0, times):
		
		# calculate score before swap
		points = calcScore(allcourses, student_list, chambers)

		# perform swap (and save what has been swapped)
		swapcourse, sem1, sem2, prac1, prac2, student1, student2 = swapStudents(chambers, allcourses, student_list, schedule)
		
		# calculate score after swap
		newpoints = calcScore(allcourses, student_list, chambers)
		
		# swap back if new score is not better
		if newpoints < points:
			
			swapStudents(chambers, allcourses, student_list, schedule, swapcourse, sem2, sem1, prac2, prac1, student2, student1)
			
			# calculate score after swap back
			newpoints = calcScore(allcourses, student_list, chambers)
			
			# stop algorithm if swapping back does not lead to original score
			if newpoints != points:
				break

	return newpoints

def hillclimbRoomlocks(times, chambers, allcourses, student_list, schedule):
	""" Searches for the optimal score by swapping roomlocks """

	# amount of steps hillclimber
	for i in range(0, times):

		# calculate score before swap
		points = calcScore(allcourses, student_list, chambers)

		# perform swap
		course1, activity1, course2, activity2, schedule = swapCourse(chambers, allcourses, student_list, schedule)

		# calculate new scores
		newpoints = calcScore(allcourses, student_list, chambers)

		# if new score lower than old score
		if newpoints < points:

			# swap back
			swapCourse(chambers, allcourses, student_list, schedule, course1, activity1, course2, activity2)

			# calculate new score
			newpoints = calcScore(allcourses, student_list, chambers)

			# if back-swap didn't go well
			if points != newpoints:

				# print courses and break loop
				print(course2, course1)
				print("ERROR")
				break

	return newpoints

def simulatedAnnealing(coolingscheme, min_iterations, chambers, allcourses, student_list, schedule):
	""" Searches for the optimal score by using a coolingscheme """

	# placeholders
	best_score = None
	best_course = None
	best_student_list = None
	best_chambers = None

	# initialize temperatures
	temp_start = 10

	# array for scores (visualization)
	scores = []

	# set start temperature 
	temperature = temp_start

	# loop until system has cooled
	for i in range(min_iterations):

		# calculate score schedule
		points = calcScore(allcourses, student_list, chambers)

		# append score to list for visualisation
		scores.append(points)

		# keep track of the best score and its variables
		if best_score == None or points > best_score: 
			best_score = points
			best_courses = allcourses
			best_student_list = student_list
			best_chambers = chambers

		# pick random neighbour by swapping 
		course1, activity1, course2, activity2, schedule = swapCourse(chambers, allcourses, student_list, schedule)

		# calculate new score
		newpoints = calcScore(allcourses, student_list, chambers)
		
		# if new score is worst 
		if newpoints < points:

			# calculate acceptance chance
			acceptance_probability = math.exp((newpoints - points) /temperature)

			# if acceptance chance higher than random number
			if (acceptance_probability > random.random()):
			
				# accept the worst solution
				points = newpoints

				# cool system
				temperature = coolingscheme(min_iterations, i)

			# if acceptance chance lower than random number
			else:

				# swap back
				swapCourse(chambers, allcourses, student_list, schedule, course1, activity1, course2, activity2)

				# calculate new score and print
				newpoints = calcScore(allcourses, student_list, chambers)

				# if back-swap didn't go well 
				if points != newpoints:

					# print coursenames and break loop
					print(course2, course1)
					print("ERROR")
					break

				# continue with previous score
				points = newpoints

		# if new score is better
		else: 

			# accept it
			points = newpoints 
			# print("accepted score:" )


	print("bestscore:", best_score)


	return best_score, best_courses, best_student_list, best_chambers, scores

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