import main
from main import translateRoomlock

def scorefunction(allcourses, student_list, chambers):

	# valid schedule has been made: 1000 points
	points = 1000;

	# subtract or add points based on schedule
	# loop through courses
	for course in allcourses:
		if course.seminars > 0:
			groups = list(range(1, course.seminars + 1))
		elif course.practicals > 0:
			groups = list(range(1, course.practicals + 1))
		else:
			groups = [1]

		dayActivity = {k: [] for k in groups}

		# loop trough activities of a course
		for activity in course.activities:
			day = int(activity[0]/28)
			if activity[2] == 0:
				if day in dayActivity[1]:
					points -= 10	
				for group in groups:	
					dayActivity[group].append(day)
			else:
				if day in dayActivity[activity[2]]:
					points -= 10
				dayActivity[activity[2]].append(day) 
		# print(course.name, dayActivity)

		for group in groups:
			if (len(dayActivity[group]) == 2):
				if (abs(dayActivity[group][0] - dayActivity[group][1]) >= 3):
					points += 20
			# if three activities in the week: mo-we-fr?
			if (len(dayActivity[group]) == 3):
				if 0 in dayActivity[group] and 2 in dayActivity[group] and 4 in dayActivity[group]:
					points += 20
			# if four activities in the week: mo-tu-th-fr?
			if (len(dayActivity[group]) == 4):
				if 0 in dayActivity[group] and 1 in dayActivity[group] and 3 in dayActivity[group] and 4 in dayActivity[group]:
					points += 20


		
	print(student_list[0].schedule)

	for student in student_list:
		timelocksStudent = []
		for activity in student.schedule:
			if activity[0] in timelocksStudent:
				points -= 1
			timelocksStudent.append(activity[0])

	for course in allcourses:
		for activity in course.activities:
			room, timelock = translateRoomlock(activity[0])
			if activity[2] == 0:
				if int(chambers[room].capacity) < course.students:
					print(chambers[room].capacity)
					print(course.students)
					print("te veel studenten: past niet in de zaal!")
					maluspoints = course.students - int(chambers[room].capacity)
					print(maluspoints)
					points -= maluspoints
			else:
				if course.seminars > 0:
					if int(chambers[room].capacity) < course.maxstudentssem:
						print(chambers[room].capacity)
						print(course.maxstudentssem)
						maluspoints = course.maxstudentssem - int(chambers[room].capacity)
						print(maluspoints)
						points -= maluspoints

	# laat eindscore zien (so far)
	print("Points: ", points)
	return points

scorefunction(main.allcourses, main.student_list, main.chambers)