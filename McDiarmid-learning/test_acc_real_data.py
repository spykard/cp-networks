from src.learnCpNet import *

modeForDatasetGeneration = 1 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = ["databases/sushi_30Users_10000Comparisons.dat","databases/sushi_30Users_20000Comparisons.dat","databases/hotels_parsing_binarisation_10000.dat","databases/hotels_parsing_binarisation_20000.dat"]
# nameOfFile = ["databases/hotels_parsing_binarisation_10000.dat","databases/hotels_parsing_binarisation_20000.dat"]
numberOfComparisons = -1 # -1 = all of the comparisons in file
percentageOfNoise = [0] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
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



fileTestHL = open("test-results/test_acc_sushi_10000_Offline.dat","w")
fileTestOL = open("test-results/test_acc_sushi_10000_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2]:
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,nameOfFile[0],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle)
	fileTestHL.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOffline[0]) + " " + str(sdAOffline[0]) + "\n")
	fileTestOL.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[0]) + " " + str(sdAOnline[0]) + "\n")
fileTestHL.close()
fileTestOL.close()

fileTestHL = open("test-results/test_acc_sushi_20000_Offline.dat","w")
fileTestOL = open("test-results/test_acc_sushi_20000_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2]:
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,nameOfFile[1],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle)
	fileTestHL.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOffline[0]) + " " + str(sdAOffline[0]) + "\n")
	fileTestOL.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[0]) + " " + str(sdAOnline[0]) + "\n")
fileTestHL.close()
fileTestOL.close()

fileTestHL = open("test-results/test_acc_hotels_10000_Offline.dat","w")
fileTestOL = open("test-results/test_acc_hotels_10000_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6]:
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,nameOfFile[2],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle)
	fileTestHL.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOffline[0]) + " " + str(sdAOffline[0]) + "\n")
	fileTestOL.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[0]) + " " + str(sdAOnline[0]) + "\n")
fileTestHL.close()
fileTestOL.close()

fileTestHL = open("test-results/test_acc_hotels_20000_Offline.dat","w")
fileTestOL = open("test-results/test_acc_hotels_20000_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6]:
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,nameOfFile[3],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle)
	fileTestHL.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOffline[0]) + " " + str(sdAOffline[0]) + "\n")
	fileTestOL.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[0]) + " " + str(sdAOnline[0]) + "\n")
fileTestHL.close()
fileTestOL.close()
