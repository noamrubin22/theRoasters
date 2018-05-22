# import main
import scorefunction
import random
import csv
from generateschedule import translateRoomlock
from scorefunction import calcScore
# from main import createSchedule

# chambers = main.chambers
# allcourses = main.allcourses
# student_list = main.student_list
# schedule = main.schedule


def swapStudents(chambers, allcourses, student_list, schedule, swapcourse = None, sem1 = None, sem2 = None, prac1 = None, prac2 = None, student1 = None, student2 = None):
	if swapcourse == None:
		# pick course to swap students in
		swapcourse = random.randint(0, len(allcourses) - 1)

		# pick new course if the course has not enough seminargroups or practicalgroups
		while allcourses[swapcourse].seminars < 2 and allcourses[swapcourse].practicals < 2:
			swapcourse = random.randint(0, len(allcourses) - 1)

	# swap students if course has seminars
	if allcourses[swapcourse].seminars > 1:
		if sem1 == None and sem2 == None:

			# pick two seminarsgroups to swap students in
			sem1 = random.randint(1, allcourses[swapcourse].seminars)
			sem2 = random.randint(1, allcourses[swapcourse].seminars)

			# pick new seminargroups if the same groups have been chosen
			while sem1 == sem2:
				sem1 = random.randint(1, allcourses[swapcourse].seminars)
				sem2 = random.randint(1, allcourses[swapcourse].seminars)

		# save names of students in seminargroups 1 and 2
		seminargroup1 = allcourses[swapcourse].seminargroups[sem1]
		seminargroup2 = allcourses[swapcourse].seminargroups[sem2]

		if student1 == None or student2 == None:
			# pick random student from seminargroup
			student1 = random.randint(0, len(seminargroup1) - 1)
			student2 = random.randint(0, len(seminargroup2) - 1)

		# swap students in seminargroups in course-class
		allcourses[swapcourse].switchSeminarStudent(sem1, sem2, student1, student2)

		# determine timelocks of activities
		for activity in allcourses[swapcourse].activities:
			if activity[2] == sem1 and 'seminar' in activity[1]:
				roomlock1 = activity[0]
				room1, timelock1 = translateRoomlock(roomlock1)
			if activity[2] == sem2 and 'seminar' in activity[1]:
				roomlock2 = activity[0]
				room2, timelock2 = translateRoomlock(roomlock2)

		# update student schedule
		for student in student_list:
			if student.last_name == allcourses[swapcourse].seminargroups[sem1][student1]:
				student.changeStudentSchedule(timelock2, timelock1, allcourses[swapcourse].name)
			if student.last_name == allcourses[swapcourse].seminargroups[sem2][student2]:
				student.changeStudentSchedule(timelock1, timelock2, allcourses[swapcourse].name)

		return swapcourse, sem1, sem2, prac1, prac2, student1, student2

	if allcourses[swapcourse].practicals > 1:
		if prac1 == None and prac2 == None:

			# pick two seminarsgroups to swap students in
			prac1 = random.randint(1, allcourses[swapcourse].practicals)
			prac2 = random.randint(1, allcourses[swapcourse].practicals)

			# pick new seminargroups if the same groups have been chosen
			while prac1 == prac2:
				prac1 = random.randint(1, allcourses[swapcourse].practicals)
				prac2 = random.randint(1, allcourses[swapcourse].practicals)

		# save names of students in seminargroups 1 and 2
		practicalgroup1 = allcourses[swapcourse].practicalgroups[prac1]
		practicalgroup2 = allcourses[swapcourse].practicalgroups[prac2]

		if student1 == None or student2 == None:
			# pick random student from seminargroup
			student1 = random.randint(0, len(practicalgroup1) - 1)
			student2 = random.randint(0, len(practicalgroup2) - 1)

		# swap students in seminargroups in course-class
		allcourses[swapcourse].switchPracticalStudent(prac1, prac2, student1, student2)

		# determine timelocks of activities
		for activity in allcourses[swapcourse].activities:
			if activity[2] == prac1 and 'practical' in activity[1]:
				roomlock1 = activity[0]
				room1, timelock1 = translateRoomlock(roomlock1)
			if activity[2] == prac2 and 'practical' in activity[1]:
				roomlock2 = activity[0]
				room2, timelock2 = translateRoomlock(roomlock2)

		# update student schedule
		for student in student_list:
			if student.last_name == allcourses[swapcourse].practicalgroups[prac1][student1]:
				student.changeStudentSchedule(timelock2, timelock1, allcourses[swapcourse].name)
			if student.last_name == allcourses[swapcourse].practicalgroups[prac2][student2]:
				student.changeStudentSchedule(timelock1, timelock2, allcourses[swapcourse].name)

		return swapcourse, sem1, sem2, prac1, prac2, student1, student2

# studentswapscores = []
# points = calcScore(allcourses, student_list, chambers)
# studentswapscores.append(points)

def hillclimbStudent(times, chambers, allcourses, student_list, schedule):
	for i in range(0, times):
		points = calcScore(allcourses, student_list, chambers)
		swapcourse, sem1, sem2, prac1, prac2, student1, student2 = swapStudents(chambers, allcourses, student_list, schedule)
		newpoints = calcScore(allcourses, student_list, chambers)
		if newpoints < points:
			swapStudents(chambers, allcourses, student_list, schedule, swapcourse, sem2, sem1, prac2, prac1, student2, student1)
			newpoints = calcScore(allcourses, student_list, chambers)
			if newpoints != points:
				break



