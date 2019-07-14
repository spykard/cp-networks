from .variable import *
from random import *
from operator import itemgetter
from math import *

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
	
	# return the variable which has the correspondent varId
	def getVariable(self, varId):
		for var in self.variables:
			if var.id == varId:
				return var
		return -1
		
	def computeVariablesInformationGain(self,decisionMode):
		for var in self.candidateVariables:
			var.updateInformationGain(decisionMode)
		
	def decision(self,decTh,epsilonThreshold,decisionMode,cpt):
		tabMax = []
		if len(self.candidateVariables) > 0:
			if decisionMode == 1:
				for var in self.candidateVariables:
					if var.currentInformationGain != 0:
						tabMax.append([var.id,var.currentInformationGain,var.currentInformationGain*(var.time/self.numberOfRules)])
				if len(tabMax) > 0:
					maxVar = max(tabMax,key=itemgetter(2))
					var = self.getVariable(maxVar[0])
					if maxVar[1] > epsilonMcDiarmid(decTh,var.time):
						return True,var,-1
			
			if decisionMode == 2:
				for var in self.candidateVariables:
					#if var.currentInformationGain != 0:
					if var.cptRule != 0 and var.cptInversedRule != 0:
						for nonPar in var.candidateNonParentVariables:
							if var.currentInformationGainNonParent[nonPar] > 0:
								# tabMax.append([var.id,nonPar,(var.time/self.numberOfRules)*var.currentInformationGainNonParent[nonPar]])
								tabMax.append([var.id,nonPar,var.currentInformationGainNonParent[nonPar]])

				if len(tabMax) > 1:
					maxVar = max(tabMax,key=itemgetter(2))
					var = self.getVariable(maxVar[0])
					varPar = self.getVariable(maxVar[1])
					
					tabMax.remove(max(tabMax,key=itemgetter(2)))
					maxVar2 = max(tabMax,key=itemgetter(2))
					var2 = self.getVariable(maxVar[0])
					varPar2 = self.getVariable(maxVar[1])
					
					# if cpt % 10000 == 0:
						# print(maxVar[2] - maxVar2[2],epsilonMcDiarmid2(decTh,var.time,var2.time,self.numberOfRules))
					# if maxVar[2] - maxVar2[2] > 2*epsilonMcDiarmid2(decTh,var.time,var2.time,self.numberOfRules) or epsilonMcDiarmid2(decTh,var.time,var2.time,self.numberOfRules) < 0.07:
					if maxVar[2] - maxVar2[2] > 2*epsilonMcDiarmid2(decTh,var.time,var2.time,self.numberOfRules) or epsilonMcDiarmid2(decTh,var.time,var2.time,self.numberOfRules) < epsilonThreshold:
					# if maxVar[2] <= maxVar2[2] - 2*epsilonMcDiarmid2(decTh,var.time,var2.time,self.numberOfRules) or epsilonMcDiarmid2(decTh,var.time,var2.time,self.numberOfRules) < epsilonThreshold:
						return True,var,varPar
					# if cpt % 10000 == 0:
						# print(maxVar[2],epsilonMcDiarmid3(decTh,var.time,self.numberOfRules))
					# if maxVar[2] > epsilonMcDiarmid3(decTh,var.time,self.numberOfRules):
						# return True,var,varPar
		return False,-1,-1
		
	def addParentNewVersion(self,var,parentVariable,useOffline,numberOfParents,autorizedCycle,decisionMode):
		var.parents.append(parentVariable)
		self.updateCPGraph()
		if self.cycle() and not autorizedCycle:
			var.parents.remove(parentVariable)
			self.updateCPGraph()
			var.candidateNonParentVariables.remove(parentVariable.id)
			
			if len(var.candidateNonParentVariables) == 0:
				self.candidateVariables.remove(var)
		else:
			var.parents.remove(parentVariable)
			if numberOfParents != -1 and len(var.parents)+1 >= numberOfParents:
				self.candidateVariables.remove(var)
				
				var.candidateNonParentVariables = []
			if useOffline:
				sub = var.addParentOffline(parentVariable,decisionMode)
				self.numberOfRules = self.numberOfRules - sub
			else:
				self.numberOfRules = var.addParentOnline(parentVariable,decisionMode,self.numberOfRules)
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
					var.candidateNonParentVariables.remove(it)
					
					if len(var.candidateNonParentVariables) == 0:
						self.candidateVariables.remove(var)
				else:
					var.parents.remove(self.getVariable(it))
					if numberOfParents != -1 and len(var.parents)+1 >= numberOfParents:
						self.candidateVariables.remove(var)
						var.candidateNonParentVariables = []

					if useOffline:
						sub = var.addParentOffline(self.getVariable(it),decisionMode)
						self.numberOfRules = self.numberOfRules - sub
					else:
						self.numberOfRules = var.addParentOnline(self.getVariable(it),decisionMode,self.numberOfRules)
					return True
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
		
	def updateCandidateNonParentVariables(self):
		for var in self.candidateVariables:
			for nonPar in var.nonParents:
				var.candidateNonParentVariables.append(nonPar)
		
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
				p += " " + str(par.id+1)
			print("Var." + str(var.id+1),"has",len(var.parents),"parents variable(s) :" + p)				
			
	def displayCPNet(self):
		print("This CP-Net",self.name,"has", len(self.variables), "variable(s).")
		noPreferences = True
		for var in self.variables:
			if var.parents == [] and var.preferences:
				noPreferences = False
				print("Var." + str(var.id+1), ":", var.preferences[-1].trueRule, "is preferred than", int(not(var.preferences[-1].trueRule)))
			if var.parents != []:
				for key in var.preferences.keys():
					parentsVect = fromIntToBin(key,len(var.parents))
					noPreferences = False
					string = "with"
					for i,elt in enumerate(parentsVect):
						if i < len(var.parents):
							string += " Var." + str(var.parents[i].id+1) + " = " + str(elt)
					print("Var." + str(var.id+1), string, "as parents :", int(var.preferences[key].trueRule), "is preferred than", int(not(var.preferences[key].trueRule)))
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
