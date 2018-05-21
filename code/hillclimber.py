import main
import scorefunction
import random
import hillclimberstudents
from main import translateRoomlock
from scorefunction import calcScore
from hillclimberstudents import hillclimbStudent

allcourses = main.allcourses
student_list = main.student_list
chambers = main.chambers
schedule = main.schedule

def swapcourse(course1 = None, activity1 = None, course2 = None, activity2 = None):

	if course1 == None:
		course1 = random.randint(0, len(allcourses) - 1)
		

	if course2 == None:
		course2 = random.randint(0, len(allcourses) - 1)


	if activity1 == None:
		activity1 = random.randint(0, len(allcourses[course1].activities) - 1)
	
	if activity2 == None:
		activity2 = random.randint(0, len(allcourses[course2].activities) - 1)

	randact1 = allcourses[course1].activities[activity1]
	randact2 = allcourses[course2].activities[activity2]
	roomlock1 = randact1[0]
	roomlock2 = randact2[0]

	allcourses[course1].changeSchedule(roomlock2, activity1)
	allcourses[course2].changeSchedule(roomlock1, activity2)

	room1, timelock1 = translateRoomlock(roomlock1)
	room2, timelock2 = translateRoomlock(roomlock2)

	coursegroup1 = allcourses[course1].activities[activity1][2]
	coursegroup2 = allcourses[course2].activities[activity2][2]


	
	if coursegroup1 == 0:
		for student in student_list:
			if allcourses[course1].name in student.courses:
				student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

	else:
		for student in student_list:
			if allcourses[course1].name in student.courses:
				if allcourses[course1].seminars > 0:
					if student.last_name in allcourses[course1].seminargroups[coursegroup1]:
						student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)
				elif allcourses[course1].practicals > 0:
					if student.last_name in allcourses[course1].practicalgroups[coursegroup1]:
						student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)


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
	for i in range(0, times):
		points = calcScore(allcourses, student_list, chambers)
		# print("Voor swap: ", points)
		course1, activity1, course2, activity2 = swapcourse()
		newpoints = calcScore(allcourses, student_list, chambers)
		# print("   Nieuwe score: ", newpoints)
		if newpoints < points:
			swapcourse(course1, activity1, course2, activity2)
			newpoints = calcScore(allcourses, student_list, chambers)
			# print("      Back to normal?: ", newpoints)
			if points != newpoints:
				print(course2, course1)
				print("ERROR")
				break

originalscore = calcScore(allcourses, student_list, chambers)
print("Begonnen met: ", originalscore)

hillclimbRoomlocks(1000)

tussenscore = calcScore(allcourses, student_list, chambers)
print("Na roomlock hillclimber", tussenscore)

hillclimbStudent(1000)

endscore = calcScore(allcourses, student_list, chambers)
print("Echte eindscore", endscore)
