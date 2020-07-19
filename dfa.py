from symbols import acceptingStateChar, startStateChar, noTransitionChar
from apiError import ApiError

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

class FrontendDFA:
    startingState = 0
    transitions = []
    states = []
    statesLookup = {}
    symbolsLookup = {}

    def __init__(self,startingState,transitions,states,statesLookup,symbolsLookup):
        self.startingState=startingState
        self.transitions=transitions
        self.states = states
        self.statesLookup=statesLookup
        self.symbolsLookup=symbolsLookup
        self.validate()

    def validate(self):
        if self.startingState is None:
            raise ApiError('No starting state','Starting state cannot be null')
        if self.transitions is None or len(self.transitions) < 1:
            raise ApiError('No transitions','No transitions found')
        if self.states is None or len(self.states) < 1:
            raise ApiError('Lack of states','No states found')

        for key in self.statesLookup:
            stateName = key.strip()
            if stateName == "":
                raise ApiError('Noname state','One of states has no name')

        finalStates = [i for i, state in enumerate(self.states) if state is 1]

        if finalStates is None or len(finalStates) < 1:
            raise ApiError('No final state','No final states found')

        flipedSymbolsLookup = {value: key for key, value in self.symbolsLookup.items()}
        flipedStateLookup = {value: key for key, value in self.statesLookup.items()}
        numberOfSymbols = len(self.symbolsLookup)
        errorMsg = ""
        for stateIndex, transition in enumerate(self.transitions):
            for i in range(numberOfSymbols):
                missingSymbols = ''
                if i >= len(transition):
                    errorMsg += 'State {}  lacks transition via {}\n'.format(flipedStateLookup[stateIndex], flipedSymbolsLookup[i])
                elif i < len(transition) and transition[i] is None:
                    errorMsg += 'State {} lacks transition via {}\n'.format(flipedStateLookup[stateIndex], flipedSymbolsLookup[i])

        if errorMsg: raise ApiError('Inconsistent transitions',errorMsg)