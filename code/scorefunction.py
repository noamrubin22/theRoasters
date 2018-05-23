import generateschedule
from generateschedule import translateRoomlock


def calcScore(allcourses, student_list, chambers):
	""" Calculates the score of a schedule"""

	# start-score of a valid schedule
	points = 1000;
	roomlocks_per_day = 28;

	#* create groups and dict to keep up the days per activity *#

	# iterate over courses
	for course in allcourses:

		# if seminar(s) exist
		if course.seminars > 0:

			# create list with amount of seminar-groups
			groups = list(range(1, course.seminars + 1))

		# if practical exist
		elif course.practicals > 0:

			# create list with amount of practical-groups
			groups = list(range(1, course.practicals + 1))

		# otherwise only one group (lecture)
		else:
			groups = [1]

		# create dict with groupnumber as key, [days] as values
		dayActivity = {k: [] for k in groups}


		#* subtract points based on activities per day *#

		# iterate over activities per course
		for activity in course.activities:

			# determine day
			day = int(activity[0] / roomlocks_per_day)

			# if activity = lecture
			if activity[2] == 0:

				# substract points when on the same day
				if day in dayActivity[1]:
					points -= 10

				# add day to list linked to lecture
				for group in groups:
					dayActivity[group].append(day)

			# for seminars
			elif activity[2] == 1:

				# substract points when on the same day
				if day in dayActivity[activity[2]]:
					points -= 10

				# add day to list linked to group
				dayActivity[activity[2]].append(day)

			# for practicals
			else:

				# substract points when on the same day
				if day in dayActivity[activity[2]]:
					points -= 10

				# add day to list linked to group
				dayActivity[activity[2]].append(day)
		# print(course.name, dayActivity)


		#* add points for spreading of activities over week *#

		# iterate over groups
		for group in groups:

			# when 2 activities in week
			if (len(dayActivity[group]) == 2):

				# add points if they are spread (mo- thu, mo-fri)
				if (abs(dayActivity[group][0] - dayActivity[group][1]) >= 3):
					points += 20

			# when 3 activities in the week
			if (len(dayActivity[group]) == 3):

				# add points if spread (mo-we-fr)
				if 0 in dayActivity[group] and 2 in dayActivity[group] and 4 in dayActivity[group]:
					points += 20

			# if 4 activities in the week
			if (len(dayActivity[group]) == 4):

				# add points if spread  (mo-tu-th-fr)
				if 0 in dayActivity[group] and 1 in dayActivity[group] and 3 in dayActivity[group] and 4 in dayActivity[group]:
					points += 20


	# for all students
	for student in student_list:

		# create empty list
		timelocksStudent = []

		# for each activity in schedule
		for activity in student.schedule:

			# if roomlock is occupied substract points
			if activity[0] in timelocksStudent:
				points -= 1

			# add roomlock to list
			timelocksStudent.append(activity[0])

	# for all courses
	for course in allcourses:

		# and activities
		for activity in course.activities:

			# substract room and timelock
			room, timelock = translateRoomlock(activity[0])

			# for lectures
			if activity[2] == 0:

				# and too many students for room, substract points
				if int(chambers[room].capacity) < course.students:
					# print(chambers[room].capacity)
					# print(course.students)
					# print("te veel studenten: past niet in de zaal!")
					maluspoints = course.students - int(chambers[room].capacity)
					# print(maluspoints)
					points -= maluspoints

			# for practical/seminars
			else:

				# if seminar
				if course.seminars > 0:

					# and too many students fro room, substract points
					if int(chambers[room].capacity) < course.maxstudentssem:
						# print(chambers[room].capacity)
						# print(course.maxstudentssem)
						maluspoints = course.maxstudentssem - int(chambers[room].capacity)
						# print(maluspoints)
						points -= maluspoints

				# if practical
				else:

					# and too many students fro room, substract points
					if int(chambers[room].capacity) < course.maxstudentsprac:
						print(chambers[room].capacity)
						print(course.maxstudentsprac)
						maluspoints = course.maxstudentsprac - int(chambers[room].capacity)
						print(maluspoints)
						points -= maluspoints

	# show points
	# print("Points: ", points)
	return points

# points = calcScore(main.allcourses, main.student_list, main.chambers)
