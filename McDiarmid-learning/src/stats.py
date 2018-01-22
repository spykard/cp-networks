from variable import *


class Stats():
	def __init__(self,var,counterForRule = 0,counterForInversedRule = 0, value = -1):
		self.trueRule = value
		
		self.counterForRule = counterForRule
		self.statsForRuleOne = {}
		self.statsForRuleZero = {}
		for nonPar in var.nonParents:
			self.statsForRuleOne[nonPar] = 0
			self.statsForRuleZero[nonPar] = 0
			
		self.counterForInversedRule = counterForInversedRule
		self.statsForInversedRuleOne = {}
		self.statsForInversedRuleZero = {}
		for nonPar in var.nonParents:
			self.statsForInversedRuleOne[nonPar] = 0
			self.statsForInversedRuleZero[nonPar] = 0
		if self.counterForRule != 0 or self.counterForInversedRule != 0:
			self.setTrueRule()
	
	def setTrueRule(self):
		if self.counterForRule >= self.counterForInversedRule:
			self.trueRule = 1
		else:
			self.trueRule = 0
	
	def addOneToTheCounter(self,whatRule):
		if whatRule == 1:
			self.counterForRule += 1
		else:
			self.counterForInversedRule += 1
		
	def calcMax(self,varId,whatRule,minusOne):
		if minusOne and self.counterForRule + self.counterForInversedRule - 1 != 0:
			return max(self.statsForRuleOne[varId] + self.statsForInversedRuleZero[varId],self.statsForRuleZero[varId] + self.statsForInversedRuleOne[varId])/(self.counterForRule + self.counterForInversedRule - 1)
		if self.counterForRule + self.counterForInversedRule != 0:
			return max(self.statsForRuleOne[varId] + self.statsForInversedRuleZero[varId],self.statsForRuleZero[varId] + self.statsForInversedRuleOne[varId])/(self.counterForRule + self.counterForInversedRule)
		return 0
	
	def display(self):
		print("\ttrue rule:", self.trueRule)
		print("\tcounter rule:", self.counterForRule)
		print("\tcounter inversed rule:", self.counterForInversedRule)
		print("\tstats rule (one):", self.statsForRuleOne)
		print("\tstats rule (zero):", self.statsForRuleZero)
		print("\tstats inversed rule (one):", self.statsForInversedRuleOne)
		print("\tstats inversed rule (zero):", self.statsForInversedRuleZero,"\n")
