import os.path
from .utility import *
from .cpNet import *
from random import *
from math import *

class Database:
	# filename = name of file,nC = numberOfComparison, nbV = number of variables, lb = lambda (number of edges), nbP = number of parents, nbO = number of objects, nbN = number of different scores, rand: true = generate random cp-net and false = use a (random) dataset, useFile: true = use an existent file and false = generate a random dataset
	def __init__(self,foldValidation,step,smooth,mode = 1, filename = "", nC = -1, noise = [0], nbV = -1, lb = -1, nbP = -1, k = 10):
		self.lenOfData = 1
		self.lenOfFold = 1
		if foldValidation:
			self.dataFold = []
			self.lenOfFold = 0
			for i in range(k):
				self.dataFold.append({}) 
				for n in noise:
					self.dataFold[i][n] = []
		else:
			self.data = {}
			for n in noise:
				self.data[n] = []
		
		# generate database from a file
		if mode == 1:
			print("step " + str(step) + "/" + str(smooth) + ":\t\t\tdata generation phase in progress...")
			file = open(filename,"r")
			data = []
			lines = file.readlines()
			self.numberOfAttributes = int(lines[0].split(" ")[1])
			del lines[0]
			del lines[0]
			del lines[0]
			for comp in lines:
				tab = comp[:-1].split(",")
				object1 = [int(i) for i in tab[0].split(" ")]
				object2 = [int(i) for i in tab[1].split(" ")]
				fVar = isASwap(object1,object2)
				if fVar != -1:
					data.append([object1,object2,fVar])
				
			if nC != -1:
				cpt = 0
				self.lenOfFold= int(nC/k)
				if cpt < nC and cpt < len(data):
					if foldValidation:
						cpt = 0
						for i in range(k):
							for j in range(self.lenOfFold):
								for n in noise:
									if randint(1,100) > n:
										self.dataFold[i][n].append(data[cpt])
									else:
										self.dataFold[i][n].append([data[cpt][1],data[cpt][0],data[cpt][2]])
								cpt += 1
					else:
						res = min(nC,len(data))
						for cpt in range(res):
							for n in noise:
								if randint(1,100) > n:
									self.data[n].append(data[cpt])
								else:
									self.data[n].append([data[cpt][1],data[cpt][0],data[cpt][2]])
						self.lenOfData = len(self.data[noise[0]])
			elif foldValidation:
				cpt = 0
				self.lenOfFold = int(len(data)/k)
				for i in range(k):
					for j in range(self.lenOfFold):
						for n in noise:
							if randint(1,100) > n:
								self.dataFold[i][n].append(data[cpt])
							else:
								self.dataFold[i][n].append([data[cpt][1],data[cpt][0],data[cpt][2]])
						cpt += 1
			else:
				for cpt in range(len(data)):
					for n in noise:
						if randint(1,100) > n:
							self.data[n].append(data[cpt])
						else:
							self.data[n].append([data[cpt][1],data[cpt][0],data[cpt][2]])
				self.lenOfData = len(self.data[noise[0]])
			file.close()
		
		# generate a database from a CP-net with noise
		if mode == 2:
			self.numberOfAttributes = nbV
			if nbV == -1:
				nbV = ceil(log(nC,2)) + 1
			N = CPNet(name = "N2", random = True,nbVar = nbV,lbd = lb,nbMaxParents = nbP)

			print("step " + str(step) + "/" + str(smooth) + ":\t\t\tdata generation phase in progress...")	
			
			if foldValidation:
				self.lenOfFold = int(nC/k)
				for i in range(k):
					for j in range(self.lenOfFold):
						comparison = self.newObject(nbV)
						flipVariable = N.getVariable(comparison[2])
						for n in noise:
							if N.preferred([flipVariable.id,flipVariable.valueOfParents(comparison[0]),comparison[0][flipVariable.id]]):
								if randint(1,100) > n:
									self.dataFold[i][n].append(comparison)
								else:
									self.dataFold[i][n].append([comparison[1],comparison[0],comparison[2]])
							else:
								if randint(1,100) > n:
									self.dataFold[i][n].append([comparison[1],comparison[0],comparison[2]])
								else:
									self.dataFold[i][n].append(comparison)
			else:
				for i in range(nC):
					comparison = self.newObject(nbV)
					flipVariable = N.getVariable(comparison[2])
					for n in noise:
						if N.preferred([flipVariable.id,flipVariable.valueOfParents(comparison[0]),comparison[0][flipVariable.id]]):
							if randint(1,100) > n:
								self.data[n].append(comparison)
							else:
								self.data[n].append([comparison[1],comparison[0],comparison[2]])
						else:
							if randint(1,100) > n:
								self.data[n].append([comparison[1],comparison[0],comparison[2]])
							else:
								self.data[n].append(comparison)
				self.lenOfData = len(self.data[noise[0]])
		
		# count the number of cycles of size 2
		self.percentageOfCycleSize2 = {}
		if not foldValidation:
			for n in noise:
				nbCycleSize2 = 0
				tab = []
				for comp in self.data[n]:
					n1 = fromBinToInt(comp[0])
					n2 = fromBinToInt(comp[1])
					# print((n1,n2),tab.keys())
					b = False
					for x in tab:
						if n1 == x[0] and n2 == x[1]:
							x[2] += 1
							b = True
					if not b:
						for x in tab:
							if n2 == x[0] and n1 == x[1]:
								x[3] += 1
								b = True
					if not b:
						tab.append([n1,n2,1,0])
				for val in tab:
					nbCycleSize2 += min(val[2],val[3])
				self.percentageOfCycleSize2[n] = nbCycleSize2/self.lenOfData*100
		
		# shuffle the data
		# for n in noise:
			# shuffle(self.data[n])

	def newObject(self,length):
		vector = []
		for i in range(length):
			if randint(0,1) % 2:
				vector.append(1)
			else:
				vector.append(0)
		flipValue = randint(0,length - 1)
		flipVector = list(vector)
		if flipVector[flipValue] == 0:
			flipVector[flipValue] = 1
		else:
			flipVector[flipValue] = 0
			
		return [vector,flipVector,flipValue]
