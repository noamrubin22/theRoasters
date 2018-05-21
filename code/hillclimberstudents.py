import main
import scorefunction
import random
from main import translateRoomlock
from scorefunction import calcScore

allcourses = main.allcourses
student_list = main.student_list
chambers = main.chambers
schedule = main.schedule

def swapStudents():
	# pick course to swap students in
	swapcourse = random.randint(0, len(allcourses) - 1)

	# pick new course if the course has not enough seminargroups or practicalgroups
	while allcourses[swapcourse].seminars < 2 and allcourses[swapcourse].practicals < 2:
		swapcourse = random.randint(0, len(allcourses) - 1)

	print(allcourses[swapcourse].name)

	# swap students if course has seminars
	if allcourses[swapcourse].seminars > 1:
		
		# pick two seminarsgroups to swap students in
		sem1 = random.randint(1, allcourses[swapcourse].seminars)
		sem2 = random.randint(1, allcourses[swapcourse].seminars)

		# pick new seminargroups if the same groups have been chosen
		while sem1 == sem2:
			sem1 = random.randint(1, allcourses[swapcourse].seminars)
			sem2 = random.randint(1, allcourses[swapcourse].seminars)

		print(sem1)
		print(sem2)

		# save names of students in seminargroups 1 and 2
		seminargroup1 = allcourses[swapcourse].seminargroups[sem1]
		seminargroup2 = allcourses[swapcourse].seminargroups[sem2]

		print(seminargroup1)
		print(seminargroup2)

		# pick random student from seminargroup
		student1 = seminargroup1[random.randint(0, len(seminargroup1))]
		student2 = seminargroup2[random.randint(0, len(seminargroup2))]

		print(student1)
		print(student2)

		allcourses[swapcourse].switchSeminarStudent(sem1, student1, student2)
		allcourses[swapcourse].switchSeminarStudent(sem2, student2, student1)

		print(allcourses[swapcourse].seminargroups[sem1])
		print(allcourses[swapcourse].seminargroups[sem2])





swapStudents()