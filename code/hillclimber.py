###################################################
# Heuristieken: Lectures & Lesroosters			  #
#												  #
# Names: Tessa Ridderikhof, Najib el Moussaoui 	  #
# 		 & Noam Rubin							  #
#												  #
# This code searchs for the optimal schedulescore #
# using a hillclimber algorithm where the only    #
# swaps being accepted are the ones that increase #
# the score 									  #
#												  #
###################################################

import main
import scorefunction
import random
# import hillclimberstudents
import csv
import generateschedule
from generateschedule import translateRoomlock
from scorefunction import calcScore
from main import createSchedule
from hillclimberstudents import hillclimbStudent

# chambers = main.chambers
# allcourses = main.allcourses
# student_list = main.student_list
# schedule = main.schedule

chambers, allcourses, student_list, schedule = createSchedule()

def swapCourse(course1 = None, activity1 = None, course2 = None, activity2 = None):
	""" """

	#* swap roomlock 2 (random) courses *#

	# if specific course is not chosen
	if course1 == None:

		# choose random course from courselist
		course1 = random.randint(0, len(allcourses) - 1)
		
	# same
	if course2 == None:
		course2 = random.randint(0, len(allcourses) - 1)


	# if specific activity is not chosen
	if activity1 == None:

		# chose random activity from course
		activity1 = random.randint(0, len(allcourses[course1].activities) - 1)

	
	# same
	if activity2 == None:
		activity2 = random.randint(0, len(allcourses[course2].activities) - 1)


	# store random activities
	randact1 = allcourses[course1].activities[activity1]
	randact2 = allcourses[course2].activities[activity2]

	
	# store roomlocks
	roomlock1 = randact1[0]
	roomlock2 = randact2[0]


	# swap the chosen activities from roomlock in schedule
	allcourses[course1].changeSchedule(roomlock2, activity1)
	allcourses[course2].changeSchedule(roomlock1, activity2)


	# translate to room and timelock for both roomlocks
	room1, timelock1 = translateRoomlock(roomlock1)
	room2, timelock2 = translateRoomlock(roomlock2)


	# store activity-groups 
	coursegroup1 = allcourses[course1].activities[activity1][2]
	coursegroup2 = allcourses[course2].activities[activity2][2]

	
	#* change schedule of individual students*# 

	
	# if first coursegroup has only one group (lecture)
	if coursegroup1 == 0:

		# for each student
		for student in student_list:

			# that follows the course
			if allcourses[course1].name in student.courses:


				# change individual schedule
				student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

	# for seminars and practicals (group > 1)
	else:

		# for each student
		for student in student_list:

			# if student follows the course
			if allcourses[course1].name in student.courses:

				# if course has seminar
				if allcourses[course1].seminars > 0:

					# if student is in seminargroup
					if student.last_name in allcourses[course1].seminargroups[coursegroup1]:


						# change individual schedule with swapped course
						student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)
				
				# if course has practical
				elif allcourses[course1].practicals > 0:

					# if student is in practical-group
					if student.last_name in allcourses[course1].practicalgroups[coursegroup1]:

						# change individual schedule
						student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

	# same for the second coursegroup
	if coursegroup2 == 0:
		for student in student_list:
			if allcourses[course2].name in student.courses:
				student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)

	else:
		for student in student_list:
			if allcourses[course2].name in student.courses:
				if allcourses[course2].seminars > 0:
					if student.last_name in allcourses[course2].seminargroups[coursegroup2]:
						student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)
				elif allcourses[course2].practicals > 0:
					if student.last_name in allcourses[course2].practicalgroups[coursegroup2]:
						student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)

	#* update roomschedules *#

	chambers[room1].changeBooking(timelock1, timelock2)
	chambers[room2].changeBooking(timelock2, timelock1)

	# save content of schedule at swapped roomlocks
	schedulecontent1 = schedule[roomlock1]
	schedulecontent2 = schedule[roomlock2]


	# switch courses in schedule
	schedule[roomlock1] = schedulecontent2
	schedule[roomlock2] = schedulecontent1

	return course1, activity1, course2, activity2


def hillclimbRoomlocks(times):
	""" Searches for the optimal score by swapping roomlocks """

	# amount of steps hillclimber
	for i in range(0, times):

		# calculate score before swap
		points = calcScore(allcourses, student_list, chambers)

		# perform swap
		course1, activity1, course2, activity2 = swapCourse()

		# calculate new scores
		newpoints = calcScore(allcourses, student_list, chambers)

		# if new score lower than old score
		if newpoints < points:
			
			# swap back
			swapCourse(course1, activity1, course2, activity2)

			# calculate new score
			newpoints = calcScore(allcourses, student_list, chambers)

			# if back-swap didn't go well
			if points != newpoints:

				# print courses and break loop
				print(course2, course1)
				print("ERROR")
				break

	return newpoints

# print original score
originalscore = calcScore(allcourses, student_list, chambers)
print("Started with: ", originalscore)

# perform hillclimber for roomlocks
hillclimbRoomlocks(1000)

# show intermediate score
intermediate_score = calcScore(allcourses, student_list, chambers)
print("After roomlock hillclimber:", intermediate_score)

# perform hillclimber for students
hillclimbStudent(1000, chambers, allcourses, student_list, schedule)

# calculate and show final score 
endscore = calcScore(allcourses, student_list, chambers)

print("Final score:", endscore)

