from variable import *
from random import *
from operator import itemgetter

# a CP-Net constists of
# a name, usually a letter
# a list of variables
# a cpGraph (represented by an adjacency matrix)
# an outcome graph (represented by a adjacency list)
class CPNet:
	def __init__(self, nbVar = -1,lbd = -1,nbMaxParents = -1, name = "", random = False):
		self.numberOfRules = 0
		self.name = name
		self.candidateVariables = []
		if not random:
			self.variables = []
		else:
			self.variables = []
			
			# create variables
			for i in range(nbVar):
				self.variables.append(Variable(id = len(self.variables)))
			
			nbMaxEdges = int(nbVar * (nbVar - 1)/2)
			if lbd == -1:
				nbEdges = nbMaxEdges
			else:
				nbEdges = lbd * nbVar
				if nbEdges > nbMaxEdges:
					nbEdges = nbMaxEdges
			nbEdgesToDelete = nbMaxEdges - nbEdges
			
			# create parents variables
			for i in range(len(self.variables)):
				var1 = self.getVariable(i)
				for j in range(i+1,len(self.variables)):
					var2 = self.getVariable(j)
					self.addParentVariables(var2,[var1])
					
			t = self.depassParent(nbMaxParents)
			shuffle(t)
			if nbMaxParents != -1:
				for var in t:
					while len(var.parents) > nbMaxParents:
						par = var.parents[randint(0,len(var.parents)-1)]
						self.deleteParentVariables(var,[par])
						nbEdgesToDelete -= 1
			
			while nbEdgesToDelete > 0:
				var = self.variables[randint(0,len(self.variables)-1)]
				if len(var.parents) != 0:
					par = var.parents[randint(0,len(var.parents)-1)]
					self.deleteParentVariables(var,[par])
					nbEdgesToDelete -= 1
			
			# create preferences
			for var in self.variables:
				pref = {}
				for i in range(2**len(var.parents)):
					pref[i] = Stats(var,value = randint(0,1))
				var.preferences = pref
	
	def depassParent(self,nbPar):
		t = []
		for var in self.variables:
			if len(var.parents) > nbPar:
				t.append(var)
		return t
	
	# return True if state with var is preferred to state with var', False else
	def preferred(self,rule):
		return self.variables[rule[0]].preferred(rule[1:])
	
	# return the variable which has the correspondant varId
	def getVariable(self, varId):
		for var in self.variables:
			if var.id == varId:
				return var
		return -1
		
	def computeVariablesInformationGain(self,decisionMode):
		for var in self.variables:
			var.updateInformationGain(self.numberOfRules,decisionMode)
		
	def decision(self,decTh,decisionMode):
		tabMax = []
		
		if len(self.candidateVariables) > 0:
			for var in self.candidateVariables:
				if var.time != 0:
					tabMax.append([var.id,var.currentInformationGain])
			if len(tabMax) > 0:
				maxVar = max(tabMax,key=itemgetter(1))
				# tabMax.remove(maxVar)
				# maxVar2 = max(tabMax,key=itemgetter(1))
				
				var = self.getVariable(maxVar[0])
				# var = self.getVariable(maxVar2[0])
				
				if decisionMode == 1:
					# print(maxVar[1], epsilonMcDiarmid(decTh,var.time))
					# if maxVar[1] <=  maxVar2[1] - 2*epsilonMcDiarmid(decTh,var.time):
					# if maxVar[1] > 0.1:
						# print("coucou",maxVar[1])
					# if epsilonMcDiarmid(decTh,var.time) < 0.35:
						# print(epsilonMcDiarmid(decTh,var.time))
					if maxVar[1] > epsilonMcDiarmid(decTh,var.time):
						return True,var
		return False,-1
		
	def addParentNewVersion(self,var,parentVariable,useOffline,numberOfParents,autorizedCycle,decisionMode):
		var.parents.append(parentVariable)
		self.updateCPGraph()
		if self.cycle() and not autorizedCycle:
			var.parents.remove(parentVariable)
			self.updateCPGraph()
		else:
			var.parents.remove(parentVariable)
			if useOffline:
				sub = var.addParentOffline(parentVariable,decisionMode)
				self.numberOfRules = self.numberOfRules - sub
			else:
				if numberOfParents != -1 and len(var.parents)+1 >= numberOfParents:
					self.candidateVariables.remove(var)
				self.numberOfRules = var.addParentOnline(parentVariable,decisionMode,self.numberOfRules)
				# self.numberOfRules = self.numberOfRules - sub + add
				var.updateInformationGain(self.numberOfRules,decisionMode)
			return True
		return False

	def addParent(self,var,useOffline,decisionMode,numberOfParents,autorizedCycle):
		l = []
		for key,value in var.generalTableForMean.items():
			if var.numberOfRules != 0:
				val = value/var.numberOfRules
			else:
				val = 0
			b = True
			for i in range(len(l)):
				if val == l[i][0]:
					l[i][1].append(key)
					b = False
			if b:
				l.append([val,[key]])
		l.sort(key=lambda colonnes: colonnes[0],reverse=True)
		for item in l:
			shuffle(item[1])

		for item in l:
			for it in item[1]:
				var.parents.append(self.getVariable(it))
				self.updateCPGraph()
				if self.cycle() and not autorizedCycle:
					var.parents.remove(self.getVariable(it))
					self.updateCPGraph()
				else:
					var.parents.remove(self.getVariable(it))
					if useOffline:
						sub = var.addParentOffline(self.getVariable(it),decisionMode)
						self.numberOfRules = self.numberOfRules - sub
					else:
						if numberOfParents != -1 and len(var.parents)+1 >= numberOfParents:
							self.candidateVariables.remove(var)
						self.numberOfRules = var.addParentOnline(self.getVariable(it),decisionMode,self.numberOfRules)
						# self.numberOfRules = self.numberOfRules - sub + add
						var.updateInformationGain(self.numberOfRules,decisionMode)
					return True
		var.alreadyTry = True
		self.candidateVariables.remove(var)
		return False
			
	def fitCPNet(self,rule):
		if self.getVariable(rule[0]).preferences[rule[1]].trueRule == rule[2]:
			return True
		return False
		
	def addVariables(self, numberOfParents, numberOfVariables = 1):
		for i in range(numberOfVariables):
			var = Variable(len(self.variables))
			self.variables.append(var)
			if numberOfParents != 0:
				self.candidateVariables.append(var)
		self.updateCPGraph()
		
	def addParentVariables(self,var,listParents,pref = None):
		self.variables[self.variables.index(var)].addParents(listParents,preferences = pref)
		self.updateCPGraph()
	
	def deleteParentVariables(self,var,listParents,pref = None):
		self.variables[self.variables.index(var)].deleteParents(listParents,preferences = pref)
		self.updateCPGraph()
		
	def updateCPGraph(self):
		self.CPGraph = {}
		self.fillCPGraph()
		
	def displayCPNetInfo(self):
		print("This CP-Net",self.name,"has", len(self.variables), "variable(s)")
		for var in self.variables:
			p = ""
			for par in var.parents:
				p += " " + str(par.id)
			print("Var." + str(var.id),"has",len(var.parents),"parents variable(s) :" + p)				
			
	def displayCPNet(self):
		print("This CP-Net",self.name,"has", len(self.variables), "variable(s).")
		noPreferences = True
		for var in self.variables:
			if var.parents == [] and var.preferences:
				noPreferences = False
				print("Var." + str(var.id), ":", var.preferences[-1].trueRule, "is preferred than", int(not(var.preferences[-1].trueRule)))
			if var.parents != []:
				for key in var.preferences.keys():
					parentsVect = fromIntToBin(key,len(var.parents))
					noPreferences = False
					string = "with"
					for i,elt in enumerate(parentsVect):
						if i < len(var.parents):
							string += " Var." + str(var.parents[i].id) + " = " + str(elt)
					print("Var." + str(var.id), string, "as parents :", int(var.preferences[key].trueRule), "is preferred than", int(not(var.preferences[key].trueRule)))
		if noPreferences:
			print("Without any preference yet.")
		
	def fillCPGraph(self):
		for var in self.variables:
			self.CPGraph[var.id] = []
		for var in self.variables:
			for par in var.parents:
				self.CPGraph[par.id].append(var.id)
	
	# return True iff CPGraph has a cycle, False else
	# we delete each "puits" node until we cannot
	def cycle(self):
		CPGraph = self.CPGraph.copy()
		b = True
		while b:
			var = -1
			for v in CPGraph.keys():
				if CPGraph[v] == []:
					var = v
			if var != -1:
				for v in CPGraph.keys():
					if var in CPGraph[v]:
						CPGraph[v].remove(var)
				del CPGraph[var]
			else:
				b = False
		if len(CPGraph) != 0:
			return True
		return False
	
	# rule = [varId,parentsValue,valVar]
	def returnRule(self,flipVar,outcome1,outcome2):
		tab = []
		if flipVar.parents == []:
			return [self.variables[flipVariable(outcome1,outcome2)].id,-1,outcome1[flipVar.id]]
		for par in flipVar.parents:
			tab.append(outcome1[par.id])
		return [self.variables[flipVariable(outcome1,outcome2)].id,fromBinToInt(tab),outcome1[flipVar.id]]
