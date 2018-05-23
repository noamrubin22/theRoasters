import csv
from generateschedule import createSchedule, translateRoomlock

chambers, allcourses, student_list, schedule = createSchedule()

print(schedule)
# print(schedule[5])

if 'Reflectie op de digitale cultuur lecture' in schedule.values:
	print("Yes")


roomlocks = []
roomnames = []
timelocks = []
days = []
coursenames = []
typeclasses = []
groups = []

for roomlock in schedule:
	roomlocks.append(roomlock)
	room, timelock = translateRoomlock(roomlock)
	roomname = chambers[room].name
	roomnames.append(roomname)
	timelocks.append(timelock)
	day = int(timelock / 4)
	days.append(day)
	contentroomlock = schedule.get(roomlock)
	if contentroomlock == None:
		typeclass = None
	elif "lecture" in contentroomlock:
		typeclass = 0
	elif "seminar" in contentroomlock:
		typeclass = 1
	elif "practical" in contentroomlock:
		typeclass = 2
	typeclasses.append(typeclass)
	for course in allcourses:
		for activity in course.activities:
			if activity[0] == roomlock:
				group = activity[2]
		if contentroomlock == None:
			coursename = None
			group = None
			students = None
		elif course.name in contentroomlock:
			coursename = course.name
			if typeclass == 0:
				students = course.studentnames
			elif typeclass == 1:
				students = course.seminargroups[group]
			elif typeclass == 2:
				# print(course.name)
				# print(course.practicalgroups)
				# print(group)
				students = course.practicalgroups[group]
	# print(students)


	coursenames.append(coursename)
	groups.append(groups)


	

with open("csvScore.csv", "w") as outFile:
	wr = csv.writer(outFile, dialect = 'excel')
	wr.writerow(roomlocks)
	wr.writerow(roomnames)
	wr.writerow(timelocks)
	wr.writerow(days)
	wr.writerow(coursenames)
	wr.writerow(["type", typeclasses])
