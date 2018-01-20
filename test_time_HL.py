from apprCpNet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "sushi_30Users_10000Comparisons.data"
numberOfComparisons = [10000,50000,100000] # -1 = all of the comparisons in file
percentageOfNoise = [0] # between 0 and 50
numberOfVariables = 15 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 30 # = percentage taken in the dataset for the bagging

# confidenceThreshold = 200 # between 0 and 1, percentage of the database taken to be confident (minimum) for decisionMode = 2
# decisionThreshold = 0.20 # between 0 and 1, percentage of the sum of the two counters for the current rule (maximum) for decisionMode = 2

confidenceThreshold = 5 # between 0 and 1, percentage of the database taken to be confident (minimum) for decisionMode = 3
decisionThreshold = 0.001 # between 0 and 1, percentage of the sum of the two counters for the current rule (maximum) for decisionMode = 3

decisionThresholdBis = 0.95 # delta for decisionMode = 1
convergence = False

online = False
offline = True
autorizedCycle = False

decisionMode = 1 # 1 = Hoeffding, 2 = variable entropy, 3 = rule entropy


for numberOfComparisons in [10000,50000,100000]:
	dataset = Database(step = 1,smooth = 1,mode = modeForDatasetGeneration, filename = nameOfFile, nC = numberOfComparisons, noise = percentageOfNoise, nbV = numberOfVariables,lb = numberOfEdgesLambda,nbP = numberOfParentsForTargetCPNet)

	fileTest = open("Tests/test_time_" + str(numberOfComparisons) + "_Offline.dat","w")
	for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
		averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,confidenceThreshold,decisionThreshold,decisionThresholdBis,convergence,online,offline,decisionMode,dataset,autorizedCycle)
		fileTest.write(str(numberOfParentsForLearnedCPNet) + " " + str(tOffline[0]) + " " + str(sdTOffline[0]) + " \n")
	fileTest.close()
