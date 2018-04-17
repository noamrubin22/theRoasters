
import csv

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
		self.lectures = lectures
		self.seminar = seminar
		self.practical = practical
		#self.maxstudents = maxstudents
		self.students = []

	def addStudent(self, student):
		""" Add student to course """
		self.students.append(student)

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


# create course-classes
allcourses = []

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

print(allcourses[1])

# # iterate over booking list 
# for timelock in booking:

# 	# move to next timelock if occupied
# 	if timelock == new_timelock:
# 		timelock += 1

# 	# add timelock if free
# 	else:
# 		add_booking(new_timelock)


