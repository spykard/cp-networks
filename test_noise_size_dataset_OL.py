from src.learnCPnet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
nameOfFile = "databases/sushi_30Users_10000Comparisons.data"
numberOfComparisons = [50000,150000,1500000] # -1 = all of the comparisons in file
percentageOfNoise = [0,10] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 10 # = percentage taken in the dataset for the cross validation

decisionThresholdBis = 0.1 # delta for decisionMode = 1
epsilonThreshold = 0.05 # threshold for epsilon

convergence = False

online = True
offline = False
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 2



for numberOfComparisons in [50000,150000,1500000]:
	fileTestOL = {}
	for i in percentageOfNoise:
		fileTestOL[i] = open("test-results/test_time_size_database_" + str(i) + "_noise_" + str(numberOfComparisons) + "_Online.dat","w")
	for numberOfParentsForLearnedCPNet in [0,1,2,4,6,8,11]:
		averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,online,offline,decisionMode,None,autorizedCycle)
		for i in percentageOfNoise:
			fileTestOL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[i]) + " " + str(sdAOnline[i]) + " " + str(aOnlineLog[i]) + " " + str(sdAOnlineLog[i]) + str(meanAccNoiseOnline[i]) + " " + str(sdANoiseOnline[i]) + " " + str(meanAccNoiseOnlineLog[i]) + " " + str(sdANoiseOnlineLog[i]) + "\n")
	for i in percentageOfNoise:
		fileTestOL[i].close()
