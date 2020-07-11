from symbols import acceptingStateChar, startStateChar, noTransitionChar

class MinimalistDFA:
    startingState = 0
    finalStates = []
    transitionTable = []
    entriesTable = []
    lookup = {}

    def __init__(self, startingState, finalStates, transitionTable):
        self.startingState = startingState
        self.finalStates = finalStates
        self.transitionTable = transitionTable

    def prepereLookupTable(self):
        for i, s in enumerate(self.transitionTable):
            self.lookup[i] = chr(ord('a') + int(i))

    def prepereEntriesTable(self):
        N = len(self.transitionTable[0])
        M = len(self.transitionTable)
        self.entriesTable = res = [ [ None for o in range(N) ] for j in range(M) ]
        for i, transition in enumerate(self.transitionTable):
            for k, enteredState in enumerate(transition):
                if enteredState is not noTransitionChar:
                    entries = self.entriesTable[int(enteredState)][k]
                    if entries:
                        shouldAdd = True
                        for existing in entries:
                            if existing is i:
                                shouldAdd = False
                        if shouldAdd:
                                self.entriesTable[int(enteredState)][k].append(i)
                    else:
                        self.entriesTable[int(enteredState)][k] = [i]
        return self.entriesTable
