import math as m

def fromIntToBin(number,numberOfBits):
	binaryVect = [0 for i in range(numberOfBits)]
	while number > 0:
		binaryVect[numberOfBits -1 -m.floor(m.log(number,2))] = 1
		number -= 2**(m.floor(m.log(number,2)))
	return binaryVect
	
def fromBinToInt(binaryVect):
	number = 0
	for i in range(len(binaryVect)-1,-1,-1):
		if binaryVect[i]:
			number += 2**(len(binaryVect) -1 -i)
	return number
	
def flipVariable(outcome1,outcome2):
	for i in range(len(outcome1)):
		if outcome1[i] != outcome2[i]:
			return i
	return -1
	
def VarDoesntChange(varId,listParentsId,length):
	listPossibleParents = []
	for i in range(length):
		if i != varId and not i in listParentsId:
			listPossibleParents.append(i)
	return listPossibleParents
	
def flipState(state,varId):
	fState = list(state)
	fState[varId] = not fState[varId]
	return fState

def existElt(elt,listParents,varId,flip):
	for parent in listParents.keys():
		if elt[parent] != listParents[parent]:
			return False
	if (elt[varId] and not flip) or (not elt[varId] and flip):
		return True
	return False
	
def setOfParentsValue(state,listOfParentsId):
	listOfParentsValue = {}
	for i,id in enumerate(listOfParentsId):
		listOfParentsValue[id] = state[i]
	return listOfParentsValue
	
	
def entropy(c1,c2):
	if c1 == 0 or c2 == 0:
		return 0
	return (-((c1/(2*(c1+c2)))*m.log(c1/(c1+c2))) - ((c2/(2*(c1+c2)))*m.log(c2/(c1+c2))))

def epsilonMcDiarmid(decTh,n):
	if decTh == 0:
		return 0
	return m.log(n)*m.sqrt((2/n)*m.log(4/decTh))+(2/n)

def isASwap(outcome1,outcome2):
	cpt = 0
	swapId = -1
	for i in range(len(outcome1)):
		if outcome1[i] != outcome2[i]:
			cpt += 1
			swapId = i
		if cpt > 1:
			return -1
	return swapId
	
