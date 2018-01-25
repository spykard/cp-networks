from apprCpNet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "sushi_30Users_10000Comparisons.data"
numberOfComparisons = 20000 # -1 = all of the comparisons in file
percentageOfNoise = [0] # between 0 and 50
numberOfVariables = [4,8,12] # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = [1,3,-1] # -1 = infinity
numberOfParentsForTargetCPNet = 5 # -1 = infinity
numberOfParentsForLearnedCPNet = 5 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 30 # = percentage taken in the dataset for the bagging

decisionThresholdBis = 0.9 # delta for decisionMode = 1
convergence = False

foldValidation = True

if convergence and foldValidation:
	convergence = False

online = False
offline = True
autorizedCycle = False

# 1 = Hoeffding for conditioned variable, 2 = Hoeffding for conditioned AND conditional variables
decisionMode = 1



fileTest = open("Tests/test_comp_soa_Offline.dat","w")
for numberOfEdgesLambda in [1,3,-1]:
	for numberOfVariables in [4,8,12]:
		averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle,foldValidation)
		fileTest.write("lambda " + str(numberOfEdgesLambda) + " var " + str(numberOfVariables) + " acc " + str(aOffline[0]) + "\n")
fileTest.close()
