
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

    
    class Student:
	""" Adds students """

	def __init__(self, name, student_id, courses): 
		self.name = name
		self.student_id = capacity
		self.courses = []

	def add_booking(self, timelock):
		""" Blocks time lock """

		self.booking.append(timelock)

	def __str__(self):
		return str(self.name)

	__repr__ = __str__

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

# # iterate over booking list 
# for timelock in booking:

# 	# move to next timelock if occupied
# 	if timelock == new_timelock:
# 		timelock += 1

# 	# add timelock if free
# 	else:
# 		add_booking(new_timelock)


