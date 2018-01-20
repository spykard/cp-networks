from apprCpNet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "sushi_30Users_10000Comparisons.data"
numberOfComparisons = 1000 # -1 = all of the comparisons in file
percentageOfNoise = [0,20] # between 0 and 50
numberOfVariables = 8 # -1 = automatically choose from the number of comparisons
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
convergence = True

online = True
offline = False
autorizedCycle = False

decisionMode = 1 # 1 = Hoeffding, 2 = variable entropy, 3 = rule entropy



averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,confidenceThreshold,decisionThreshold,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle)

for key,value in meanConvergenceAccuracyOnline.items():
	convfile = open("Tests/test_conv_" + str(key) + "_Online.dat","w")
	convfile.write("0 100 0\n")
	for i,v in enumerate(value):
		convfile.write(str(i+1) + " " + str(100-v) + " " + str(sdConvergenceAccuracyOnline[key][i]) + "\n")
	convfile.write("\n")
	convfile.close()

print(displayParameters(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,confidenceThreshold,decisionThreshold,decisionThresholdBis,lenOfData,numberOfAttributes,online) + "\n" + displayResults(modeForDatasetGeneration,averageCycleSize2,percentageOfNoise,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOffline,lenOfData,online,offline,""))
