
import csv
import random

class Room:
	""" Adds features to room """

	def __init__(self, name, capacity): 
		self.name = name
		self.capacity = capacity
		self.booking = []

	def add_booking(self, timelock):
		""" Blocks time lock """

		self.booking.append(timelock)

	def __str__(self):
		return str(self.name)

	__repr__ = __str__


class Course:
	""" Add features to course """
	def __init__(self, name, lectures, seminar, practical):
		self.name = name
		self.lectures = int(lectures)
		self.seminars = int(seminar)
		self.practicals = int(practical)
		self.activities = []
		#self.maxstudents = maxstudents
		self.students = []

	def addStudent(self, student):
		""" Add student to course """
		self.students.append(student)

	def updateSchedule(self, roomlock, activity):
		self.activities.append([roomlock, activity]) 

	def __str__(self):
		return "Name: %s \nNumber of lectures: %s\nNumber of seminars: %s \nNumber of practicals: %s \n" % (self.name, self.lectures, self.seminar, self.practical)

# create empty list

if __name__=='__main__':

	chambers = []

	# reads csv file
	with open('zalen.csv', 'rt') as csvfile:
		
		# creates csvfile
		rooms = csv.reader(csvfile)

		# iterate over rows 
		for row in rooms:

			# extract text out of list
			for text in row: 

				# split features
				features = text.split(";")

				# initilize features for class 
				name = features[0] 
				capacity = features[1]

				# initilaze room using the class
				room = Room(name, capacity)

				# add room to list
				chambers.append(room)

	print(chambers)


# create list for courses
allcourses = []

# load courses as classes in allcourses-list
with open('vakken.csv', 'rt') as coursefile:
	courses = csv.reader(coursefile)
	for row in courses:
		for text in row:
			courseInfo = text.split(";")
			courseName = courseInfo[0]
			courseLectures = courseInfo[1]
			courseSeminars = courseInfo[2]
			coursePracticals = courseInfo[4]
			allcourses.append(Course(courseName, courseLectures, courseSeminars, coursePracticals))

# create empty dictionary with all room-timelock combinations (roomlocks) as keys
roomlocks = list(range(0, 140))
schedule = dict.fromkeys(roomlocks)

def translateRoomlock(roomlock):
	""" Translates roomlock number to roomnumber and timelock """
	room = roomlock % 7
	timelock = int(roomlock/7)
	return room, timelock

# loop through courses to schedule classes of course one-by-one
for course in allcourses:
	# schedule lectures while course has still lectures left to schedule
	while course.lectures > 0:
		# choose random roomlock
		pickroomlock = random.randint(0, 139)
		# pick new random roomlock if room is not empty at that time
		# dit errort trouwens soms, meestal niet (nog naar kijken!)
		while schedule[pickroomlock] is not None:
			pickroomlock = random.randint(0, 140)
		# schedule lecture in roomlock
		schedule[pickroomlock] = course.name + " lecture"
		course.lectures -= 1
		# put scheduled lecture in course class
		course.updateSchedule(pickroomlock, course.name + " lecture")
		# add scheduled lecture to room class
		room, timelock = translateRoomlock(pickroomlock)
		chambers[room].add_booking(timelock)
	# same for seminars
	while course.seminars > 0:
		pickroomlock = random.randint(0, 139)
		while schedule[pickroomlock] is not None:
			pickroomlock = random.randint(0, 140)
		schedule[pickroomlock] = course.name + " seminar"
		course.seminars -= 1
		course.updateSchedule(pickroomlock, course.name + " seminar")
		room, timelock = translateRoomlock(pickroomlock)
		chambers[room].add_booking(timelock)	
	# same for practicals
	while course.practicals > 0:
		pickroomlock = random.randint(0, 139)
		while schedule[pickroomlock] is not None:
			pickroomlock = random.randint(0, 140)
		schedule[pickroomlock] = course.name + " practical"
		course.practicals -= 1	
		course.updateSchedule(pickroomlock, course.name + " practical")
		room, timelock = translateRoomlock(pickroomlock)
		chambers[room].add_booking(timelock)

# even voor visualisatie
print(schedule) # heel schedule
print(allcourses[5].activities) # activiteiten van vak
print(chambers[1].booking) # bookings van een zaal

# valid schedule has been made: 1000 points
points = 1000;

# subtract or add points based on schedule
# loop through courses
for course in allcourses:
	print(course.name)
	dayActivity = []
	# loop trough activities of a course
	for activity in range(0, len(course.activities)):
		# determine day of activity
		timelock = course.activities[activity][0]
		day = int(timelock/28)
		# if day has more than one activity in one day: subtract 10 points
		if day in dayActivity:
			points -= 10
		# add day of activity to array of days of activities
		dayActivity.append(day)
	
	# check if classes are distributed over the week
	# if two activities in the week: mo-th, tu-fr or mo-fr?
	if (len(course.activities) == 2):
		if (abs(dayActivity[0] - dayActivity[1]) >= 3):
			points += 20
	# if three activities in the week: mo-we-fr?
	if (len(course.activities) == 3):
		if 0 in dayActivity and 2 in dayActivity and 4 in dayActivity:
			points += 20
	# if four activities in the week: mo-tu-th-fr?
	if (len(course.activities) == 4):
		if 0 in dayActivity and 1 in dayActivity and 3 in dayActivity and 4 in dayActivity:
			points += 20
	
	# laat even zien welke dagen er activiteiten zijn voor dit vak
	print("dag(en): ", dayActivity)

# laat eindscore zien (so far)
print("Points: ", points)
	


# # iterate over booking list 
# for timelock in booking:

# 	# move to next timelock if occupied
# 	if timelock == new_timelock:
# 		timelock += 1

# 	# add timelock if free
# 	else:
# 		add_booking(new_timelock)


