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


for numberOfComparisons in [10000,50000,100000]:
	dataset = Database(foldValidation,step = 1,smooth = 1,mode = modeForDatasetGeneration, filename = nameOfFile, nC = numberOfComparisons, noise = percentageOfNoise, nbV = numberOfVariables,lb = numberOfEdgesLambda,nbP = numberOfParentsForTargetCPNet,k = numberOfRoundsForLearningProcedure)

	fileTestHL = open("Tests/test_time_" + str(numberOfComparisons) + "_Offline.dat","w")
	fileTestOL = open("Tests/test_time_" + str(numberOfComparisons) + "_Online.dat","w")
	for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
		averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,dataset,autorizedCycle,foldValidation)
		fileTestHL.write(str(numberOfParentsForLearnedCPNet) + " " + str(tOffline[0]) + " " + str(sdTOffline[0]) + " \n")
		fileTestOL.write(str(numberOfParentsForLearnedCPNet) + " " + str(tOnline[0]) + " " + str(sdTOnline[0]) + " \n")
	fileTestHL.close()
	fileTestOL.close()
