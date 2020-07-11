from loger import Loger
from helpers import splitOff, getAutomataPrintOut

class MooreAlghorithm:
    markers = []

    def __init__(self,logPath):
        self.loger = Loger(logPath)
        self.loger.clear()

    def getMarkersPrint(self):
        printOut = ''
        for i,row in enumerate(self.markers):
            whitespace = '   '*i
            printOut += '{}{}\n'.format(whitespace,row[i:])
        return printOut

    def glueStates(self):
        P = []
        whatWasGlued = []
        allStates = []
        for i,row in enumerate(self.markers):
            cutRow = row[i:]
            allStates.append(i)
            glued = []
            for k, column in enumerate(cutRow):
                if k == 0: continue
                truePos = k+i
                if column == 0 and truePos not in whatWasGlued:
                    glued.append(truePos)
                    whatWasGlued.append(truePos)
            if glued:
                P.append(glued+[i])
                whatWasGlued.append(i)

        # add states that were not glued
        diff = splitOff(allStates,whatWasGlued)[0]
        P+=[[x] for x in diff]
        return P

    def minimize(self,automata):
        automata.prepereEntriesTable()
        L = []
        N = len(automata.transitionTable)
        self.markers = res = [ [ 0 for i in range(N) ] for j in range(N) ]

        for i, transition in enumerate(automata.transitionTable):
            for finalState in automata.finalStates:
                if i not in automata.finalStates:
                    L.append([finalState, i])
                    self.markers[finalState][i] = 1
                    self.markers[i][finalState] = 1

        index = 1
        turnLength = len(L)
        rawIndex = 1;
        self.loger.log('Tura 1')

        while L:
            pair = L.pop(0)

            if turnLength+1 == rawIndex:
                index+=1
                rawIndex = 1
                turnLength = len(L)
                self.loger.log('\nTura {}'.format(index))

            for symbol, d in enumerate(automata.transitionTable[0]):
                entries1 = automata.entriesTable[pair[0]][symbol]
                entries2 = automata.entriesTable[pair[1]][symbol]
                self.loger.log('---------')
                self.loger.log('Pair: [{},{}] symbol: {}'.format(pair[0],pair[1],symbol))
                if entries1 is None or entries2 is None:
                    continue
                self.loger.log('{} is entered by: '.format(pair[0])+' '.join(str(x) for x in entries1))
                self.loger.log('{} is entered by: '.format(pair[1])+' '.join(str(x) for x in entries2))
                for entry in entries1:
                    for entry2 in entries2:
                        if self.markers[entry][entry2] == 0 and self.markers[entry2][entry] == 0:
                            self.loger.log('Can be added: {} {}'.format(entry, entry2))
                            L.append([entry, entry2])
                            self.markers[entry][entry2] = index+1
                            self.markers[entry2][entry] = index+1
            rawIndex+=1
        self.loger.log('\n')
        printOut = self.getMarkersPrint()
        P = self.glueStates()
        automataPrintOut = getAutomataPrintOut(P,automata)
        self.loger.log(printOut)
        self.loger.log('Glued states: {}'.format(str(P)))
        self.loger.log(automataPrintOut)
        return automataPrintOut