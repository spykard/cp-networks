from src.learnCpNet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "databases/sushi_30Users_10000Comparisons.data"
numberOfComparisons = 500000 # -1 = all of the comparisons in file
percentageOfNoise = [0] # between 0 and 50
numberOfVariables = [4,8,12] # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = [1,3,-1] # -1 = infinity
numberOfParentsForTargetCPNet = 5 # -1 = infinity
numberOfParentsForLearnedCPNet = 5 # -1 = infinity
numberOfRoundsForFileGeneration = 3
numberOfRoundsForLearningProcedure = 10 # = percentage taken in the dataset for the bagging

decisionThresholdBis = 0.1 # delta for decisionMode = 1

convergence = False

if numberOfRoundsForLearningProcedure != 1:
	convergence = False

online = True
offline = True
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 1



fileTestHL = open("test-results/test_comp_soa_Offline.dat","w")
fileTestOL = open("test-results/test_comp_soa_Online.dat","w")
for numberOfEdgesLambda in [1,3,-1]:
	for numberOfVariables in [4,8,12]:
		averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle)
		fileTestHL.write("lambda " + str(numberOfEdgesLambda) + " var " + str(numberOfVariables) + " acc " + str(aOffline[0]) + "\n")
		fileTestOL.write("lambda " + str(numberOfEdgesLambda) + " var " + str(numberOfVariables) + " acc " + str(aOnline[0]) + "\n")
fileTestHL.close()
fileTestOL.close()
