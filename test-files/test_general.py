from ../learnCpNet import *
from sys import *

# arguments for python3 command line: numberOfRounds online[True or False] offline[True or False] decisionMode[1 or 2 or 3] decisionThresholdBis
print(argv[1],argv[2],argv[3],argv[4],argv[5])

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "test_database.dat"
numberOfComparisons = 1000000 # -1 = all of the comparisons in file
percentageOfNoise = [0,10,20,40] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = int(argv[1]) # = percentage taken in the dataset for the bagging

decisionThresholdBis = float(argv[5]) # delta for decisionMode = 1
convergence = False

foldValidation = False

if convergence and foldValidation:
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

averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle,foldValidation)
print(displayParameters(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,lenOfData,numberOfAttributes,online) + "\n" + displayResults(modeForDatasetGeneration,averageCycleSize2,percentageOfNoise,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOffline,lenOfData,lenOfFold,online,offline,"",foldValidation))
