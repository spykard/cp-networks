import math as m
import string as s
from operator import attrgetter
import random
from .utility import *
from .stats import *
	
# a variable consists of
# an id (unique), for instance 2
# a set (list) of parents variables, for instance [A,B]
# an hashmap of hashmaps and counters, for instance {0 -> [0,{1 -> 1/2, 3 -> 1}, 6, {1 -> 2/3, 3 -> 0}, 8],...} which means
# that the rule with the value 0 for parent's variable, c' > c, it appears 6 times and the positive value of the first variable
# appears half of the time, etc...
# nonParents is a table that contains the id of all non parent variables
class Variable:
	def __init__(self, id = -1):
		self.id = id
		self.parents = []
		self.preferences = {}
		self.nonParents = []
		self.generalTableForMean = {}
		self.numberOfRules = 0
		self.candidateNonParentVariables = []
		
		self.cptRule = 0
		self.cptInversedRule = 0
		
		self.currentInformationGain = 0.0
		self.currentInformationGainNonParent = {}
		
		self.time = 0
		
	def __lt__(self,v):
		return self.id < v.id
		
	def printParents(self):
		s = "["
		for par in self.parents:
			s += str(par.id) + ","
		print(s + "]")
		
	# def updateInformationGain(self,decisionMode):
		# self.currentInformationGain = 0
		# sum = 0
		# if decisionMode == 2:
			# sumNonPar = {}
			# for nonPar in self.candidateNonParentVariables:
				# self.currentInformationGainNonParent[nonPar] = 0
				# sumNonPar[nonPar] = 0
		# for pref in self.preferences.values():
			# if pref.counterForRule != 0 and pref.counterForInversedRule != 0:
				# if decisionMode == 1:
					# sum += max(pref.counterForRule, pref.counterForInversedRule)
				# if decisionMode == 2:
					# sum += max(pref.counterForRule, pref.counterForInversedRule)
					# for nonPar in self.candidateNonParentVariables:
						# sumNonPar[nonPar] += max(pref.statsForRuleOne[nonPar] + pref.statsForInversedRuleZero[nonPar],pref.statsForRuleZero[nonPar] + pref.statsForInversedRuleOne[nonPar])
		# self.currentInformationGain = entropy(sum/self.time,(1 - (sum/self.time)))
		# if decisionMode == 2:
			# for nonPar in self.candidateNonParentVariables:
					# self.currentInformationGainNonParent[nonPar] = entropy(sumNonPar[nonPar]/self.time,1 - (sumNonPar[nonPar]/self.time))
					
					
	def updateInformationGain(self,decisionMode):
		self.currentInformationGain = 0		
		if decisionMode == 1:
			sum = 0
			for pref in self.preferences.values():
				if pref.counterForRule != 0 and pref.counterForInversedRule != 0:
					if decisionMode == 1:
						sum += max(pref.counterForRule, pref.counterForInversedRule)
						self.currentInformationGain += ((pref.counterForRule + pref.counterForInversedRule)/self.time) * entropy(pref.counterForRule, pref.counterForInversedRule)
					if decisionMode == 2:
						sum += max(pref.counterForRule, pref.counterForInversedRule)
						for nonPar in self.candidateNonParentVariables:
							sumNonPar[nonPar] += max(pref.statsForRuleOne[nonPar] + pref.statsForInversedRuleZero[nonPar],pref.statsForRuleZero[nonPar] + pref.statsForInversedRuleOne[nonPar])
		if decisionMode == 2:
			entropyVar = 0
			for pref in self.preferences.values():
				entropyVar += ((pref.counterForRule+pref.counterForInversedRule)/self.time)*entropy(pref.counterForRule,pref.counterForInversedRule)
			for nonPar in self.candidateNonParentVariables:
				entropyVarPar = 0
				for pref in self.preferences.values():
					entropyVarPar += ((pref.statsForRuleOne[nonPar] + pref.statsForInversedRuleOne[nonPar])/self.time)*entropy(pref.statsForRuleOne[nonPar],pref.statsForInversedRuleOne[nonPar]) + ((pref.statsForRuleZero[nonPar] + pref.statsForInversedRuleZero[nonPar])/self.time)*entropy(pref.statsForRuleZero[nonPar],pref.statsForInversedRuleZero[nonPar])
				self.currentInformationGainNonParent[nonPar] = entropyVar - entropyVarPar

	def updateCPTable(self,rule,outcome,canUse,decisionMode):
		self.time += 1
		if rule[1] == 1:
			self.cptRule += 1
		else: self.cptInversedRule += 1
		if self.preferences[rule[0]].trueRule == -1:
			self.numberOfRules += 1
		self.preferences[rule[0]].addOneToTheCounter(rule[1])
		if canUse:
			for nonPar in self.candidateNonParentVariables:
				if decisionMode == 1:
					self.generalTableForMean[nonPar] -= self.preferences[rule[0]].calcMax(nonPar,rule[1],True)
				if outcome[nonPar] == 1:
					if rule[1] == 1:
						self.preferences[rule[0]].statsForRuleOne[nonPar] += 1
					else:
						self.preferences[rule[0]].statsForInversedRuleOne[nonPar] += 1
				else:
					if rule[1] == 1:
						self.preferences[rule[0]].statsForRuleZero[nonPar] += 1
					else:
						self.preferences[rule[0]].statsForInversedRuleZero[nonPar] += 1
				if decisionMode == 1:
					self.generalTableForMean[nonPar] += self.preferences[rule[0]].calcMax(nonPar,rule[1],False)
		self.preferences[rule[0]].setTrueRule()
		
	def addParentOffline(self,par,decisionMode):
		oldPreferences = self.preferences.copy()
		self.parents.append(par)
		self.parents.sort()
		self.nonParents.remove(par.id)
		
		self.candidateNonParentVariables.remove(par.id)

		self.cptRule = 0
		self.cptInversedRule = 0
		
		if decisionMode == 2:
			del self.currentInformationGainNonParent[par.id]

		self.preferences = {}
		self.numberOfRules = 0
		self.currentInformationGain = 0.0
		
		sub = 0
		
		self.generalTableForMean = {}
		for nonPar in self.candidateNonParentVariables:
			self.generalTableForMean[nonPar] = 0
		
		for key,value in oldPreferences.items():		
			if key == -1:
				self.preferences[1] = Stats(self,0,0)
				self.preferences[0] = Stats(self,0,0)
				
				sub += oldPreferences[-1].counterForRule + oldPreferences[-1].counterForInversedRule
				
				for nonPar in self.candidateNonParentVariables:
					self.preferences[1].statsForRuleOne[nonPar] = 0
					self.preferences[1].statsForRuleZero[nonPar] = 0
					self.preferences[1].statsForInversedRuleOne[nonPar] = 0
					self.preferences[1].statsForInversedRuleZero[nonPar] = 0
					
					self.preferences[0].statsForRuleOne[nonPar] = 0
					self.preferences[0].statsForRuleZero[nonPar] = 0
					self.preferences[0].statsForInversedRuleOne[nonPar] = 0
					self.preferences[0].statsForInversedRuleZero[nonPar] = 0
			else:
				oldVector = fromIntToBin(key,len(self.parents)-1)
				indexOfNewParentVariable = self.parents.index(par)
				
				newVector1 = list(oldVector)
				newVector1.insert(indexOfNewParentVariable,1)
				newVector0 = list(oldVector)
				newVector0.insert(indexOfNewParentVariable,0)
				
				self.preferences[fromBinToInt(newVector1)] = Stats(self,0,0)
				self.preferences[fromBinToInt(newVector0)] = Stats(self,0,0)
				
				sub += oldPreferences[key].counterForRule + oldPreferences[key].counterForInversedRule
				
				for nonPar in self.candidateNonParentVariables:
					self.preferences[fromBinToInt(newVector1)].statsForRuleOne[nonPar] = 0
					self.preferences[fromBinToInt(newVector1)].statsForRuleZero[nonPar] = 0
					self.preferences[fromBinToInt(newVector1)].statsForInversedRuleOne[nonPar] = 0
					self.preferences[fromBinToInt(newVector1)].statsForInversedRuleZero[nonPar] = 0
					
					self.preferences[fromBinToInt(newVector0)].statsForRuleOne[nonPar] = 0
					self.preferences[fromBinToInt(newVector0)].statsForRuleZero[nonPar] = 0
					self.preferences[fromBinToInt(newVector0)].statsForInversedRuleOne[nonPar] = 0
					self.preferences[fromBinToInt(newVector0)].statsForInversedRuleZero[nonPar] = 0
		return sub

	def addParentOnline(self,par,decisionMode,totalRules):
		oldPreferences = self.preferences.copy()
		self.parents.append(par)
		self.parents.sort()
		self.nonParents.remove(par.id)
		
		self.candidateNonParentVariables.remove(par.id)

		self.cptRule = 0
		self.cptInversedRule = 0
		
		if decisionMode == 2:
			del self.currentInformationGainNonParent[par.id]
		self.preferences = {}
		self.numberOfRules = 0
		self.currentInformationGain = 0.0
		self.time = 0
		
		sub = 0
		add = 0
				
		if decisionMode == 1:
			self.generalTableForMean = {}
			for nonPar in self.candidateNonParentVariables:
				self.generalTableForMean[nonPar] = 0
				
		
		for key,value in oldPreferences.items():
			if key == -1:
				self.preferences[1] = Stats(self,oldPreferences[-1].statsForRuleOne[par.id],oldPreferences[-1].statsForInversedRuleOne[par.id])
				self.preferences[0] = Stats(self,oldPreferences[-1].statsForRuleZero[par.id],oldPreferences[-1].statsForInversedRuleZero[par.id])
				
				self.time += self.preferences[1].counterForRule + self.preferences[1].counterForInversedRule + self.preferences[0].counterForRule + self.preferences[1].counterForInversedRule
				
				self.cptRule += self.preferences[1].counterForRule + self.preferences[0].counterForRule
				self.cptInversedRule += self.preferences[1].counterForInversedRule + self.preferences[1].counterForInversedRule
				
				if oldPreferences[-1].statsForRuleOne[par.id] + oldPreferences[-1].statsForInversedRuleOne[par.id] != 0:
					self.numberOfRules += 1
				if oldPreferences[-1].statsForRuleZero[par.id] + oldPreferences[-1].statsForInversedRuleZero[par.id] != 0:
					self.numberOfRules += 1
				
				sub += oldPreferences[-1].counterForRule + oldPreferences[-1].counterForInversedRule
				add += oldPreferences[-1].statsForRuleOne[par.id] + oldPreferences[-1].statsForInversedRuleOne[par.id] + oldPreferences[-1].statsForRuleZero[par.id] + oldPreferences[-1].statsForInversedRuleZero[par.id]
				
				for nonPar in self.candidateNonParentVariables:
					self.preferences[1].statsForRuleOne[nonPar] = max(oldPreferences[-1].statsForRuleOne[nonPar] - oldPreferences[-1].counterForRule + oldPreferences[-1].statsForRuleOne[par.id],0)
					self.preferences[1].statsForRuleZero[nonPar] = max(oldPreferences[-1].statsForRuleZero[nonPar] - oldPreferences[-1].counterForRule + oldPreferences[-1].statsForRuleOne[par.id],0)
					self.preferences[1].statsForInversedRuleOne[nonPar] = max(oldPreferences[-1].statsForInversedRuleOne[nonPar] - oldPreferences[-1].counterForInversedRule + oldPreferences[-1].statsForInversedRuleOne[par.id],0)
					self.preferences[1].statsForInversedRuleZero[nonPar] = max(oldPreferences[-1].statsForInversedRuleZero[nonPar] - oldPreferences[-1].counterForInversedRule + oldPreferences[-1].statsForInversedRuleOne[par.id],0)
					
					self.preferences[0].statsForRuleOne[nonPar] = max(oldPreferences[-1].statsForRuleOne[nonPar] - oldPreferences[-1].counterForRule + oldPreferences[-1].statsForRuleZero[par.id],0)
					self.preferences[0].statsForRuleZero[nonPar] = max(oldPreferences[-1].statsForRuleZero[nonPar] - oldPreferences[-1].counterForRule + oldPreferences[-1].statsForRuleZero[par.id],0)
					self.preferences[0].statsForInversedRuleOne[nonPar] = max(oldPreferences[-1].statsForInversedRuleOne[nonPar] - oldPreferences[-1].counterForInversedRule + oldPreferences[-1].statsForInversedRuleZero[par.id],0)
					self.preferences[0].statsForInversedRuleZero[nonPar] = max(oldPreferences[-1].statsForInversedRuleZero[nonPar] - oldPreferences[-1].counterForInversedRule + oldPreferences[-1].statsForInversedRuleZero[par.id],0)
				
					if decisionMode == 1:
						self.generalTableForMean[nonPar] += self.preferences[1].calcMax(nonPar,1,False) + self.preferences[0].calcMax(nonPar,1,False)
			else:
				oldVector = fromIntToBin(key,len(self.parents)-1)
				indexOfNewParentVariable = self.parents.index(par)
				
				newVector1 = list(oldVector)
				newVector1.insert(indexOfNewParentVariable,1)
				newVector0 = list(oldVector)
				newVector0.insert(indexOfNewParentVariable,0)
				
				self.preferences[fromBinToInt(newVector1)] = Stats(self,oldPreferences[key].statsForRuleOne[par.id],oldPreferences[key].statsForInversedRuleOne[par.id])
				self.preferences[fromBinToInt(newVector0)] = Stats(self,oldPreferences[key].statsForRuleZero[par.id],oldPreferences[key].statsForInversedRuleZero[par.id])
				
				self.time += self.preferences[fromBinToInt(newVector1)].counterForRule + self.preferences[fromBinToInt(newVector1)].counterForInversedRule + self.preferences[fromBinToInt(newVector0)].counterForRule + self.preferences[fromBinToInt(newVector0)].counterForInversedRule
				
				self.cptRule += self.preferences[fromBinToInt(newVector1)].counterForRule + self.preferences[fromBinToInt(newVector0)].counterForRule
				self.cptInversedRule += self.preferences[fromBinToInt(newVector1)].counterForInversedRule + self.preferences[fromBinToInt(newVector0)].counterForInversedRule
				
				if oldPreferences[key].statsForRuleOne[par.id] + oldPreferences[key].statsForInversedRuleOne[par.id] != 0:
					self.numberOfRules += 1
				if oldPreferences[key].statsForRuleZero[par.id] + oldPreferences[key].statsForInversedRuleZero[par.id] != 0:
					self.numberOfRules += 1
				
				sub += oldPreferences[key].counterForRule + oldPreferences[key].counterForInversedRule
				add += oldPreferences[key].statsForRuleOne[par.id] + oldPreferences[key].statsForInversedRuleOne[par.id] + oldPreferences[key].statsForRuleZero[par.id] + oldPreferences[key].statsForInversedRuleZero[par.id]
				
				for nonPar in self.candidateNonParentVariables:
					self.preferences[fromBinToInt(newVector1)].statsForRuleOne[nonPar] = max(oldPreferences[key].statsForRuleOne[nonPar] - oldPreferences[key].counterForRule + oldPreferences[key].statsForRuleOne[par.id],0)
					self.preferences[fromBinToInt(newVector1)].statsForRuleZero[nonPar] = max(oldPreferences[key].statsForRuleZero[nonPar] - oldPreferences[key].counterForRule + oldPreferences[key].statsForRuleOne[par.id],0)
					self.preferences[fromBinToInt(newVector1)].statsForInversedRuleOne[nonPar] = max(oldPreferences[key].statsForInversedRuleOne[nonPar] - oldPreferences[key].counterForInversedRule + oldPreferences[key].statsForInversedRuleOne[par.id],0)
					self.preferences[fromBinToInt(newVector1)].statsForInversedRuleZero[nonPar] = max(oldPreferences[key].statsForInversedRuleZero[nonPar] - oldPreferences[key].counterForInversedRule + oldPreferences[key].statsForInversedRuleOne[par.id],0)
					
					self.preferences[fromBinToInt(newVector0)].statsForRuleOne[nonPar] = max(oldPreferences[key].statsForRuleOne[nonPar] - oldPreferences[key].counterForRule + oldPreferences[key].statsForRuleZero[par.id],0)
					self.preferences[fromBinToInt(newVector0)].statsForRuleZero[nonPar] = max(oldPreferences[key].statsForRuleZero[nonPar] - oldPreferences[key].counterForRule + oldPreferences[key].statsForRuleZero[par.id],0)
					self.preferences[fromBinToInt(newVector0)].statsForInversedRuleOne[nonPar] = max(oldPreferences[key].statsForInversedRuleOne[nonPar] - oldPreferences[key].counterForInversedRule + oldPreferences[key].statsForInversedRuleZero[par.id],0)
					self.preferences[fromBinToInt(newVector0)].statsForInversedRuleZero[nonPar] = max(oldPreferences[key].statsForInversedRuleZero[nonPar] - oldPreferences[key].counterForInversedRule + oldPreferences[key].statsForInversedRuleZero[par.id],0)
				
					if decisionMode == 1:
						self.generalTableForMean[nonPar] += self.preferences[fromBinToInt(newVector1)].calcMax(nonPar,1,False) + self.preferences[fromBinToInt(newVector0)].calcMax(nonPar,1,False)
		
		newTotalRules = totalRules - sub + add

		return newTotalRules

	def valueOfParents(self,outcome):
		tab = []
		for par in self.parents:
			tab.append(outcome[par.id])
		return fromBinToInt(tab)

	def printPreferences(self):
		print("preferences for variable " + str(self.id) + ":")
		for key,value in self.preferences.items():
			print("parents value: " + str(key))
			value.display()

	# return True if rule (of the form [valParents,valVar]) corresponds to an existent rule for the current variable
	def preferred(self,rule):
		if self.preferences[rule[0]].trueRule == rule[1]:
			return True
		return False
	
	# refresh conditionals preferences of current variable
	def setPreferences(self, preferences):
		self.preferences = {}
		if preferences:
			for pref in preferences:
				self.preferences[fromBinToInt(pref[:-1])] = pref[-1]
				
	def deleteParents(self,listParents,preferences):
		for par in listParents:
			if par in self.parents:
				self.parents.remove(par)
		self.setPreferences(preferences)
		
	def addParents(self,listParents,preferences):
		for par in listParents:
			self.parents.append(par)
		self.parents.sort()
		self.setPreferences(preferences)
