from src.learnCPnet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "databases/sushi_30Users_10000Comparisons.data"
numberOfComparisons = [10000,100000,250000,500000] # -1 = all of the comparisons in file
percentageOfNoise = [0,10] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 3
numberOfRoundsForLearningProcedure = 10 # = percentage taken in the dataset for the bagging

decisionThresholdBis = 0.1 # delta for decisionMode = 1
epsilonThreshold = 0.05 # threshold for epsilon

convergence = False

online = True
offline = True
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 1


for numberOfComparisons in [10000,100000,500000]:
	fileTestHL = {}
	fileTestOL = {}
	for i in percentageOfNoise:
		fileTestHL[i] = open("test-results/test_time_size_database_" + str(i) + "_noise_" + str(numberOfComparisons) + "_Offline.dat","w")
		fileTestOL[i] = open("test-results/test_time_size_database_" + str(i) + "_noise_" + str(numberOfComparisons) + "_Online.dat","w")
	for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6,7,8,9,10,11]:
		averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,online,offline,decisionMode,None,autorizedCycle)
		for i in percentageOfNoise:
			fileTestHL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(aOffline[i]) + " " + str(sdAOffline[i]) + str(aOfflineLog[i]) + " " + str(sdAOfflineLog[i]) + "\n")
			fileTestOL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[i]) + " " + str(sdAOnline[i]) + str(aOnlineLog[i]) + " " + str(sdAOnlineLog[i]) + "\n")
	for i in percentageOfNoise:
		fileTestHL[i].close()
		fileTestOL[i].close()
