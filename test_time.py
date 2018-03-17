from src.learnCPnet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "databases/sushi_30Users_10000Comparisons.data"
numberOfComparisons = [10000,50000,100000,500000] # -1 = all of the comparisons in file
percentageOfNoise = [0] # between 0 and 50
numberOfVariables = 15 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 10
numberOfRoundsForLearningProcedure = 1 # = percentage taken in the dataset for the bagging

decisionThresholdBis = 0.1 # delta for decisionMode = 1
epsilonThreshold = 0.05 # threshold for epsilon

convergence = False

online = True
offline = True
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 1


for numberOfComparisons in [10000,50000,100000,500000]:
	fileTestHL = open("test-results/test_time_" + str(numberOfComparisons) + "_Offline.dat","w")
	fileTestOL = open("test-results/test_time_" + str(numberOfComparisons) + "_Online.dat","w")
	for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
		averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,online,offline,decisionMode,None,autorizedCycle)
		fileTestHL.write(str(numberOfParentsForLearnedCPNet) + " " + str(tOffline[0]) + " " + str(sdTOffline[0]) + " \n")
		fileTestOL.write(str(numberOfParentsForLearnedCPNet) + " " + str(tOnline[0]) + " " + str(sdTOnline[0]) + " \n")
	fileTestHL.close()
	fileTestOL.close()
