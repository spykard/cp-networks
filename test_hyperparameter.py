from src.learnCPnet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
nameOfFile = "databases/sushi_30Users_10000Comparisons.data"
numberOfComparisons = 1500000 # -1 = all of the comparisons in file
percentageOfNoise = [0,10,20] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 10 # = percentage taken in the dataset for the cross validation

numberOfRounds = 1

decisionThresholdBis = 0.1 # delta for decisionMode = 1
epsilonThreshold = 0.05 # threshold for epsilon

convergence = False

online = True
offline = False
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 2



dataset = []
for i in range(numberOfRounds):
	dataset.append(Database(step = 1,smooth = 1,mode = modeForDatasetGeneration, filename = nameOfFile, nC = numberOfComparisons, noise = percentageOfNoise, nbV = numberOfVariables,lb = numberOfEdgesLambda,nbP = numberOfParentsForTargetCPNet,k = numberOfRoundsForLearningProcedure))

fileTest = {}
for i in percentageOfNoise:
	fileTest[i] = open("test-results/test_hyperparameter_" + str(i) + ".dat","w")
for decisionThresholdBis in [0,0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2]:
	accOnline = {}
	accNoiseOnline = {}
	accOnlineLog = {}
	accNoiseOnlineLog = {}
	sdOnline = {}
	sdNoiseOnline = {}
	sdOnlineLog = {}
	sdNoiseOnlineLog = {}
	for n in percentageOfNoise:
		accOnline[n] = 0
		accNoiseOnline[n] = 0
		accOnlineLog[n] = 0
		accNoiseOnlineLog[n] = 0
		sdOnline[n] = 0
		sdNoiseOnline[n] = 0
		sdOnlineLog[n] = 0
		sdNoiseOnlineLog[n] = 0
	for i in range(numberOfRounds):
		averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,online,offline,decisionMode,dataset[i],autorizedCycle)
		for n in percentageOfNoise:
			accOnline[n] += aOnline[n]
			accNoiseOnline[n] += meanAccNoiseOnline[n]
			accOnlineLog[n] += aOnlineLog[n]
			accNoiseOnlineLog[n] += meanAccNoiseOnlineLog[n]
			sdOnline[n] += sdAOnline[n]
			sdNoiseOnline[n] += sdANoiseOnline[n]
			sdOnlineLog[n] += sdAOnlineLog[n]
			sdNoiseOnlineLog[n] += sdANoiseOnlineLog[n]
	for i in percentageOfNoise:
		fileTest[i].write(str(decisionThresholdBis) + " " + str(accOnline[i]/numberOfRounds) + " " + str(sdOnline[i]/numberOfRounds) + " " + str(accOnlineLog[i]/numberOfRounds) + " " + str(sdOnlineLog[i]/numberOfRounds) + " " + str(accNoiseOnline[i]/numberOfRounds) + " " + str(sdNoiseOnline[i]/numberOfRounds) + " " + str(accNoiseOnlineLog[i]/numberOfRounds) + " " + str(sdNoiseOnlineLog[i]/numberOfRounds) + "\n")
for i in percentageOfNoise:
	fileTest[i].close()
