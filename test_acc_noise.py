from apprCpNet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "sushi_30Users_10000Comparisons.data"
numberOfComparisons = 20000 # -1 = all of the comparisons in file
percentageOfNoise = [0,10,20,40] # between 0 and 50
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
offline = True
autorizedCycle = False

# 1 = Hoeffding for conditioned variable, 2 = Hoeffding for conditioned AND conditional variables
decisionMode = 1



dataset = Database(foldValidation,step = 1,smooth = 1,mode = modeForDatasetGeneration, filename = nameOfFile, nC = numberOfComparisons, noise = percentageOfNoise, nbV = numberOfVariables,lb = numberOfEdgesLambda,nbP = numberOfParentsForTargetCPNet,k = numberOfRoundsForLearningProcedure)

fileTestNoiseHL = {}
fileTestNoiseOL = {}

for i in percentageOfNoise:
	fileTestNoiseHL[i] = open("Tests/test_acc_noise" + str(i) + "_Offline.dat","w")
	fileTestNoiseOL[i] = open("Tests/test_acc_noise" + str(i) + "_Online.dat","w")
for numberOfParentsForLearnedCPNet in [0,1,2,3,4,5,6,7,8,9,10,11]:
	averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,dataset,autorizedCycle,foldValidation)
	for i in percentageOfNoise:
		fileTestNoiseHL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(aOffline[i]) + " " + str(sdAOffline[i]) + "\n")
		fileTestNoiseOL[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(aOnline[i]) + " " + str(sdAOnline[i]) + "\n")
#numberOfParentsForLearnedCPNet = -1
#autorizedCycle = True
#averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,confidenceThreshold,decisionThreshold,decisionThresholdBis,convergence,online,offline,decisionMode,dataset,autorizedCycle)
#for i in percentageOfNoise:
#	fileTestNoise[i].write(str(numberOfParentsForLearnedCPNet) + " " + str(aOffline[i]) + " " + str(sdAOffline[i]) + "\n")
for i in percentageOfNoise:
	fileTestNoiseHL[i].close()
	fileTestNoiseOL[i].close()

print(displayParameters(modeForDatasetGeneration,bagging,nameOfFile[0],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,lenOfData,numberOfAttributes,online) + "\n" + displayResults(modeForDatasetGeneration,averageCycleSize2,percentageOfNoise,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOffline,lenOfData,lenOfFold,online,offline,"",foldValidation))
