from apprCpNet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "sushi_30Users_10000Comparisons.data"
numberOfComparisons = 20000 # -1 = all of the comparisons in file
percentageOfNoise = [0,10,20,30,40,50,60,70,80,90,100] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 10 # = percentage taken in the dataset for the bagging

numberOfRounds = 3

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

dataset = []
for i in range(numberOfRounds):
	dataset.append(Database(foldValidation,step = 1,smooth = 1,mode = modeForDatasetGeneration, filename = nameOfFile, nC = numberOfComparisons, noise = percentageOfNoise, nbV = numberOfVariables,lb = numberOfEdgesLambda,nbP = numberOfParentsForTargetCPNet,k = numberOfRoundsForLearningProcedure))


# Test noise accuracy
fileTestNoiseHL = {}
fileTestNoiseOL = {}
for i in [0,10,20,40]:
	fileTestNoiseHL[i] = open("Tests/test_acc_noise" + str(i) + "_Offline.dat","w")
	fileTestNoiseOL[i] = open("Tests/test_acc_noise" + str(i) + "_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6,7,8,9,10,11]:
	accOnline = {}
	sdOnline = {}
	accOffline = {}
	sdOffline = {}
	for n in [0,10,20,40]:
		accOnline[n] = 0
		sdOnline[n] = 0
		accOffline[n] = 0
		sdOffline[n] = 0
	for i in range(numberOfRounds):
		averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,[0,10,20,40],numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,dataset[i],autorizedCycle,foldValidation)
		for n in [0,10,20,40]:
			accOnline[n] += aOnline[n]
			sdOnline[n] += sdAOnline[n]
			accOffline[n] += aOffline[n]
			sdOffline[n] += sdAOffline[n]
	
	for i in [0,10,20,40]:
		fileTestNoiseHL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(accOffline[i]/numberOfRounds) + " " + str(sdOffline[i]/numberOfRounds) + "\n")
		fileTestNoiseOL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(accOnline[i]/numberOfRounds) + " " + str(sdOnline[i]/numberOfRounds) + "\n")

for i in [0,10,20,40]:
	fileTestNoiseHL[i].close()
	fileTestNoiseOL[i].close()

# test hyperparameter
offline = False
fileTest = {}
for i in [0,10,20,40]:
	fileTest[i] = open("Tests/test_hyperparameter_" + str(i) + ".dat","w")
for decisionThresholdBis in [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]:
	accOnline = {}
	sdOnline = {}
	for n in [0,10,20,40]:
		accOnline[n] = 0
		sdOnline[n] = 0
	for i in range(numberOfRounds):
		averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,[0,10,20,40],numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,dataset[i],autorizedCycle,foldValidation)
		for n in [0,10,20,40]:
			accOnline[n] += aOnline[n]
			sdOnline[n] += sdAOnline[n]
	for i in [0,10,20,40]:
		fileTest[i].write(str(decisionThresholdBis) + " " + str(accOnline[i]/numberOfRounds) + " " + str(sdOnline[i]/numberOfRounds) + "\n")
for i in [0,10,20,40]:
	fileTest[i].close()
offline = True

# test noise resist
for n in percentageOfNoise:
		accOnline[n] = 0
		sdOnline[n] = 0
		accOffline[n] = 0
		sdOffline[n] = 0
for i in range(numberOfRounds):
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,dataset[i],autorizedCycle,foldValidation)
	for n in percentageOfNoise:
		accOnline[n] += meanAccNoiseOnline[n]
		sdOnline[n] += sdANoiseOnline[n]
		accOffline[n] += meanAccNoiseOffline[n]
		sdOffline[n] += sdANoiseOffline[n]
convfileTestOffline = open("Tests/test_noise_resist_Offline.dat","w")
tab1 = []
tab2 = []
for key in meanAccNoiseOffline.keys():
	tab1.append([key,accOffline[key]/numberOfRounds])
	tab2.append([key,sdOffline[key]/numberOfRounds])
tab1.sort()
tab2.sort()
convfileTestOffline.write("0 0.0 0.0\n")
for i in range(1,len(tab1)):
	convfileTestOffline.write(str(tab1[i][0]) + " " + str(abs(tab1[0][1] - tab1[i][1])) + " " + str((tab2[0][1] + tab2[i][1])/2) + "\n")
convfileTestOffline.close()
convfileTestOnline = open("Tests/test_noise_resist_Online.dat","w")
tab1 = []
tab2 = []
for key in meanAccNoiseOnline.keys():
	tab1.append([key,accOnline[key]/numberOfRounds])
	tab2.append([key,sdOnline[key]/numberOfRounds])
tab1.sort()
tab2.sort()
convfileTestOnline.write("0 0.0 0.0\n")
for i in range(1,len(tab1)):
	convfileTestOnline.write(str(tab1[i][0]) + " " + str(abs(tab1[0][1] - tab1[i][1])) + " " + str((tab2[0][1] + tab2[i][1])/2) + "\n")
convfileTestOnline.close()
