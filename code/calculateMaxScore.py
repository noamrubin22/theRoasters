from generateschedule import createSchedule

chambers, allcourses, student_list, schedule = createSchedule()

roomlocks_per_day = 28

points = 1000


for course in allcourses:
		# if seminar(s) exist
	if course.seminars > 0:

		# create list with amount of seminar-groups
		groups = list(range(1, int(course.seminars) + 1))

	# if practical exist
	elif course.practicals > 0:

		# create list with amount of practical-groups
		groups = list(range(1, int(course.practicals) + 1))

	# otherwise only one group (lecture)
	else:
		groups = [1]

	# create dict with groupnumber as key, [days] as values
	dayActivity = {k: [] for k in groups}

	# iterate over activities per course
	for activity in course.activities:

		# determine day
		day = int(activity[0] / roomlocks_per_day)

		# if activity = lecture
		if activity[2] == 0:

			# add day to list linked to lecture
			for group in groups:
				dayActivity[group].append(day)

		# for seminars and practicals
		else:
			# add day to list linked to group
			dayActivity[activity[2]].append(day)

	if len(dayActivity[1]) >= 2 and len(dayActivity[1]) <= 4:
		points += (20 * len(groups))

print(points)


