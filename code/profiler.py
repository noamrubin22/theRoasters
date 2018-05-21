import cProfile, pstats, io

def profile(fnc):

	""" A decorator that uses cProfile to profile a function """

	def inner(*args, **kwargs):

		pr = cProfile.Profile()
		pr.enable()
		retval = fnc(*args, **kwargs)
		pr.disable()
		s = io.StringI0()
		sortby = "cumulative"
		ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
		ps.print_stats()
		print(s.getvalue())
		return retval

	return inner