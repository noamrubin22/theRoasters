import main
import scorefunction
import random
from main import translateRoomlock
from scorefunction import calcScore

allcourses = main.allcourses
student_list = main.student_list
chambers = main.chambers
schedule = main.schedule

def swapcourse(course1 = None, activity1 = None, course2 = None, activity2 = None):

	if course1 == None:
		course1 = random.randint(0, len(allcourses) - 1)
		
		while len(allcourses[course1].activities) == 0 or not allcourses[course1].activities:
			course1 = random.randint(0, len(allcourses))

	if course2 == None:
		course2 = random.randint(0, len(allcourses) - 1)

		while len(allcourses[course2].activities) == 0 or not allcourses[course2].activities:
			course2 = random.randint(0, len(allcourses))

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

	originalcounter = 0
	
	if coursegroup1 == 0:
		for student in student_list:
			if allcourses[course1].name in student.courses:
				originalcounter += 1
				student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

	else:
		for student in student_list:
			if allcourses[course1].name in student.courses:
				if allcourses[course1].seminars > 0:
					if student.last_name in allcourses[course1].seminargroups[coursegroup1]:
						originalcounter += 1
						student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)
				elif allcourses[course1].practicals > 0:
					if student.last_name in allcourses[course1].practicalgroups[coursegroup1]:
						originalcounter += 1
						student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

	studentcounter = 0

	if coursegroup2 == 0:
		for student in student_list:
			if allcourses[course2].name in student.courses:
				studentcounter += 1
				student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)


	else:
		for student in student_list:
			if allcourses[course2].name in student.courses:
				if allcourses[course2].seminars > 0:
					if student.last_name in allcourses[course2].seminargroups[coursegroup2]:
						studentcounter += 1
						student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)
				elif allcourses[course2].practicals > 0:
					if student.last_name in allcourses[course2].practicalgroups[coursegroup2]:
						studentcounter += 1
						student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)




	chambers[room1].changeBooking(timelock1, timelock2)
	chambers[room2].changeBooking(timelock2, timelock1)
	print(allcourses[course1].students, allcourses[course2].students)
	print(originalcounter, studentcounter)

	return course1, activity1, course2, activity2


for i in range(0, 1000):
	points = calcScore(allcourses, student_list, chambers)
	print("Voor swap: ", points)
	course1, activity1, course2, activity2 = swapcourse()
	newpoints = calcScore(allcourses, student_list, chambers)
	print("   Nieuwe score: ", newpoints)
	if newpoints < points:
		swapcourse(course1, activity1, course2, activity2)
		newpoints = calcScore(allcourses, student_list, chambers)
		print("      Back to normal?: ", newpoints)
		if points != newpoints:
			print(course2, course1)
			print("ERROR")
			break

print("Eindscore: ", newpoints)

print(student_list[3].schedule)

for activity in student_list[3].schedule:
	swap1 = activity[0]

swap1 = student_list[3].schedule[0][0]
print(swap1)

student_list[3].changeStudentSchedule(swap1, 16, "Architectuur en computerorganisatie")

print(student_list[3].schedule)