import random
import time

random.seed()

# to choose from a list sequentially
class Sequence:
	def __init__(self, seed=0):
		self.seed = seed

	def select(self, sequence:list):
		while self.seed <= self.constraint:
			ret = sequence[self.seed]
			self.seed += 1
			return ret

	def clear(self):
		self.seed = 0

	# limit the rows
	def limit(self, n):
		self.constraint = n


seq = Sequence()

# choose from sequence at random
def random_choice(sequence: list):
	return random.choice(sequence)


def seq_choice(sequence:list):
	# this function limits the no of rows
	seq.limit(len(sequence))
	return seq.select(sequence)