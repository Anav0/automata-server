from symbols import acceptingStateChar, startStateChar, noTransitionChar
from dfa import MinimalistDFA, FrontendDFA

def minimalistDFAfromFile(filePath):
    startingState = 0
    finalStates = []
    transitionTable = []
    with open(filePath,'r') as file:
        index = 0
        for line in file:
            if index == 0:
                index+=1
                continue
            splitedLine = line.strip().split("\t")
            if startStateChar in splitedLine[0]:
                startingState = index-1
            if acceptingStateChar in splitedLine[0]:
                finalStates.append(index-1)
            transition = []
            for i, char in enumerate(splitedLine):
                if i == 0: continue
                transition.append(splitedLine[i])
            transitionTable.append(transition)
            index+=1

        return MinimalistDFA(startingState,finalStates,transitionTable)

def getAutomataPrintOut(P,automata):
    printOut = "\t"
    helperSet = {noTransitionChar: noTransitionChar}
    for i, symbol in enumerate(automata.transitionTable[0]):
        printOut+=str(i)+"\t"
    printOut+="\n"
    # iterating two times just to get proper prit out may be costly
    for subset in P:
        gluedStates = ''.join(str(x) for x in subset);
        for state in subset:
            helperSet[str(state)] = gluedStates
    for subset in P:
        addStartStateMarker = False
        addFinishStateMarker = False
        for state in subset:
            printOut+=str(state)
            if state in automata.finalStates:
                addFinishStateMarker = True
            if state is automata.startingState:
                addStartStateMarker = True

        printOut+=acceptingStateChar if addFinishStateMarker else ""
        printOut+=startStateChar if addStartStateMarker else ""
        printOut+="\t"
        printOut+='\t'.join(helperSet[str(x)] for x in automata.transitionTable[subset[0]]);
        printOut+="\n"
    return printOut[:-1]

def splitOff(array,toSplit):
    a = []
    b = []
    for value in array:
        if value in toSplit:
            b.append(value)
        else:
            a.append(value)
    if b and a:
        return [a,b]
    else:
        return [a]

def printOutToFrontend(printOut, symbolsLookup, statesLookup):
    startingState = 0
    index = 0
    statesLookup = {y:x for x,y in statesLookup.items()}
    transitionTable = []
    newStatesLookup = {}
    splitedByLines = printOut.strip().split("\n")
    splitedByLines = splitedByLines[1:]
    states = [0] * len(splitedByLines)

    for line in splitedByLines:
        splitedLine = line.strip().split("\t")
        if startStateChar in splitedLine[0]:
            startingState = index
            splitedLine[0] = splitedLine[0][:-1]
        if acceptingStateChar in splitedLine[0]:
            states[index] = 1
            splitedLine[0] = splitedLine[0][:-1]
        for i, gluedStates in enumerate(splitedLine):
            if startStateChar in gluedStates or acceptingStateChar in gluedStates:
                gluedStates = gluedStates[:-1]
            newStateName = ''.join([statesLookup[int(state)] for state in list(gluedStates)])
            newStatesLookup[newStateName] = index
            break
        index+=1

    for line in splitedByLines:
        splitedLine = line.strip().split("\t")
        transition = []
        for i, gluedStates in enumerate(splitedLine):
            if i==0: continue
            newStateName = ''.join([statesLookup[int(state)] for state in list(gluedStates)])
            transition.append(newStatesLookup[newStateName])
        transitionTable.append(transition)

    return FrontendDFA(startingState,transitionTable,states,newStatesLookup,symbolsLookup)