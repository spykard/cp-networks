from src.learnCPnet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
nameOfFile = "databases/sushi_30Users_10000Comparisons.data"
numberOfComparisons = 200000 # -1 = all of the comparisons in file
percentageOfNoise = [0,10,20,40] # between 0 and 50
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

online = False
offline = True
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 2



dataset = []
for i in range(numberOfRounds):
	dataset.append(Database(step = 1,smooth = 1,mode = modeForDatasetGeneration, filename = nameOfFile, nC = numberOfComparisons, noise = percentageOfNoise, nbV = numberOfVariables,lb = numberOfEdgesLambda,nbP = numberOfParentsForTargetCPNet,k = numberOfRoundsForLearningProcedure))

fileTestNoiseHL = {}
for i in percentageOfNoise:
	fileTestNoiseHL[i] = open("test-results/test_acc_noise" + str(i) + "_Offline.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2,6,8,11]:
	accOffline = {}
	accOfflineLog = {}
	sdOffline = {}
	sdOfflineLog = {}
	for n in percentageOfNoise:
		accOffline[n] = 0
		accOfflineLog[n] = 0
		sdOffline[n] = 0
		sdOfflineLog[n] = 0
	for i in range(numberOfRounds):
		averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,percentageOfNoise,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,online,offline,decisionMode,dataset[i],autorizedCycle)
		for n in percentageOfNoise:
			accOffline[n] += aOffline[n]
			accOfflineLog[n] += aOfflineLog[n]
			sdOffline[n] += sdAOffline[n]
			sdOfflineLog[n] += sdAOfflineLog[n]
	for i in percentageOfNoise:
		fileTestNoiseHL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(accOffline[i]/numberOfRounds) + " " + str(sdOffline[i]/numberOfRounds) + " " + str(accOfflineLog[i]/numberOfRounds) + " " + str(sdOfflineLog[i]/numberOfRounds) + "\n")
for i in percentageOfNoise:
	fileTestNoiseHL[i].close()
