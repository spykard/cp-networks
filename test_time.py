from src.learnCPnet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "databases/sushi_30Users_10000Comparisons.data"
numberOfComparisons = [5000,10000,50000,200000] # -1 = all of the comparisons in file
percentageOfNoise = [0] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 10 # = percentage taken in the dataset for the cross validation

decisionThresholdBis = 1 # delta for decisionMode = 1
epsilonThreshold = 0.5 # threshold for epsilon

convergence = False

online = True
offline = True
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 2


for numberOfComparisons in [5000,10000,50000,200000]:
	fileTestHL = open("test-results/test_time_" + str(numberOfComparisons) + "_Offline.dat","w")
	fileTestOL = open("test-results/test_time_" + str(numberOfComparisons) + "_Online.dat","w")
	for numberOfParentsForLearnedCPNet in [0,1,2,6,8,11]:
		averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,online,offline,decisionMode,None,autorizedCycle)
		fileTestHL.write(str(numberOfParentsForLearnedCPNet) + " " + str(tOffline[0]) + " " + str(sdTOffline[0]) + " \n")
		fileTestOL.write(str(numberOfParentsForLearnedCPNet) + " " + str(tOnline[0]) + " " + str(sdTOnline[0]) + " \n")
	fileTestHL.close()
	fileTestOL.close()
