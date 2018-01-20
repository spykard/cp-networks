from apprCpNet import *

modeForDatasetGeneration = 2 # 1 = read a file, 2 = generate a synthetic database
bagging = False
nameOfFile = "sushi_30Users_10000Comparisons.data"
numberOfComparisons = 10000 # -1 = all of the comparisons in file
percentageOfNoise = [0,10,20,30,40,50,60,70,80,90,100] # between 0 and 50
numberOfVariables = 12 # -1 = automatically choose from the number of comparisons
numberOfEdgesLambda = -1 # -1 = infinity
numberOfParentsForTargetCPNet = -1 # -1 = infinity
numberOfParentsForLearnedCPNet = -1 # -1 = infinity
numberOfRoundsForFileGeneration = 1
numberOfRoundsForLearningProcedure = 30 # = percentage taken in the dataset for the bagging


decisionThresholdBis = 0.6 # delta for decisionMode = 1
convergence = False

foldValidation = True

if convergence and foldValidation:
	convergence = False

online = True
offline = False
autorizedCycle = False

# 1 = Hoeffding for conditioned variable, 2 = Hoeffding for conditioned AND conditional variables
decisionMode = 1



averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle,foldValidation)
	
convfileTestOnline = open("Tests/test_noise_resist_95_Online.dat","w")
tab1 = []
tab2 = []
for key in meanAccNoiseOnline.keys():
	tab1.append([key,meanAccNoiseOnline[key]])
	tab2.append([key,sdANoiseOnline[key]])
tab1.sort()
tab2.sort()
convfileTestOnline.write("0 0.0 0.0\n")
for i in range(1,len(tab1)):
	convfileTestOnline.write(str(tab1[i][0]) + " " + str(abs(tab1[0][1] - tab1[i][1])) + " " + str((tab2[0][1] + tab2[i][1])/2) + "\n")
convfileTestOnline.close()
	
print(displayParameters(modeForDatasetGeneration,bagging,nameOfFile[0],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,lenOfData,numberOfAttributes,online) + "\n" + displayResults(modeForDatasetGeneration,averageCycleSize2,percentageOfNoise,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOffline,lenOfData,lenOfFold,online,offline,"",foldValidation))




decisionThresholdBis = 0.9 # delta for decisionMode = 1

averageCycleSize2,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,sdANoiseOnline,meanAccNoiseOffline,sdANoiseOffline,lenOfData,lenOfFold,numberOfAttributes,meanConvergenceAccuracyOnline,sdConvergenceAccuracyOnline,meanConvergenceAccuracyOffline,sdConvergenceAccuracyOffline = generalProcedure(modeForDatasetGeneration,bagging,nameOfFile,numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,convergence,online,offline,decisionMode,None,autorizedCycle,foldValidation)
	
convfileTestOnline = open("Tests/test_noise_resist_90_Online.dat","w")
tab1 = []
tab2 = []
for key in meanAccNoiseOnline.keys():
	tab1.append([key,meanAccNoiseOnline[key]])
	tab2.append([key,sdANoiseOnline[key]])
tab1.sort()
tab2.sort()
convfileTestOnline.write("0 0.0 0.0\n")
for i in range(1,len(tab1)):
	convfileTestOnline.write(str(tab1[i][0]) + " " + str(abs(tab1[0][1] - tab1[i][1])) + " " + str((tab2[0][1] + tab2[i][1])/2) + "\n")
convfileTestOnline.close()
	
print(displayParameters(modeForDatasetGeneration,bagging,nameOfFile[0],numberOfComparisons,percentageOfNoise,numberOfVariables,numberOfEdgesLambda,numberOfParentsForTargetCPNet,numberOfParentsForLearnedCPNet,numberOfRoundsForFileGeneration,numberOfRoundsForLearningProcedure,decisionThresholdBis,lenOfData,numberOfAttributes,online) + "\n" + displayResults(modeForDatasetGeneration,averageCycleSize2,percentageOfNoise,aOnline,sdAOnline,aOffline,sdAOffline,tOnline,sdTOnline,meanIT,sdIT,tOffline,sdTOffline,meanAccNoiseOnline,meanAccNoiseOffline,lenOfData,lenOfFold,online,offline,"",foldValidation))
