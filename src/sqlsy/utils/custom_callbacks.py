import random
from sqlsy.engine import Engine
import numpy as np

random.seed()

# choose from sequence at random
def random_choice(sequence: list):
	return random.choice(sequence)


# generate random floats
def random_float(n1:int, n2:int):
	return random.choice(np.arange(n1, n2, 0.1))


# to make calls to sequence
# independent we need shared count {}
def sequence():
	state = {}
	# generate sequence of numbers
	def internal(n1:int, n2:int):
		nonlocal state
		col = Engine.get_col()   # get current column being filled
		state.setdefault(col, n1)
		state[col] += 1
		return state[col]-1
	return internal