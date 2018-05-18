import main
import scorefunction
import random
from main import translateRoomlock
from scorefunction import calcScore

allcourses = main.allcourses
student_list = main.student_list
chambers = main.chambers

def swapcourse(allcourses, student_list, chambers):

	allcourses_beforeswap = allcourses
	student_list_beforeswap = student_list
	chambers_beforeswap = chambers

	points = calcScore(allcourses, student_list, chambers)
	print("Voor swap: ", points)


	course1 = random.randint(0, len(allcourses) - 1)
	course2 = random.randint(0, len(allcourses) - 1)

	while len(allcourses[course1].activities) == 0 or not allcourses[course1].activities:
		course1 = random.randint(0, len(allcourses))

	while len(allcourses[course2].activities) == 0 or not allcourses[course2].activities:
		course2 = random.randint(0, len(allcourses))

	activity1 = random.randint(0, len(allcourses[course1].activities) - 1)
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


	# if coursegroup1 == 0:
	# 	for student in student_list:
	# 		if allcourses[course1].name in student.courses:
	# 			student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

	# else:
	# 	for student in main.student_list:
	# 		if allcourses[course1].name in student.courses:
	# 			if allcourses[course1].seminars > 0:
	# 				if student.last_name in allcourses[course1].seminargroups[coursegroup1]:
	# 					student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)
	# 			elif allcourses[course1].practicals > 0:
	# 				if student.last_name in allcourses[course1].practicalgroups[coursegroup1]:
	# 					student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

	# if coursegroup2 == 0:
	# 	for student in student_list:
	# 		if allcourses[course2].name in student.courses:
	# 			student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)

	# else:
	# 	for student in main.student_list:
	# 		if allcourses[course2].name in student.courses:
	# 			if allcourses[course2].seminars > 0:
	# 				if student.last_name in allcourses[course2].seminargroups[coursegroup2]:
	# 					student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)
	# 			elif allcourses[course2].practicals > 0:
	# 				if student.last_name in allcourses[course2].practicalgroups[coursegroup2]:
	# 					student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)


	chambers[room1].changeBooking(timelock1, timelock2)
	chambers[room2].changeBooking(timelock2, timelock1)

	newpoints = calcScore(allcourses, student_list, chambers)
	print("   Nieuwe score: ", newpoints)

	if newpoints > points:
		return newpoints
	else:

		allcourses[course1].changeSchedule(roomlock1, activity1)
		allcourses[course2].changeSchedule(roomlock2, activity2)
		main.chambers[room1].changeBooking(timelock2, timelock1)
		main.chambers[room2].changeBooking(timelock1, timelock2)

		newpoints = calcScore(allcourses, student_list, chambers)
		print("      Back to normal?: ", newpoints)
		if newpoints != points:
			print("ERRORR                               ERROR")
			print(allcourses[course1].name, allcourses[course2].name)
			print(timelock1, timelock2)

		return newpoints


for i in range(0, 10000):
	newpoints = swapcourse(allcourses, student_list, chambers)

print("Eindscore: ", newpoints)