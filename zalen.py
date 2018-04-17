class Room:
	""" Adds features to room """

	def __init__(self, name, capacity): 
		self.name = "A1.04"
		self.capacity = 41
		self.booking = []

	def add_booking(self, timelock):
		""" Blocks time lock """

		self.booking.append(timelock)

# iterate over booking list 
for timelock in booking:

	# move to next timelock if occupied
	if timelock == new_timelock:
		timelock += 1

	# add timelock if free
	else:
		add_booking(new_timelock)