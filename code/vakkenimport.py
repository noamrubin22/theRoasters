import csv

class Course:
	def __init__(self, name, lectures, seminar, practical):
		self.name = name
		self.lectures = lectures
		self.seminar = seminar
		self.practical = practical
		#self.maxstudents = maxstudents
		self.students = []

	def addStudent(self, student):
		self.students.append(student)

	def __str__(self):
		return "Name: %s \nNumber of lectures: %s\nNumber of seminars: %s \nNumber of practicals: %s \n" % (self.name, self.lectures, self.seminar, self.practical)

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

print(allcourses[0].name)

