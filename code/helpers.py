import random
import math
import re
from classes import Students, Room, Course
from parse import *


def createRooms():
	""" Creates lists for rooms """

	# create empty list
	chambers = []

	# read csv file with rooms
	with open('../data/zalen.csv', 'rt') as csvfile:

		# create csvfile
		rooms = csv.reader(csvfile)

		# iterate over rows
		for row in rooms:

			# extract text out of list
			for text in row:

				# split features
				features = text.split(";")

				# initialize features for class
				name = features[0]
				capacity = features[1]

				# initilaze room using the class
				room = Room(name, capacity)

				# add room to list
				chambers.append(room)

	return chambers


def createCourses():
	""" Substracts course information and put into list """

	# create list for courses
	allcourses = []

	# load courses as classes in allcourses-list
	with open('../data/vakken.csv', 'rt') as coursefile:

		# clean text
		courses = csv.reader(coursefile)
		for row in courses:
			for text in row:
				courseInfo = text.split(";")

				# add course name
				courseName = courseInfo[0]

				# add amount of lectures
				courseLectures = courseInfo[1]

				# add amount of seminars
				courseSeminars = courseInfo[2]

				# add max amount seminars
				courseMaxSem = courseInfo[3]
				if courseMaxSem == "nvt":
					courseMaxSem = 0

				# add amount of practicals
				coursePracticals = courseInfo[4]

				# add max amount practicals
				courseMaxPrac = courseInfo[5]
				if courseMaxPrac == "nvt":
					courseMaxPrac = 0

				# add course to list
				allcourses.append(Course(courseName, courseLectures, courseSeminars, courseMaxSem, coursePracticals, courseMaxPrac))

	return allcourses

def createStudents():
	""" Creates a list with students """

	# create empty list
	student_list = []

	# import student classes
	student_list = createStudentClass()

	return student_list

def createEmptySchedule():
	""" Prepare dictionary that represents schedule """

	# create empty dictionary with all room-timelock combinations (roomlocks) as keys
	roomlocks = list(range(0, 140))
	schedule = dict.fromkeys(roomlocks)

	return schedule

def createStudentGroups(allcourses, student_list):
	"""" Divides students into practical and seminar groups """

	# for each course
	for course in allcourses:

		# check all students
		for student in student_list:

			# if student is attenting course
			if course.name in student.courses:

				# add student to course class
				course.addStudent(student.last_name)

		# if course has seminars
		if course.seminars > 0:

			# count and add amount to course class
			numofseminars = math.ceil(course.students/course.maxstudentssem)
			course.addSeminar(numofseminars)

		# if course has practicals
		if course.practicals > 0:

			# count and add to course class
			numofpracticals = math.ceil(course.students/course.maxstudentsprac)
			course.addPractical(numofpracticals)


		#* divide students over groups *#
		# start with group '1'
		sem = 1

		# if course has seminars
		if course.seminars > 0:

			# iterate over students in course with steps of max amount of students
			for i in range(0, len(course.studentnames), course.maxstudentssem):

				# create list with names of students
				studentlist = course.studentnames[i: i + course.maxstudentssem]

				# add studentlist to course class
				course.createSeminarGroup(sem, studentlist)

				# go on to the next group
				sem += 1

		# same for practical
		prac = 1
		if course.practicals > 0:
			for i in range(0, len(course.studentnames), course.maxstudentsprac):
				studentlist = course.studentnames[i: i + course.maxstudentsprac]
				course.createPracticalGroup(prac, studentlist)
				prac += 1


	return allcourses, student_list

def translateRoomlock(roomlock):
	""" Translates roomlock number into roomnumber and timelock """

	# amount of rooms per timelock
	total_amount_rooms = 7

	# determine the room
	room = roomlock % total_amount_rooms

	# determine timelock
	timelock = int(roomlock / total_amount_rooms)


	return room, timelock


def scheduleClass(course, typeClass, schedule, chambers, student_list):
	"""" Schedules activities of a course """

	# group activities by type
	if typeClass == "lecture":
		activity = course.lectures
	elif typeClass == "seminar":
		activity = course.seminars
	elif typeClass == "practical":
		activity = course.practicals

	# untill no activities are left
	while activity > 0:

		# choose random roomlock
		pickroomlock = random.randint(0, 139)

		# until an unoccupied roomlock is found
		while schedule[pickroomlock] is not None:

			# pick new random roomlock
			pickroomlock = random.randint(0, 139)

		# if room is free, substract the room and timelock
		room, timelock = translateRoomlock(pickroomlock)

		# add activity to schedule at roomlock
		schedule[pickroomlock] = course.name + " " + typeClass + " " + str(activity)

		#* determine group number *#

		# lecture has only 1 group
		if typeClass == "lecture":
			group = 0

		# seminars and practicals > 1 group,
		else:

			# activity number decreases as we schedule it, which gives different group number
			group = activity

		# update course class with new activity
		course.updateSchedule(pickroomlock, (course.name + " " + typeClass), group)

		# update room class with new activity
		room, timelock = translateRoomlock(pickroomlock)
		chambers[room].add_booking(timelock)


		# update student class with new activity
		if typeClass == "lecture":
			for student in student_list:
				if course.name in student.courses:
					student.updateStudentSchedule(timelock, course.name)

		if typeClass == "seminar":
			for student in student_list:
				if course.name in student.courses:
					if student.last_name in course.seminargroups[activity]:
						student.updateStudentSchedule(timelock, course.name)

		if typeClass == "practical":
			for student in student_list:
				if course.name in student.courses:
					if student.last_name in course.practicalgroups[activity]:
						student.updateStudentSchedule(timelock, course.name)

		# decrease activity counter
		activity -= 1

	return

def complementCourse(allcourses, schedule, chambers, student_list):
	""" Schedules activities for each course into schedule """

	# for each course
	for course in allcourses:

		# schedule activities
		scheduleClass(course, "lecture", schedule, chambers, student_list)
		scheduleClass(course, "seminar", schedule, chambers, student_list)
		scheduleClass(course, "practical", schedule, chambers, student_list)

	return allcourses, schedule, chambers, student_list

def createSchedule():
	""" Creates a schedule """

	# creates list available rooms
	chambers = createRooms()

	# creates list of all courses
	allcourses = createCourses()

	# creates student_list
	student_list = createStudents()

	# create empty schedule with roomlocks as keys
	schedule = createEmptySchedule()

	# divide students over courses-groups
	allcourses, student_list = createStudentGroups(allcourses, student_list)

	# complement schedule with activities from courses
	complementCourse(allcourses, schedule, chambers, student_list)

	return chambers, allcourses, student_list, schedule

def updateClassesFromSchedule(schedule):
	#* update classes to new schedule *#

	allcourses = createCourses()
	chambers = createRooms()
	student_list = createStudents()
	allcourses, student_list = createStudentGroups(allcourses, student_list)

	for roomlock, activity in schedule.items():
		if activity is not None:

			if "lecture" in activity:
				splittext = activity.split(" lecture ")
				typeClass = "lecture"
				coursename = splittext[0]
				group = 0

			if "seminar" in activity:
				splittext = activity.split(" seminar ")
				typeClass = "seminar"
				coursename = splittext[0]
				group = int(float(splittext[1]))

			if "practical" in activity:
				splittext = activity.split(" practical ")
				typeClass = "practical"


				coursename = splittext[0]
				group = int(float(splittext[1]))

			for course in allcourses:
				if coursename == course.name:

				# update course class with new activity
					course.updateSchedule(roomlock, (coursename + " " + typeClass), group)

					# update room class with new activity
					room, timelock = translateRoomlock(roomlock)
					chambers[room].add_booking(timelock)

					# update student class with new activity
					if typeClass == "lecture":
						for student in student_list:
							if course.name in student.courses:
								student.updateStudentSchedule(timelock, course.name)

					if typeClass == "seminar":
						for student in student_list:
							if course.name in student.courses:
								if student.last_name in course.seminargroups[group]:
									student.updateStudentSchedule(timelock, course.name)

					if typeClass == "practical":
						for student in student_list:
							if course.name in student.courses:
								if student.last_name in course.practicalgroups[group]:
									student.updateStudentSchedule(timelock, course.name)

	return allcourses, student_list, chambers

def calcScore(allcourses, student_list, chambers):
	""" Calculates the score of a schedule"""

	# start-score of a valid schedule
	points = 1000
	allcoursespoints = []
	roomlocks_per_day = 28

	#* create groups and dict to keep up the days per activity *#

	# iterate over courses
	for course in allcourses:

		coursepoints = 0

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

		#* subtract points based on activities per day *#

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


		for group in groups:
			for day in range(0, 5):
				dayoccurance = dayActivity[group].count(day)
				if dayoccurance > 1:
					points -= ((dayoccurance - 1) * 10)
					coursepoints -= ((dayoccurance - 1) * 10)
		#* add points for spreading of activities over week *#

		# iterate over groups
		for group in groups:

			# when 2 activities in week
			if (len(dayActivity[group]) == 2):

				# add points if they are spread (mo- thu, mo-fri)
				if (abs(dayActivity[group][0] - dayActivity[group][1]) >= 3):
					points += 20
					coursepoints += 20

			# when 3 activities in the week
			if (len(dayActivity[group]) == 3):

				# add points if spread (mo-we-fr)
				if 0 in dayActivity[group] and 2 in dayActivity[group] and 4 in dayActivity[group]:
					points += 20
					coursepoints += 20

			# if 4 activities in the week
			if (len(dayActivity[group]) == 4):

				# add points if spread  (mo-tu-th-fr)
				if 0 in dayActivity[group] and 1 in dayActivity[group] and 3 in dayActivity[group] and 4 in dayActivity[group]:
					points += 20
					coursepoints += 20

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
					coursepoints -= maluspoints

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
						coursepoints -= maluspoints

				# if practical
				else:

					# and too many students from room, substract points
					if int(chambers[room].capacity) < course.maxstudentsprac:
						print(chambers[room].capacity)
						print(course.maxstudentsprac)
						maluspoints = course.maxstudentsprac - int(chambers[room].capacity)
						print(maluspoints)
						points -= maluspoints
						coursepoints -= maluspoints

		allcoursespoints.append([course.name, coursepoints])



	# for all students
	for student in student_list:

		# create empty list
		timelocksStudent = []

		# for each activity in schedule
		for activity in student.schedule:

			# if roomlock is occupied substract points
			if activity[0] in timelocksStudent:
				points -= 1
				coursepoints -= 1

			# add roomlock to list
			timelocksStudent.append(activity[0])

	return points

def swapCourse(chambers, allcourses, student_list, schedule, course1 = None, activity1 = None, course2 = None, activity2 = None):
	""" Swaps roomlocks of 2 (random) courses """

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
		if len(allcourses[course1].activities) == 0:
			activity1 = 0
		else:
			activity1 = random.randint(0, len(allcourses[course1].activities) - 1)

	# same
	if activity2 == None:
		if len(allcourses[course2].activities) == 0:
			activity2 = 0
		else:
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
				if allcourses[course1].seminars > 0 and allcourses[course1].practicals == 0:

					# if student is in seminargroup
					if student.last_name in allcourses[course1].seminargroups[coursegroup1]:

							# change individual schedule with swapped course
							student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

				# if course has practical
				elif allcourses[course1].practicals > 0 and allcourses[course1].seminars == 0:
					# if student is in practical-group
					if student.last_name in allcourses[course1].practicalgroups[coursegroup1]:
						# print(student.last_name)
						# change individual schedule
						student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

				elif allcourses[course1].seminars > 0 and allcourses[course1].practicals > 0:
					if student.last_name in allcourses[course1].seminargroups[coursegroup1] or student.last_name in allcourses[course1].practicalgroups[coursegroup1]:
						student.changeStudentSchedule(timelock1, timelock2, allcourses[course1].name)

	# same for the second coursegroup
	if coursegroup2 == 0:
		for student in student_list:
			if allcourses[course2].name in student.courses:
				student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)

	else:
		for student in student_list:
				# if course has seminar
				if allcourses[course2].seminars > 0 and allcourses[course2].practicals == 0:

					# if student is in seminargroup
					if student.last_name in allcourses[course2].seminargroups[coursegroup2]:

							# change individual schedule with swapped course
							student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)

				# if course has practical
				elif allcourses[course2].practicals > 0 and allcourses[course2].seminars == 0:
					# if student is in practical-group
					if student.last_name in allcourses[course2].practicalgroups[coursegroup2]:
						student.changeStudentSchedule(timelock2, timelock1, allcourses[course2].name)

				elif allcourses[course2].seminars > 0 and allcourses[course2].practicals > 0:
					if student.last_name in allcourses[course2].seminargroups[coursegroup2] or student.last_name in allcourses[course2].practicalgroups[coursegroup2]:
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

	return course1, activity1, course2, activity2, schedule


def swapStudents(chambers, allcourses, student_list, schedule, swapcourse = None, sem1 = None, sem2 = None, prac1 = None, prac2 = None, student1 = None, student2 = None):
	""" Swaps between seminar- or practicalgroups of two (random) students in a (random) course """

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

# initiliaze temperatures
start_temp = 10
final_temp = 0.0001

def linear(min_iterations, i, start = start_temp, final = final_temp):
    """ Returns temperature calculated using a linear function """

    temperature = start - i * (start - final) / min_iterations
    
    return temperature


def exponential(min_iterations, i, start = start_temp, final = final_temp):
    """ Returns temperature calculated using an exponential function """

    temperature = (start * (final / start) ** (i / min_iterations))
 
    return temperature 


def sigmoidal(min_iterations, i, start = start_temp, final = final_temp ):
    """ Returns temperature, calculated using a sigmoidal function """

    # to prevent a math overflow a scale (x^(1/ (i - min_iterations))) is used
    temperature = final + ((start - final)**( 1/ (i - min_iterations))) / \
    				(1 **(i - min_iterations)) + math.exp(0.3 * ((i - min_iterations / 2) /(i - min_iterations)))

    return temperature


def geman(min_iterations, i, start = start_temp):
	""" Returns temperature, calculated using a geman function """
 
	temperature = start / (math.log(i + 1) + 1) 
	
	return temperature


def lin_exp(min_iterations, i): 
    """ Temperature is calculated using an exponential and linear function """

    # vary between the functions
    if i % 2 == 0: 
        return exponential(min_iterations, i)
    else: 
        return linear(min_iterations, i)


def exp_sig(min_iterations, i): 
    """ Temperature is calculated using an exponential and linear function """

    # vary between the functions
    if i % 2 == 0: 
        return sigmoidal(min_iterations, i)
    else: 
        return exponential(min_iterations, i)


def gem_lin(min_iterations, i): 
    """ Temperature is calculated using an geman and linear function """

    # vary between the functions
    if i % 2 == 0: 
        return linear(min_iterations, i)
    else: 
        return geman(min_iterations, i)



def gem_exp(min_iterations, i): 
    """ Temperature is calculated using an exponential and geman function """

    # vary between the functions
    if i % 2 == 0: 
        return geman(min_iterations, i)
    else: 
        return exponential(min_iterations, i)


def lin_sig(min_iterations, i): 
    """ Temperature is calculated using an sigmoidal and linear function """

    # vary between the functions
    if i % 2 == 0: 
        return sigmoidal(min_iterations, i)
    else: 
       return linear(min_iterations, i)

def gem_exp(min_iterations, i): 
    """ Temperature is calculated using an geman and sigmoidal function """

    # vary between the functions
    if i % 2 == 0: 
        return geman(min_iterations, i)
    else: 
        return sigmoidal(min_iterations, i)

def initial_population(amount):
    """ Creates an intial population and returns the parents """

    population = []
    scores = []

    for i in range(amount):

        # print("Generating initial population...")

        timetable_info = []
        score_info = []

        # create a new random schedule
        chambers, allcourses, student_list, schedule = create_schedule()

        # print("Hillclimbing on schedule {}...".format(i))
        # hillclimb_roomlocks2(20, chambers, allcourses, student_list, schedule)

        # add all information about this specific schedule
        score_info.append(allcourses)
        score_info.append(student_list)
        score_info.append(chambers)

        # add individual schedule-info to timetable array
        timetable_info.append(score_info)
        timetable_info.append(schedule)

        # add the array with individual timetable-info to the population
        population.append(timetable_info)


    return population


def selection(population, rate):
    """ Calculates the fitness of an individual by returning the schedule score """

    mating_pool = []
    scores = []

    def fitness(timetable_info):
        """ Calculates the fitness of an individual """

        # print("Calculating fitness scores...")

        return calc_score(timetable_info[0][0],
                         timetable_info[0][1],
                         timetable_info[0][2])

    # choose the fittest individuals
    population = sorted(population, key=fitness, reverse=True)

    # set max and range
    probability = int(rate * len(population))
    rate = int(rate * 100)

    for i in range(rate):

        # fittest schedules have highest probabilities
        scores.append(calc_score(population[i][0][0], population[i][0][1], population[i][0][2]))
        mating_pool.append(population[i])

    # iterate over parents
    # for i in range(rate):
    #
    #     # create matingpool
    #     for j in range(probability):
    #
    #         # fittest schedules have highest probabilities
    #         scores.append(calc_score(population[i][0][0], population[i][0][1], population[i][0][2]))
    #         mating_pool.append(population[i])
    #
    #     # decrease probability
    #     probability -= 1

    return mating_pool


def mutation(schedule, chambers, allcourses, student_list, chance):
    """ Creates a mutation by performing a hillclimber for roomlocks """

    # determine probability
    probability = random.random()

    # if probability is smaller than given chance
    if probability < chance:

        # swap between roomlocks using hillclimber
        hillclimb_roomlocks2(int(probability * 100), chambers, allcourses, student_list, schedule)

    return



def cross_over(mating_pool, offspring, generation, chance):
    """ Creates offspring by exchanging genes from mating pool """

    # create empty list for children
    children = []
    fittest_score = 0
    chance_array = []
    gen_scores = []

    # determine probability
    probability = len(mating_pool)

    # iterate over mating pool
    for i in range(len(mating_pool)):

        # iterate over probability
        for j in range(probability):

            # append iteration
            chance_array.append(i)

        # decrease probability
        probability -= 1

    # set fittest_score
    fittest_score = 0

    # iterate over offspring
    for i in range(offspring):

        # create an empty schedule
        schedule = create_empty_schedule()

        # amount of activites that have to be scheduled
        activities = 125

        # choose a mother and father from the mating pool
        parents = []
        parents = mating_pool
        random_parent = chance_array[random.randint(0, len(chance_array) - 1)]
        parent_schedule = parents[random_parent][1]
        
        # until no activities are left
        while activities > 0:

            # print("Applying crossover between parents...")

            # if activities % 2 == 0:
            #     parent_schedule = parents[0][1]  # >>> [[allcourses, chambers, studentlist], schedule]
            # else:
            #     parent_schedule = parents[1][1]

            # choose random course from parent schedule
            random_course = random.randint(0, len(parent_schedule) - 1)

            # create empty course list
            courses = []

            # iterate over values in schedule
            for key, value in schedule.items():

                # if roomlock is not empty
                if value is not None:

                    # add to course list
                    courses.append(value)

            # initialize counters
            counter = 0
            newparentcounter = 0

            # if schedule has no place for the random course, a None value is chosen, or the random course is already chosen
            while schedule[random_course] is not None or parent_schedule[random_course] is None or parent_schedule[random_course] in courses:
                
                # choose new random course from parent schedule
                random_course = random.randint(0, len(parent_schedule) - 1)

                # increase counter
                counter += 1
        
                # if random course still not scheduled
                if counter > 100:

                    # choose new parent
                    parent_schedule = parents[random.randint(0, len(parents) - 1)][1]
                    
                    # reset counter
                    counter = 0

                    # increase parent-counter
                    newparentcounter += 1

                    # if 500 new parents weren't enough
                    if newparentcounter > 500:
                        break

            # schedule random course on same place as parent
            schedule[random_course] = parent_schedule[random_course]

            # decrease activities
            activities -= 1

        # update classes from schedule
        allcourses, student_list, chambers = update_classes_from_schedule(schedule)

        # create new arrays schedule properties
        timetable_info = []
        score_info = []

        # add all information about this specific schedule
        score_info.append(allcourses)
        score_info.append(student_list)
        score_info.append(chambers)

        # perform mutatation if chance is higher than probability
        mutation(schedule, chambers, allcourses, student_list, chance)

        # add individual schedule-info to timetable array
        timetable_info.append(score_info)
        timetable_info.append(schedule)

        # calculate score
        score = calc_score(allcourses, student_list, chambers)

        # add to score file
        gen_scores.append(score)

        # if score is better than the fittest
        if score > fittest_score:

            # adjust fittest score
            fittest_score = score
            
            print("New best found ---> Schedule: {}, generation: {}, score: {}".format(i, generation, score))

        # add the array with individual timetable-info to the population
        children.append(timetable_info)

    # create score dict
    total_gen_scores[generation] = gen_scores

    return children

def print_schedule(schedule, allcourses, student_list, chambers):

    schedule_location = "visualisation/schedule.csv"
    schedule_file = open(schedule_location, 'w')

    writer = csv.writer(schedule_file)

    times = ['Monday 09:00 - 11:00', 'Monday 11:00 - 13:00', 'Monday 13:00 - 15:00', 'Monday 15:00 - 17:00',
             'Tuesday 09:00 - 11:00', 'Tuesday 11:00 - 13:00', 'Tuesday 13:00 - 15:00', 'Tuesday 15:00 - 17:00',
             'Wednesday 09:00 - 11:00', 'Wednesday 11:00 - 13:00', 'Wednesday 13:00 - 15:00', 'Wednesday 15:00 - 17:00',
             'Thursday 09:00 - 11:00', 'Thursday 11:00 - 13:00', 'Thursday 13:00 - 15:00', 'Thursday 15:00 - 17:00',
             'Friday 09:00 - 11:00', 'Friday 11:00 - 13:00', 'Friday 13:00 - 15:00', 'Friday 15:00 - 17:00']

    timetable = []

    j = 0

    for i in range(0, len(schedule), 7):
        timelock = []
        timelock.append(times[j])
        timelock.append(schedule[i])
        timelock.append(schedule[i+1])
        timelock.append(schedule[i+2])
        timelock.append(schedule[i+3])
        timelock.append(schedule[i+4])
        timelock.append(schedule[i+5])
        timelock.append(schedule[i+6])
        timetable.append(timelock)
        j += 1

    score, acp = calcScore(allcourses, student_list, chambers)

    fields = ['Score = {}'.format(score), 'A1.04', 'A1.06', 'A1.08', 'A1.10', 'B0.201', 'C0.110', 'C1.112']

    writer.writerow(fields)

    for timelock in timetable:
        writer.writerow(timelock)

    print("Printed a schedule at {} with a score of {}.".format(schedule_location, score))

def plot_simulated_annealing(scores, coolingscheme, best_score): 
	""" Plots schedule score during simulated annealing """ 

	functionname = str(coolingscheme.__name__)
	plt.plot(range(0, len(scores)), scores, label=functionname)
	plt.ylabel("Score")
	plt.xlabel("Runs")
	plt.title("Simulated annealing")
	plt.text(5, (max(scores)), best_score)
	plt.legend()
	plt.show()	

def plot_random_schedules(scores):
	""" Creates an histogram of random schedules"""

	plt.hist(scores, bins = len(scores))
	plt.ylabel("Score")
	plt.xlabel("Times")
	plt.title("Histogram random schedules")
	plt.show()


def plot_hillclimber(scores, hillclimb_students_scores = None):
	""" Plots schedule score during hillclimber """

	plt.plot(range(0, len(scores)), scores)
	if hillclimb_students_scores:
		plt.plot(range(len(scores), len(scores) + len(hillclimb_students_scores)), hillclimb_students_scores)
	plt.ylabel("Score")
	plt.xlabel("Amount of swaps")
	plt.title("Hillclimber")
	plt.show()


def multiple_simulated_annealing(scores): 
	""" Plots schedule score during simulated annealing for different coolingschemes """ 

	plt.plot(range(0, len(scores[0])), scores[0], label = "geman")
	plt.plot(range(0, len(scores[1])), scores[1], label = "linear")
	plt.plot(range(0, len(scores[2])), scores[2], label = "sigmoidal")
	plt.plot(range(0, len(scores[3])), scores[3], label = "exponential")		
	plt.ylabel("Score")
	plt.xlabel("Runs")
	plt.title("Simulated annealing")
	# plt.text(5, max(scores[0]))
	plt.legend()
	plt.show()	


def plot_average_hillclimb(repetitions, runs):
""" Performs the hillclimber a certain number of times (repetitions) with a specified number of runs
 and plot the average scores """
	totalscores = []
	for i in range(repetitions):
		algorithm_scores = []
		chambers, allcourses, student_list, schedule = createSchedule()
		for i in range(runs):
			score = hillclimbRoomlocks(1, chambers, allcourses, student_list, schedule)
			algorithm_scores.append(score)
		totalscores.append(algorithm_scores)

	sorted_scores = []
	for i in range(runs):
		selected_score = []
		for j in range(repetitions):
			selected_score.append(totalscores[j][i])
		sorted_scores.append(selected_score)

	average_scores = []
	for scores in sorted_scores:
		average_scores.append(sum(scores)/len(scores))

	plot_hillclimber(average_scores)


def plot_average_SA(repetitions, runs):
""" Performs all cooling schemes of simulated annealing a certain number of times (repetitions) and
plots the average scores """
	totalscores = []
	for i in range(repetitions):
		algorithm_scores = []
		chambers, allcourses, student_list, schedule = createSchedule()
		best_score, best_courses, best_student_list, best_chambers, geman_scores = simulatedAnnealing(geman, runs, chambers, allcourses, student_list, schedule)
		chambers, allcourses, student_list, schedule = createSchedule()
		best_score, best_courses, best_student_list, best_chambers, linear_scores = simulatedAnnealing(linear, runs, chambers, allcourses, student_list, schedule)
		chambers, allcourses, student_list, schedule = createSchedule()
		best_score, best_courses, best_student_list, best_chambers, sigmoidal_scores = simulatedAnnealing(sigmoidal, runs, chambers, allcourses, student_list, schedule)
		chambers, allcourses, student_list, schedule = createSchedule()
		best_score, best_courses, best_student_list, best_chambers, exponential_scores = simulatedAnnealing(exponential, runs, chambers, allcourses, student_list, schedule)
		algorithm_scores.append([geman_scores, linear_scores, sigmoidal_scores, exponential_scores])
		totalscores.append(algorithm_scores)

	print(totalscores)

	all_geman_scores = []
	all_linear_scores = []
	all_sigmoidal_scores = []
	all_exponential_scores = []

	for i in range(repetitions):
		all_geman_scores.append(totalscores[i][0][0])
		all_linear_scores.append(totalscores[i][0][1])
		all_sigmoidal_scores.append(totalscores[i][0][2])
		all_exponential_scores.append(totalscores[i][0][3])

	geman_sorted_scores = []
	linear_sorted_scores = []
	sigmoidal_sorted_scores = []
	exponential_sorted_scores = []
	for i in range(runs):
		geman_selected_score = []
		linear_selected_score = []
		sigmoidal_selected_score = []
		exponential_selected_score = []
		for j in range(repetitions):
			geman_selected_score.append(all_geman_scores[j][i])
			linear_selected_score.append(all_linear_scores[j][i])
			sigmoidal_selected_score.append(all_sigmoidal_scores[j][i])
			exponential_selected_score.append(all_exponential_scores[j][i])
		geman_sorted_scores.append(geman_selected_score)
		linear_sorted_scores.append(linear_selected_score)
		sigmoidal_sorted_scores.append(sigmoidal_selected_score)
		exponential_sorted_scores.append(exponential_selected_score)

	geman_average_scores = []
	for scores in geman_sorted_scores:
		geman_average_scores.append(sum(scores)/len(scores))

	linear_average_scores = []
	for scores in linear_sorted_scores:
		linear_average_scores.append(sum(scores)/len(scores))

	sigmoidal_average_scores = []
	for scores in sigmoidal_sorted_scores:
		sigmoidal_average_scores.append(sum(scores)/len(scores))

	exponential_average_scores = []
	for scores in exponential_sorted_scores:
		exponential_average_scores.append(sum(scores)/len(scores))

	average_scores = [geman_average_scores, linear_average_scores, sigmoidal_average_scores, exponential_average_scores]

	multiple_simulated_annealing(average_scores)

