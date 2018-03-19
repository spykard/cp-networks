from src.learnCPnet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "databases/sushi_30Users_10000Comparisons.data"
numberOfComparisons = 1500000 # -1 = all of the comparisons in file
percentageOfNoise = [0,10,20,30,40,50,60,70,80,90,100] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 10 # = percentage taken in the dataset for the cross validation

numberOfRounds = 3

decisionThresholdBis = 0.1 # delta for decisionMode = 1
epsilonThreshold = 0.05 # threshold for epsilon

convergence = False

online = True
offline = True
autorizedCycle = False

# 1 = McDiarmid for conditioned variable, 2 = McDiarmid for conditioned AND conditional variables
decisionMode = 2

dataset = []
for i in range(numberOfRounds):
	dataset.append(Database(step = 1,smooth = 1,mode = modeForDatasetGeneration, filename = nameOfFile, nC = numberOfComparisons, noise = percentageOfNoise, nbV = numberOfVariables,lb = numberOfEdgesLambda,nbP = numberOfParentsForTargetCPNet,k = numberOfRoundsForLearningProcedure))


# Test noise accuracy
fileTestNoiseHL = {}
for i in [0,10,20,40]:
	fileTestNoiseHL[i] = open("test-results/test_acc_noise" + str(i) + "_Offline.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2,6,8,11]:
	accOffline = {}
	accOfflineLog = {}
	sdOffline = {}
	sdOfflineLog = {}
	for n in [0,10,20,40]:
		accOffline[n] = 0
		accOfflineLog[n] = 0
		sdOffline[n] = 0
		sdOfflineLog[n] = 0
	for i in range(numberOfRounds):
		averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,200000,[0,10,20,40],numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,False,True,decisionMode,dataset[i],autorizedCycle)
		for n in [0,10,20,40]:
			accOffline[n] += aOffline[n]
			accOfflineLog[n] += aOfflineLog[n]
			sdOffline[n] += sdAOffline[n]
			sdOfflineLog[n] += sdAOfflineLog[n]
	for i in [0,10,20,40]:
		fileTestNoiseHL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(accOffline[i]/numberOfRounds) + " " + str(sdOffline[i]/numberOfRounds) + " " + str(accOfflineLog[i]/numberOfRounds) + " " + str(sdOfflineLog[i]/numberOfRounds) + "\n")
for i in [0,10,20,40]:
	fileTestNoiseHL[i].close()
	
fileTestNoiseOL = {}
for i in [0,10,20,40]:
	fileTestNoiseOL[i] = open("test-results/test_acc_noise" + str(i) + "_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2,6,8,11]:
	accOnline = {}
	accOnlineLog = {}
	sdOnline = {}
	sdOnlineLog = {}
	for n in [0,10,20,40]:
		accOnline[n] = 0
		accOnlineLog[n] = 0
		sdOnline[n] = 0
		sdOnlineLog[n] = 0
	for i in range(numberOfRounds):
		averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,1500000,[0,10,20,40],numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,True,False,decisionMode,dataset[i],autorizedCycle)
		for n in [0,10,20,40]:
			accOnline[n] += aOnline[n]
			accOnlineLog[n] += aOnlineLog[n]
			sdOnline[n] += sdAOnline[n]
			sdOnlineLog[n] += sdAOnlineLog[n]
	for i in [0,10,20,40]:
		fileTestNoiseOL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(accOnline[i]/numberOfRounds) + " " + str(sdOnline[i]/numberOfRounds) + " " + str(accOnlineLog[i]/numberOfRounds) + " " + str(sdOnlineLog[i]/numberOfRounds) + "\n")
for i in [0,10,20,40]:
	fileTestNoiseOL[i].close()

# test hyperparameter
fileTest = {}
for i in [0,10,20,40]:
	fileTest[i] = open("test-results/test_hyperparameter_" + str(i) + ".dat","w")
for decisionThresholdBis in [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2]:
	accOnline = {}
	accOnlineLog = {}
	sdOnline = {}
	sdOnlineLog = {}
	for n in [0,10,20,40]:
		accOnline[n] = 0
		accOnlineLog[n] = 0
		sdOnline[n] = 0
		sdOnlineLog[n] = 0
	for i in range(numberOfRounds):
		averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,1500000,[0,10,20,40],numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,True,False,decisionMode,dataset[i],autorizedCycle)
		for n in [0,10,20,40]:
			accOnline[n] += aOnline[n]
			accOnlineLog[n] += aOnlineLog[n]
			sdOnline[n] += sdAOnline[n]
			sdOnlineLog[n] += sdAOnlineLog[n]
	for i in [0,10,20,40]:
		fileTest[i].write(str(decisionThresholdBis) + " " + str(accOnline[i]/numberOfRounds) + " " + str(sdOnline[i]/numberOfRounds) + " " + str(accOnlineLog[i]/numberOfRounds) + " " + str(sdOnlineLog[i]/numberOfRounds) + "\n")
for i in [0,10,20,40]:
	fileTest[i].close()

# test noise resist
for n in percentageOfNoise:
	accOffline[n] = 0
	accOfflineLog[n] = 0
	sdOffline[n] = 0
	sdOfflineLog[n] = 0
for i in range(numberOfRounds):
	averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,200000,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,False,True,decisionMode,dataset[i],autorizedCycle)
	for n in percentageOfNoise:
		accOffline[n] += aOffline[n]
		accOfflineLog[n] += aOfflineLog[n]
		sdOffline[n] += sdAOffline[n]
		sdOfflineLog[n] += sdAOfflineLog[n]
convfileTestOffline = open("test-results/test_noise_resist_Offline.dat","w")
tab1 = []
tab2 = []
tab3 = []
tab4 = []
for key in meanAccNoiseOffline.keys():
	tab1.append([key,accOffline[key]/numberOfRounds])
	tab2.append([key,sdOffline[key]/numberOfRounds])
	tab3.append([key,accOfflineLog[key]/numberOfRounds])
	tab4.append([key,sdOfflineLog[key]/numberOfRounds])
tab1.sort()
tab2.sort()
tab3.sort()
tab4.sort()
convfileTestOffline.write("0 0.0 0.0 0.0 0.0\n")
for i in range(1,len(tab1)):
	convfileTestOffline.write(str(tab1[i][0]) + " " + str(abs(tab1[0][1] - tab1[i][1])) + " " + str((tab2[0][1] + tab2[i][1])/2) + " " + str(abs(tab3[i][1])) + " " + str(tab4[i][1]) + "\n")
convfileTestOffline.close()

for n in percentageOfNoise:
	accOnline[n] = 0
	accOnlineLog[n] = 0
	sdOnline[n] = 0
	sdOnlineLog[n] = 0
for i in range(numberOfRounds):
	averageCycleSize2,aOnline,aOnlineLog,sdAOnline,sdAOnlineLog,aOffline,aOfflineLog,sdAOffline,sdAOfflineLog,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOnlineLog,sdANoiseOnline,sdANoiseOnlineLog,meanAccNoiseOffline,meanAccNoiseOfflineLog,sdANoiseOffline,sdANoiseOfflineLog,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,meanConvergenceAccuracyOnlineLog,sdConvergenceAccuracyOnline,sdConvergenceAccuracyOnlineLog,meanConvergenceAccuracyOffline,meanConvergenceAccuracyOfflineLog,sdConvergenceAccuracyOffline,sdConvergenceAccuracyOfflineLog = generalProcedure(modeForDatasetGeneration,nameOfFile,1500000,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,epsilonThreshold,convergence,True,False,decisionMode,dataset[i],autorizedCycle)
	for n in percentageOfNoise:
		accOnline[n] += aOnline[n]
		accOnlineLog[n] += aOnlineLog[n]
		sdOnline[n] += sdAOnline[n]
		sdOnlineLog[n] += sdAOnlineLog[n]
convfileTestOnline = open("test-results/test_noise_resist_Online.dat","w")
tab1 = []
tab2 = []
tab3 = []
tab4 = []
for key in meanAccNoiseOnline.keys():
	tab1.append([key,accOnline[key]/numberOfRounds])
	tab2.append([key,sdOnline[key]/numberOfRounds])
	tab3.append([key,accOnlineLog[key]/numberOfRounds])
	tab4.append([key,sdOnlineLog[key]/numberOfRounds])
tab1.sort()
tab2.sort()
tab3.sort()
tab4.sort()
convfileTestOnline.write("0 0.0 0.0 0.0 0.0\n")
for i in range(1,len(tab1)):
	convfileTestOnline.write(str(tab1[i][0]) + " " + str(abs(tab1[0][1] - tab1[i][1])) + " " + str((tab2[0][1] + tab2[i][1])/2) + " " + str(abs(tab3[i][1])) + " " + str(tab4[i][1]) + "\n")
convfileTestOnline.close()
