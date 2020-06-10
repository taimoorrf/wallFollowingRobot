
# Set up library imports.
import random
from collections import Counter
from itertools import chain

# install bitstring 
import subprocess
import sys
def install(package):
	subprocess.check_call([sys.executable, "-m", "pip", "install", package])
install("bitstring")

# import bitstring
from bitstring import *

########################################################
'''
	- This module assumes you first read the Jupyter notebook. 
	- You are free to add other members functions in class GeneticAlgorithm
	  as long as you do not modify the code already written. If you have justified
	  reasons for making modifications in code, come talk to us. 
	- Our implementation uses recursive solutions and some flavor of 
	  functional programming (maps/lambdas); You're not required to do so.
	  Just Write clean code. 
'''
########################################################

class GeneticAlgorithm(object):

	def __init__(self, POPULATION_SIZE, CHROMOSOME_LENGTH, verbose):
		self.wall_bit_string_raw = "01010101011001101101010111011001100101010101100101010101"
		self.wall_bit_string = ConstBitStream(bin = self.wall_bit_string_raw)
		self.population_size = POPULATION_SIZE
		self.chromosome_length = CHROMOSOME_LENGTH # this is the length of self.wall_bit_string
		self.terminate = False
		self.verbose = verbose # In verbose mode, fitness of each individual is shown. 

	def run_genetic_alg(self):
		'''  
		The pseudo you saw in slides of Genetic Algorithm is implemented here. 
		Here, You'll get a flavor of functional 
		programming in Python- Those who attempted ungraded optional tasks in tutorial
		have seen something similar there as well. 
		Those with experience in functional programming (Haskell etc)
		should have no trouble understanding the code below. Otherwise, take our word that
		this is more or less similar to the generic pseudocode in Jupyter Notebook.

		'''
		"You may not make any changes to this function."

		# Creation of Population
		solutions = self.generate_candidate_sols(self.population_size) # arg passed for recursive implementation.

		# Evaluation of individuals
		parents = self.evaluate_candidates(solutions)

		while(not self.terminate):
			# Make pairs
			pairs_of_parents = self.select_parents(parents)

			# Recombination of pairs.
			recombinded_parents = list(chain(*map(lambda pair: \
				self.recombine_pairs_of_parents(pair[0], pair[1]), \
					pairs_of_parents))) 

			# Mutation of each individual
			mutated_offspring = list(map(lambda offspring: \
				self.mutate_offspring(offspring), recombinded_parents))

			# Evaluation of individuals
			parents = self.evaluate_candidates(mutated_offspring) # new parents (offspring)
			if self.verbose and not self.terminate:
				self.print_fitness_of_each_indiviudal(parents)

######################################################################
###### These two functions print fitness of each individual ##########

# *** "Warning" ***: In this function, if an individual with 100% fitness is discovered, algorithm stops. 
# You should implement a stopping condition elsewhere. This codition, for example,
# won't stop your algorithm if mode is not verbose.
	def print_fitness_of_one_individual(self, _candidate_sol):
		_WallBitString = self.wall_bit_string
		_WallBitString.pos = 0
		_candidate_sol.pos = 0
		
		matching_bit_pairs = 0
		try:
			if not self.terminate:
				while (_WallBitString.read(2).bin == _candidate_sol.read(2).bin):
					matching_bit_pairs = matching_bit_pairs + 1
				print('Individual Fitness: ', round((matching_bit_pairs)/28*100, 2), '%')
		except: # When all bits matched. 
			pass
			return

	def print_fitness_of_each_indiviudal(self, parents):
		if parents:
			for _parent in parents:
				self.print_fitness_of_one_individual(_parent)

###### These two functions print fitness of each individual ##########
######################################################################

	def select_parents(self, parents):
		parentsList = []
		i = 0
		while i < len(parents):
			parentsList.append((parents[i], parents[i + 1]))
			i += 2
		
		return parentsList


	# A helper function that you may find useful for `generate_candidate_sols()`
	def random_num(self):
		random.seed()
		return random.randrange(2**14) ## for fitting in 14 bits.

	def generate_candidate_sols(self, n): 
		population = []
		for i in range(n):
			randStr = ''
			for j in range(4):
				randNum = format(self.random_num(),"014b")
				randStr += str(randNum)
			population.append(ConstBitStream(bin = (randStr)))
		
		return population

	def recombine_pairs_of_parents(self, p1, p2):
		random.seed()
		num = random.randrange(31, 51)
		numOneLeft = p1[:num]
		numOneRight = p1[num:]
		numTwoLeft = p2[:num]
		numTwoRight = p2[num:]
		
		return (numOneLeft + numTwoRight, numTwoLeft + numOneRight)

	def mutate_offspring(self, p):
		mutationRate = 0.005
		i = 0
		strm = BitStream(p)
		while i < len(p):
			random.seed()
			randNum = random.choices([0, 1], [(1 - mutationRate), mutationRate])
			if randNum == [1]:
				strm.invert(i)
			i = i+1
		return ConstBitStream(strm)

	def evaluate_candidates(self, candidates): 
		
		
		sameBits = []
		i = 0
		while i < len(candidates):
			same = 0
			self.wall_bit_string.pos = 0
			candidates[i].pos = 0
			while self.wall_bit_string.read('bin:2') == candidates[i].read('bin:2'):
				if candidates[i].pos >= 56 or self.wall_bit_string.pos >= 56:
					break
				same += 1
			self.wall_bit_string.pos = 0
			candidates[i].pos = 0
			sameBits.append(same)
			i+=1

		similarityLength = []
		i = 0
		
		while i < len(candidates):
			similarityLength.append((sameBits[i]/28.0))
			i += 1
		sumList = sum(similarityLength)
		average = (sumList/28)/len(candidates)
		probabilites = []
		i = 0
		while i < len(candidates):
			probabilites.append(similarityLength[i]/average)
			i += 1

		if self.wall_bit_string in candidates:
			print("100 percent achieved")
			self.terminate = True
		
		return random.choices(candidates, probabilites, k = self.population_size)



