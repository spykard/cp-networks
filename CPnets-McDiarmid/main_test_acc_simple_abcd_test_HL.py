from src.learnCPnet import *
import os.path

modeForDatasetGeneration = 1 # 1 = read a file, 2 = generate a synthetic database
nameOfFile = [None,None,None,None,os.path.abspath("CPnets-McDiarmid/databases/simple_abcd_test_michael_et_al.dat")]
# nameOfFile = ["databases/sushi_30Users_10000Comparisons.dat","databases/sushi_30Users_20000Comparisons.dat","databases/hotels_parsing_binarisation_10000.dat","databases/hotels_parsing_binarisation_20000.dat","databases/movieLensDataset_200000.dat"]
numberOfComparisons = -1 # -1 = all of the comparisons in file
percentageOfNoise = [0] # between 0 and 50
numberOfVariables = -1 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 0 # = percentage taken in the dataset for the cross validation

decisionThresholdBis = 0.1 # delta for decisionMode = 1
epsilonThreshold = 0.05 # threshold for epsilon

convergence = False

online = False
offline = True
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 2



fileTestHL = open(os.path.abspath("CPnets-McDiarmid/test-results/main_test_acc_simple_abcd_test.dat"),"w")
for numberOfParentsForLearnedCPNet in [3]:
	averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile[4],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,online,offline,decisionMode,None,autorizedCycle)
	fileTestHL.write(str(numberOfParentsForLearnedCPNet) + " " + str(aOffline[0]) + " " + str(sdAOffline[0]) + " " + str(aOfflineLog[0]) + " " + str(sdAOfflineLog[0]) + "\n")
fileTestHL.close()
