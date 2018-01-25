from apprCpNet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "sushi_30Users_10000Comparisons.data"
numberOfComparisons = [100,1000,5000,10000] # -1 = all of the comparisons in file
percentageOfNoise = [0,10] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 3
numberOfRoundsForLearningProcedure = 10 # = percentage taken in the dataset for the bagging

decisionThresholdBis = 0.9 # delta for decisionMode = 1
convergence = False

foldValidation = True

if convergence and foldValidation:
	convergence = False

online = True
offline = True
autorizedCycle = False

# 1 = Hoeffding for conditioned variable, 2 = Hoeffding for conditioned AND conditional variables
decisionMode = 1


for numberOfComparisons in [5000,10000,20000]:
	fileTestHL = {}
	fileTestOL = {}
	for i in percentageOfNoise:
		fileTestHL[i] = open("Tests/test_time_size_database_" + str(i) + "_noise_" + str(numberOfComparisons) + "_Offline.dat","w")
		fileTestOL[i] = open("Tests/test_time_size_database_" + str(i) + "_noise_" + str(numberOfComparisons) + "_Online.dat","w")
	for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6,7,8,9,10,11]:
		averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle,foldValidation)
		for i in percentageOfNoise:
			fileTestHL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(aOffline[i]) + " " + str(sdAOffline[i]) + "\n")
			fileTestOL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[i]) + " " + str(sdAOnline[i]) + "\n")
	for i in percentageOfNoise:
		fileTestHL[i].close()
		fileTestOL[i].close()
