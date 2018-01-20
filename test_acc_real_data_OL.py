from apprCpNet import *

modeForDatasetGeneration = 1 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = ["sushi_30Users_10000Comparisons.dat","sushi_30Users_20000Comparisons.dat","hotels_parsing_binarisation_10000.dat","hotels_parsing_binarisation_20000.dat"]
# nameOfFile = ["hotels_parsing_binarisation_10000.dat","hotels_parsing_binarisation_20000.dat"]
numberOfComparisons = -1 # -1 = all of the comparisons in file
percentageOfNoise = [0] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
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
offline = False
autorizedCycle = False

# 1 = Hoeffding for conditioned variable, 2 = Hoeffding for conditioned AND conditional variables
decisionMode = 1



fileTest = open("Tests/test_acc_sushi_10000_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2]:
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile[0],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle,foldValidation)
	fileTest.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[0]) + " " + str(sdAOnline[0]) + "\n")
fileTest.close()

fileTest = open("Tests/test_acc_sushi_20000_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2]:
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile[1],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle,foldValidation)
	fileTest.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[0]) + " " + str(sdAOnline[0]) + "\n")
fileTest.close()

fileTest = open("Tests/test_acc_hotels_10000_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6]:
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile[2],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle,foldValidation)
	fileTest.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[0]) + " " + str(sdAOnline[0]) + "\n")
fileTest.close()

fileTest = open("Tests/test_acc_hotels_20000_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6]:
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile[3],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle,foldValidation)
	fileTest.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[0]) + " " + str(sdAOnline[0]) + "\n")
fileTest.close()
