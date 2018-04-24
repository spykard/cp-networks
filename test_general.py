from sys import *
from src.learnCPnet import *

# arguments for python3 command line: numberOfRounds online[True or False] offline[True or False] decisionMode[1 or 2] decisionThresholdBis epsilonThreshold numberOfComparisons
print(argv[1],argv[2],argv[3],argv[4],argv[5],argv[6],argv[7])

modeForDatasetGeneration = 1 # 1 = read a file, 2 = generate a synthetic database
nameOfFile = "databases/movieLensDataset_user4222.dat"
numberOfComparisons = int(argv[7]) # -1 = all of the comparisons in file
percentageOfNoise = [0] # between 0 and 50
numberOfVariables = -1 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = 4 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = int(argv[1]) # = percentage taken in the dataset for the cross validation

decisionThresholdBis = float(argv[5]) # delta for decisionMode = 1
epsilonThreshold = float(argv[6]) # threshold for epsilon

convergence = False

# True or False
if argv[2] == "True":
	online = True
else:
	online = False
if argv[3] == "True":
	offline = True
else:
	offline = False

autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = int(argv[4])



averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,online,offline,decisionMode,None,autorizedCycle)
print(displayParameters(modeForDatasetGeneration,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,lenOfFold,numberOfAttributes,online) + "\n" + displayResults(modeForDatasetGeneration,averageCycleSize2,percentageOfNoise,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,lenOfFold,online,offline,""))
