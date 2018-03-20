from src.learnCPnet import *
from math import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
nameOfFile = "databases/sushi_30Users_10000Comparisons.data"
numberOfComparisons = 500000 # -1 = all of the comparisons in file
percentageOfNoise = [0,20] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 10 # = percentage taken in the dataset for the cross validation

decisionThresholdBis = 0.1 # delta for decisionMode = 1
epsilonThreshold = 0.05 # threshold for epsilon

convergence = True

online = True
offline = True
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 2



averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,200000,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,False,True,decisionMode,None,autorizedCycle)
for key,value in meanConvergenceAccuracyOffline.items():
	convfileHL = open("test-results/test_conv_" + str(key) + "_Offline.dat","w")
	convfileHL.write("0 100 0 " + str(-(1/4)*log(1/2)-(1/4)*log(1/2)) + " 0\n")
	for i,v in enumerate(value):
		convfileHL.write(str(i+1) + " " + str(100-v) + " " + str(sdConvergenceAccuracyOffline[key][i]) + " " + str(meanConvergenceAccuracyOfflineLog[key][i]) + " " + str(sdConvergenceAccuracyOfflineLog[key][i]) + "\n")
	convfileHL.write("\n")
	convfileHL.close()

averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,1500000,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,True,False,decisionMode,None,autorizedCycle)
for key,value in meanConvergenceAccuracyOnline.items():
	convfileOL = open("test-results/test_conv_" + str(key) + "_Online.dat","w")
	convfileOL.write("0 100 0 " + str(-(1/4)*log(1/2)-(1/4)*log(1/2)) + " 0\n")
	for i,v in enumerate(value):
			convfileOL.write(str(i+1) + " " + str(100-v) + " " + str(sdConvergenceAccuracyOnline[key][i]) + " " + str(meanConvergenceAccuracyOnlineLog[key][i]) + " " + str(sdConvergenceAccuracyOnlineLog[key][i]) + "\n")
	convfileOL.write("\n")
	convfileOL.close()
