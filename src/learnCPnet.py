from .CPnet import *
from .database import *
import time
from random import *
from math import *

def learningCPNetOnline(data,dataTestForConv,numberOfVar,dtBis,nbOfParents,lenOfFold,convergence,convergenceAccuracyOnline,noise,computationTimeOnline,iterationTime,decisionMode,autorizedCycle):
	N = {}
	for n in noise:
		shuffle(data[n])
		
		timeBefore = time.clock()
		
		# initialization
		N[n] = CPNet(name = "N")
		N[n].addVariables(numberOfParents = nbOfParents, numberOfVariables = numberOfVar)
		
		for var in N[n].variables:
			for i in range(len(N[n].variables)):
				if var.id != i:
					var.nonParents.append(i)
					var.candidateNonParentVariables.append(i)
					
					var.generalTableForMean[i] = 0
			var.preferences[-1] = Stats(var,0,0)
			for nonPar in var.candidateNonParentVariables:
				var.currentInformationGainNonParent[nonPar] = 0
		
		# learning procedure
		cpt = 0
		for comparison in data[n]:
			iterationTimeBefore = time.clock()
			
			swapVariable = N[n].getVariable(comparison[2])
			rule = N[n].returnRule(swapVariable,comparison[0],comparison[1])[1:]
			N[n].numberOfRules += 1

			swapVariable.updateCPTable(rule,comparison[0],swapVariable in N[n].candidateVariables,decisionMode)
			if swapVariable in N[n].candidateVariables:
				swapVariable.updateInformationGain(decisionMode)
			
			# McDiarmid bound
			if decisionMode == 1:
				dec,candVariable = N[n].decision(dtBis,decisionMode,cpt)[:2]
				if dec and N[n].addParent(candVariable,False,decisionMode,nbOfParents,autorizedCycle):
					print("\t\t" + str(cpt + 1) + "th comparison:\t\t\tvariable " + str(candVariable.id + 1) + " receives a new parent variable...")
			
			# entropy for couple of variables
			if decisionMode == 2:
				dec,candVariable,candParVariable = N[n].decision(dtBis,decisionMode,cpt)
				if dec and N[n].addParentNewVersion(candVariable,candParVariable,False,nbOfParents,autorizedCycle,decisionMode):
					print("\t\t" + str(cpt + 1) + "th comparison:\t\t\tvariable " + str(candVariable.id + 1) + " receives the parent variable " + str(candParVariable.id +1) + "...")
				
			iterationTimeAfter = time.clock()
			iterationTime[n].append(iterationTimeAfter - iterationTimeBefore)
			
			if convergence:
				correctComp = 0
				for comparison in dataTestForConv[0]:
					if N[n].fitCPNet(N[n].returnRule(N[n].getVariable(comparison[2]),comparison[0],comparison[1])):
						correctComp += 1
				convergenceAccuracyOnline[n][cpt].append(correctComp/lenOfFold*100)
			cpt += 1
			
		timeAfter = time.clock()
		computationTimeOnline[n].append(timeAfter - timeBefore)

	return N
	
def learningCPNetOffline(data,dataTestForConv,numberOfVar,nbOfParents,lenOfFold,convergence,convergenceAccuracyOffline,noise,computationTimeOffline,decisionMode,autorizedCycle):
	N = {}
	for n in noise:
		
		timeBefore = time.clock()
		
		# initialization
		N[n] = CPNet(name = "N")
		N[n].addVariables(numberOfParents = nbOfParents, numberOfVariables = numberOfVar)
		if decisionMode == 2:
			N[n].updateCandidateNonParentVariables()
		
		listOfVariables = {}
		
		# create non parent variables
		for var in N[n].variables:
			for i in range(len(N[n].variables)):
				if var.id != i:
					var.nonParents.append(i)
					var.candidateNonParentVariables.append(i)
					
					var.generalTableForMean[i] = 0
			var.preferences[-1] = Stats(var,0,0)
			for nonPar in var.candidateNonParentVariables:
				var.currentInformationGainNonParent[nonPar] = 0
		
		# learning procedure		
		finish = False
		
		cpt = 0
		
		while not finish:
			N[n].numberOfRules = 0
			
			# browse the database
			for comparison in data[n]:
				swapVariable = N[n].getVariable(comparison[2])
				rule = N[n].returnRule(swapVariable,comparison[0],comparison[1])[1:]
				swapVariable.updateCPTable(rule,comparison[0],swapVariable in N[n].candidateVariables,decisionMode)
				N[n].numberOfRules += 1
			
			# compute accuracy in case of convergence
			if convergence:
				correctComp = 0
				for comparison in dataTestForConv[0]:
					if N[n].fitCPNet(N[n].returnRule(N[n].getVariable(comparison[2]),comparison[0],comparison[1])):
						correctComp += 1
				
				if len(convergenceAccuracyOffline[n]) <= cpt:
					convergenceAccuracyOffline[n].append([correctComp/lenOfFold*100])
				else:
					convergenceAccuracyOffline[n][cpt].append(correctComp/lenOfFold*100)
				cpt += 1
			
			# compute information gain variables
			N[n].computeVariablesInformationGain(decisionMode)
			
			# looking for the best information gain
			if decisionMode == 1:
				varEntr = []
				for var in N[n].candidateVariables:
					b = True
					for i in range(len(varEntr)):
						if varEntr[i][0] == var.currentInformationGain*(var.time/N[n].numberOfRules):
							b = False
							varEntr[i][1].append(var.id)
							break
					if b == True:
						varEntr.append([var.currentInformationGain*(var.time/N[n].numberOfRules),[var.id]])
				
				# choose a random variable among those which have the best entropy
				varEntr.sort(key=lambda colonnes: colonnes[0],reverse=True)
				for item in varEntr:
					shuffle(item[1])
				
				# if all variables are pure, we stop
				if len(varEntr) == 0 or varEntr[0][0] == 0:
					finish = True
				# otherwise, we need to find a new parent variable (if it exists)
				else:
					finish = True
					for item in varEntr:
						for it in item[1]:
							if N[n].getVariable(it) in N[n].candidateVariables and (len(N[n].getVariable(it).parents) < nbOfParents or nbOfParents == -1):
								if N[n].addParent(N[n].getVariable(it),True,decisionMode,nbOfParents,autorizedCycle):
									print("\t\t\t\t\tvariable " + str(it + 1) + " receives a new parent variable...")
									finish = False
									break
						if not finish:
							break
			
			# use entropy for searching a couple (conditioned,parent) variables
			if decisionMode == 2:
				tabInformationGain = []
				finish = True
				for var in N[n].variables:
					if len(var.parents) < nbOfParents or nbOfParents == -1:
						finish = False
						for nonPar in var.candidateNonParentVariables:
							# tabInformationGain.append([(var.time/N[n].numberOfRules)*var.currentInformationGainNonParent[nonPar],var.id,nonPar])
							tabInformationGain.append([var.currentInformationGainNonParent[nonPar],var.id,nonPar])
				if not finish:
					tabInformationGain.sort(key=lambda colonnes: colonnes[0],reverse=True)
					finish = True
					for elt in tabInformationGain:
						if elt[0] < 0: print(elt[0])
						if N[n].addParentNewVersion(N[n].getVariable(elt[1]),N[n].getVariable(elt[2]),True,nbOfParents,autorizedCycle,decisionMode):
							print("\t\t\t\t\tvariable " + str(elt[1] + 1) + " receives the parent variable " + str(elt[2] +1) + "...")
							finish = False
							break							
						
		timeAfter = time.clock()
		computationTimeOffline[n].append(timeAfter - timeBefore)

	return N
	
def generalProcedure(m,fileName,numberOfComparisons,no,v,b,numberOfParents1,numberOfParents2,smooth,smooth2,dtBis,convergence,online,offline,decisionMode,data,autorizedCycle):
	if smooth == 0:
		smooth = 1
	if smooth2 == 0:
		smooth2 = 1
		
	if m == 1:
		smooth = 1
	
	convergenceAccuracyOnline = {}
	computationTimeOnline = {}
	iterationTime = {}
	accOnline = {}
	accNoiseOnline = {}
	
	convergenceAccuracyOffline = {}
	computationTimeOffline = {}
	accOffline = {}
	accNoiseOffline = {}
	
	averageCycleSize2 = {}
	for n in no:
		averageCycleSize2[n] = 0
	
	maxAccuracyBag = -1

	print()
	
	for i in range(smooth):
		if data == None:
			if numberOfComparisons == -1 and m == 2:
				numberOfComparisons = int(input("Enter a number of comparaisons: "))
				print()
			dataset = Database(i+1, smooth, mode = m, filename = fileName, nC = numberOfComparisons, noise = no, nbV = v,lb = b,nbP = numberOfParents1, k = smooth2)
		else:
			dataset = data
			
		# for n in no:
			# averageCycleSize2[n] += dataset.percentageOfCycleSize2[n]
		
		if i == 0:
			for n in no:
				if online:
					convergenceAccuracyOnline[n] = [[] for i in range(dataset.lenOfFold)]
					computationTimeOnline[n] = []
					iterationTime[n] = []
					accOnline[n] = []
					accNoiseOnline[n] = []
				if offline:
					convergenceAccuracyOffline[n] = []
					computationTimeOffline[n] = []
					accOffline[n] = []
					accNoiseOffline[n] = []
		
		for j in range(smooth2):
			dataTest = {}
			dataTrain = {}
			for n in no:
				if smooth2 == 1:
					dataTest[n] = dataTrain[n] = [swap for swap in dataset.dataFold[0][n]]
				else:
					dataTest[n] = [swap for swap in dataset.dataFold[j][n]]
					dataTrain[n] = []
					for other in range(smooth2):
						if other != j:
							dataTrain[n].extend(dataset.dataFold[other][n])
			if offline:
				if online:
					print("\tsubstep " + str(2 * j + 1) + "/" + str(2*smooth2) + ":\t\t\tOFFLINE learning phase in progress...")
				else:
					print("\tsubstep " + str(j + 1) + "/" + str(smooth2) + ":\t\t\tOFFLINE learning phase in progress...")
				learnedCPNetOffline = learningCPNetOffline(dataTrain,dataTest,dataset.numberOfAttributes,numberOfParents2,dataset.lenOfFold,convergence,convergenceAccuracyOffline,no,computationTimeOffline,decisionMode,autorizedCycle)
		
			if online:
				if offline:
					print("\tsubstep " + str(2 * j + 2) + "/" + str(2*smooth2) + ":\t\t\tONLINE learning phase in progress...")
				else:
					print("\tsubstep " + str(j + 1) + "/" + str(smooth2) + ":\t\t\tONLINE learning phase in progress...")
				learnedCPNetOnline = learningCPNetOnline(dataTrain,dataTest,dataset.numberOfAttributes,dtBis,numberOfParents2,dataset.lenOfFold,convergence,convergenceAccuracyOnline,no,computationTimeOnline,iterationTime,decisionMode,autorizedCycle)
			
			print("\t\t\t\t\ttest phase in progress...")
			for n in no:
				correctCompOnline = 0
				correctCompOffline = 0
				for comparison in dataTest[n]:
					if online and learnedCPNetOnline[n].fitCPNet(learnedCPNetOnline[n].returnRule(learnedCPNetOnline[n].getVariable(comparison[2]),comparison[0],comparison[1])):
						correctCompOnline += 1
					if offline and learnedCPNetOffline[n].fitCPNet(learnedCPNetOffline[n].returnRule(learnedCPNetOffline[n].getVariable(comparison[2]),comparison[0],comparison[1])):
						correctCompOffline += 1
						
				correctCompNoiseOnline = 0
				correctCompNoiseOffline = 0
				for comparison in dataTest[0]:
					if online and learnedCPNetOnline[n].fitCPNet(learnedCPNetOnline[n].returnRule(learnedCPNetOnline[n].getVariable(comparison[2]),comparison[0],comparison[1])):
						correctCompNoiseOnline += 1
					if offline and learnedCPNetOffline[n].fitCPNet(learnedCPNetOffline[n].returnRule(learnedCPNetOffline[n].getVariable(comparison[2]),comparison[0],comparison[1])):
						correctCompNoiseOffline += 1
				
				if online:
					accOnline[n].append(correctCompOnline/dataset.lenOfFold*100)
					accNoiseOnline[n].append(correctCompNoiseOnline/dataset.lenOfFold*100)
				if offline:
					accOffline[n].append(correctCompOffline/dataset.lenOfFold*100)
					accNoiseOffline[n].append(correctCompNoiseOffline/dataset.lenOfFold*100)
	
	totalSmooth = smooth*smooth2
	
	meanAccOnline = {}
	meanAccNoiseOnline = {}
	meanTOnline = {}
	meanIT = {}
	sdAOnline = {}
	sdANoiseOnline = {}
	sdTOnline = {}
	sdIT = {}

	meanAccOffline = {}
	meanAccNoiseOffline = {}
	meanTOffline = {}
	sdAOffline = {}
	sdANoiseOffline = {}
	sdTOffline = {}
	
	for n in no:
	
		averageCycleSize2[n] /= smooth
	
		if online:
			meanAccOnline[n] = 0
			meanAccNoiseOnline[n] = 0
			meanTOnline[n] = 0
			meanIT[n] = 0
			sdAOnline[n] = 0
			sdANoiseOnline[n] = 0
			sdTOnline[n] = 0
			sdIT[n] = 0
		if offline:
			meanAccOffline[n] = 0
			meanAccNoiseOffline[n] = 0
			meanTOffline[n] = 0
			sdAOffline[n] = 0
			sdANoiseOffline[n] = 0
			sdTOffline[n] = 0
		
		if online:
			for i in range(totalSmooth):
				meanAccOnline[n] += accOnline[n][i]
				meanAccNoiseOnline[n] += accNoiseOnline[n][i]
				meanTOnline[n] += computationTimeOnline[n][i]
			meanAccOnline[n] /= totalSmooth
			meanAccNoiseOnline[n] /= totalSmooth
			meanTOnline[n] /= totalSmooth
			for i in range(totalSmooth):
				sdAOnline[n] += (accOnline[n][i] - meanAccOnline[n])**2
				sdANoiseOnline[n] += (accNoiseOnline[n][i] - meanAccNoiseOnline[n])**2
				sdTOnline[n] += (computationTimeOnline[n][i] - meanTOnline[n])**2
			if totalSmooth != 1:
				sdAOnline[n] /= (totalSmooth - 1)
				sdAOnline[n] = sqrt(sdAOnline[n])
				sdANoiseOnline[n] /= (totalSmooth - 1)
				sdANoiseOnline[n] = sqrt(sdANoiseOnline[n])
				sdTOnline[n] /= (totalSmooth - 1)
				sdTOnline[n] = sqrt(sdTOnline[n])
			
		if offline:
			for i in range(totalSmooth):
				meanAccOffline[n] += accOffline[n][i]
				meanAccNoiseOffline[n] += accNoiseOffline[n][i]
				meanTOffline[n] += computationTimeOffline[n][i]
			meanAccOffline[n] /= totalSmooth
			meanAccNoiseOffline[n] /= totalSmooth
			meanTOffline[n] /= totalSmooth
			for i in range(totalSmooth):
				sdAOffline[n] += (accOffline[n][i] - meanAccOffline[n])**2
				sdANoiseOffline[n] += (accNoiseOffline[n][i] - meanAccNoiseOffline[n])**2
				sdTOffline[n] += (computationTimeOffline[n][i] - meanTOffline[n])**2
			if totalSmooth != 1:
				sdAOffline[n] /= (totalSmooth - 1)
				sdAOffline[n] = sqrt(sdAOffline[n])
				sdANoiseOffline[n] /= (totalSmooth - 1)
				sdANoiseOffline[n] = sqrt(sdANoiseOffline[n])
				sdTOffline[n] /= (totalSmooth - 1)
				sdTOffline[n] = sqrt(sdTOffline[n])

	meanConvergenceAccuracyOnline = {}
	sdConvergenceAccuracyOnline = {}
	meanConvergenceAccuracyOffline = {}
	sdConvergenceAccuracyOffline = {}
	
	if convergence:
		if offline:
			maxLenIt = -1
			for n in no:
				if len(convergenceAccuracyOffline[n])>maxLenIt:
					maxLenIt = len(convergenceAccuracyOffline[n])
			for n in no:
				lastIt = convergenceAccuracyOffline[n][-1]
				while len(convergenceAccuracyOffline[n]) < maxLenIt:
					convergenceAccuracyOffline[n].append(lastIt)
			
		for n in no:
			if online:
				meanConvergenceAccuracyOnline[n] = [0 for i in range(dataset.lenOfFold)]
				sdConvergenceAccuracyOnline[n] = [0 for i in range(dataset.lenOfFold)]
				for j in range(len(meanConvergenceAccuracyOnline[n])):
					for i in range(totalSmooth):
						meanConvergenceAccuracyOnline[n][j] += convergenceAccuracyOnline[n][j][i]
					meanConvergenceAccuracyOnline[n][j] /= totalSmooth
					for i in range(totalSmooth):
						sdConvergenceAccuracyOnline[n][j] += (convergenceAccuracyOnline[n][j][i] - meanConvergenceAccuracyOnline[n][j])**2
					if totalSmooth != 1:
						sdConvergenceAccuracyOnline[n][j] /= (totalSmooth - 1)
						sdConvergenceAccuracyOnline[n][j] = sqrt(sdConvergenceAccuracyOnline[n][j])
						
			if offline:
				meanConvergenceAccuracyOffline[n] = [0 for i in range(len(convergenceAccuracyOffline[n]))]
				sdConvergenceAccuracyOffline[n] = [0 for i in range(len(convergenceAccuracyOffline[n]))]
				for j in range(len(meanConvergenceAccuracyOffline[n])):
					for i in range(len(convergenceAccuracyOffline[n][j])):
						meanConvergenceAccuracyOffline[n][j] += convergenceAccuracyOffline[n][j][i]
					meanConvergenceAccuracyOffline[n][j] /= len(convergenceAccuracyOffline[n][j])
					for i in range(len(convergenceAccuracyOffline[n][j])):
						sdConvergenceAccuracyOffline[n][j] += (convergenceAccuracyOffline[n][j][i] - meanConvergenceAccuracyOffline[n][j])**2
					if len(convergenceAccuracyOffline[n][j]) != 1:
						sdConvergenceAccuracyOffline[n][j] /= (len(convergenceAccuracyOffline[n][j]) - 1)
						sdConvergenceAccuracyOffline[n][j] = sqrt(sdConvergenceAccuracyOffline[n][j])
	
	print()
	if online:
		print("We obtain the following last ONLINE learned CP-Net:")
		# learnedCPNetOnline.displayCPNet()
		learnedCPNetOnline[no[0]].displayCPNetInfo()
		print()
	if offline:
		print("We obtain the following last OFFLINE learned CP-Net:")
		# learnedCPNetOffline.displayCPNet()
		learnedCPNetOffline[no[0]].displayCPNetInfo()
		print()
	
	return averageCycleSize2,meanAccOnline,sdAOnline,meanAccOffline,sdAOffline,meanTOnline,sdTOnline,meanIT,sdIT,meanTOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,dataset.lenOfFold,dataset.numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline





def displayParameters(modeForDatasetGeneration,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,lenOfFold,numberOfAttributes,online):
	if modeForDatasetGeneration == 1:
		if online:
			return "For the file " + nameOfFile + " (number of comparisons = " + str(lenOfFold) + " per fold, number of variables = " + str(numberOfAttributes) + "),\nnoise = " + str(percentageOfNoise) + "% of the database,\nwith " + str(numberOfParentsForLearnedCPNet) + " parents in the learned CPnet,\n" + str(numberOfRoundsForFileGeneration) + " x " + str(numberOfRoundsForLearningProcedure) + " folds,\ndelta = " + str(decisionThresholdBis) + ".\n"
		else:
			return "For the file " + nameOfFile + " (number of comparisons = " + str(lenOfFold) + " per fold, number of variables = " + str(numberOfAttributes) + "),\nnoise = " + str(percentageOfNoise) + "% of the database,\nwith " + str(numberOfParentsForLearnedCPNet) + " parents in the learned CPnet,\n" + str(numberOfRoundsForFileGeneration) + " x " + str(numberOfRoundsForLearningProcedure) + " folds.\n"
	if modeForDatasetGeneration == 2:
		if online:
			return "For a random database (number of comparisons = " + str(lenOfFold) + " per fold),\ngenerate from a random CPnet (number of variables = " + str(numberOfAttributes) + ", number of parents = " + str(numberOfParentsForTargetCPNet) + ", lambda = " + str(numberOfEdgesLambda) + "),\nnoise = " + str(percentageOfNoise) + "% of the database,\nwith " + str(numberOfParentsForLearnedCPNet) + " parents in the learned CPnet,\n" + str(numberOfRoundsForFileGeneration) + " x " + str(numberOfRoundsForLearningProcedure) + " folds,\ndelta = " + str(decisionThresholdBis) + ".\n"
		else:
			return "For a random database (number of comparisons = " + str(lenOfFold) + " per fold),\ngenerate from a random CPnet (number of variables = " + str(numberOfAttributes) + ", number of parents = " + str(numberOfParentsForTargetCPNet) + ", lambda = " + str(numberOfEdgesLambda) + "),\nnoise = " + str(percentageOfNoise) + "% of the database,\nwith " + str(numberOfParentsForLearnedCPNet) + " parents in the learned CPnet,\n" + str(numberOfRoundsForFileGeneration) + " x " + str(numberOfRoundsForLearningProcedure) + " folds.\n"
		
def displayResults(modeForDatasetGeneration,averageCycleSize2,percentageOfNoise,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOffline,lenOfFold,online,offline,text):
	s = text + ""
	if percentageOfNoise != [0]:
		for n in percentageOfNoise:
			s += "\n"
			if online:
				s += "For noise = " + str(n) + "% (" + str(round(averageCycleSize2[n],2)) + "% of cycles of size 2),\nwe obtain for the ONLINE version:\n" + str(round(aOnline[n],2)) + "% of agreement *" + str(int(aOnline[n]/100*lenOfFold)) + "/" + str(lenOfFold) + " comparisons* (sd = " + str(round(sdAOnline[n],2)) + "%),\naccuracy for unnoised dataset: " + str(meanAccNoiseOnline[n]) + "% (difference with actual noised dataset: " + str(round(meanAccNoiseOnline[0] - meanAccNoiseOnline[n],1)) + "),\ncomputation takes " + str(round(tOnline[n],4)) + " seconds (sd = " + str(round(sdTOnline[n],4)) + " seconds),\nthe computation of one iteration takes " + str(round(meanIT[n]*1000,4)) + " milliseconds (sd = " + str(round(sdIT[n]*1000,4)) + " milliseconds).\n"
			if offline:
				s += "For noise = " + str(n) + "% (" + str(round(averageCycleSize2[n],2)) + "% of cycles of size 2),\nwe obtain for the OFFLINE version:\n" + str(round(aOffline[n],2)) + "% of agreement *" + str(int(aOffline[n]/100*lenOfFold)) + "/" + str(lenOfFold) + " comparisons* (sd = " + str(round(sdAOffline[n],2)) + "%),\naccuracy for unnoised dataset: " + str(meanAccNoiseOffline[n]) + "% (difference with actual noised dataset: " + str(round(meanAccNoiseOffline[0] - meanAccNoiseOffline[n],1)) + "),\ncomputation takes " + str(round(tOffline[n],4)) + " seconds (sd = " + str(round(sdTOffline[n],4)) + " seconds).\n"
	else:
		
		if online:
			s += "We obtain for the ONLINE version:\n" + str(round(aOnline[0],2)) + "% of agreement *" + str(int(aOnline[0]/100*lenOfFold)) + "/" + str(lenOfFold) + " comparisons* (sd = " + str(round(sdAOnline[0],2)) + "%),\ncomputation takes " + str(round(tOnline[0],4)) + " seconds (sd = " + str(round(sdTOnline[0],4)) + " seconds),\nthe computation of one iteration takes " + str(round(meanIT[0]*1000,4)) + " milliseconds (sd = " + str(round(sdIT[0]*1000,4)) + " milliseconds).\n"
		if offline:
			s += "We obtain for the OFFLINE version:\n" + str(round(aOffline[0],2)) + "% of agreement *" + str(int(aOffline[0]/100*lenOfFold)) + "/" + str(lenOfFold) + " comparisons* (sd = " + str(round(sdAOffline[0],2)) + "%),\ncomputation takes " + str(round(tOffline[0],4)) + " seconds (sd = " + str(round(sdTOffline[0],4)) + " seconds).\n"
	return s
