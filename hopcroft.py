from loger import Loger
from symbols import acceptingStateChar, startStateChar, noTransitionChar, symbolSplitChar, statesSplitChar
import copy
from helpers import splitOff, getAutomataPrintOut

class HopcroftAlghorithm:

    def __init__(self,logPath):
        self.loger = Loger(logPath)
        self.loger.clear()

    def minimize(self, automata):
        L = []
        P = [automata.finalStates]
        entries = automata.prepereEntriesTable()

        # initialize P and L
        regularStates = []
        for i, state in enumerate(automata.transitionTable):
            if i not in automata.finalStates:
                regularStates.append(i)
        P.append(regularStates)

        # put smaller list on L
        toPutOnListL = []
        if len(P[0]) < len(P[1]):
            toPutOnListL = statesSplitChar.join(str(x) for x in P[0])
        else:
            toPutOnListL = statesSplitChar.join(str(x) for x in P[1])

        for i,d in enumerate(automata.transitionTable[0]):
            L.append('{}{}{}'.format(toPutOnListL,symbolSplitChar,i))

        # as long as there are elements in L
        loopCounter = 1;
        while L:
            self.loger.log('\n======== {}. loop ========\n'.format(loopCounter))
            self.loger.log('P: {}'.format(P))
            self.loger.log('L: {}'.format(L))
            itemFromL = L.pop(0)
            splited = itemFromL.split(symbolSplitChar)
            states = splited[0].split(statesSplitChar)
            symbol = splited[1]
            #print('{} {} {}'.format(splited,states,symbol))
            whatEnteres = []
            for state in states:
                potentialEntry = automata.entriesTable[int(state)][int(symbol)]
                if not potentialEntry:
                    continue
                else:
                    whatEnteres += potentialEntry

            # łamanie
            if not whatEnteres:
                self.loger.log('Nothing enters {} via symbol: {}'.format(states,symbol))
                loopCounter+=1
                continue
            self.loger.log('States: {} are entering {} via symbol: {}'.format(whatEnteres,states,symbol))
            tmpP = copy.deepcopy(P)
            self.loger.log('\nLooking for subset \'B\' of P to break apart')
            for i, B in enumerate(P):
                splited = splitOff(B, whatEnteres)
                if len(splited) > 1:
                    self.loger.log('\n{}. B: {} broken by: {} to: {}'.format(i+1,B,whatEnteres,splited))
                    tmpP.remove(B)
                    for split in splited:
                        tmpP.append(split)
                    self.loger.log('P after breaking up: {}'.format(tmpP))
                    # Uzupełnienie list L
                    flattenB = ''.join(str(x) for x in B)
                    wasFoundInL = False
                    self.loger.log('L before filling: {}'.format(L))
                    for g, element in enumerate(L):
                        split = element.split(symbolSplitChar)
                        states = split[0].split(statesSplitChar)
                        symbol = split[1]
                        joinedStates = "".join(states)

                        if flattenB in joinedStates:
                            replaced = L.pop(g)
                            for split in splited:
                                joinedSplit = statesSplitChar.join(str(x) for x in split)
                                self.loger.log('Replaced {} with {} in L'.format(replaced,joinedSplit+symbol))
                                L.insert(g,joinedSplit+symbolSplitChar+symbol)
                            wasFoundInL = True

                    if not wasFoundInL:
                        if len(splited[0]) != len(splited[1]):
                            splited = sorted(splited,key=len)
                            smallerBreak = splited[0]
                        else:
                            smallerBreak = splited[1]

                        smallerBreak = '-'.join(str(x) for x in smallerBreak)
                        for i, transition in enumerate(automata.transitionTable[0]):
                            L.append(smallerBreak+symbolSplitChar+str(i))
                            self.loger.log('Added {} to L'.format(smallerBreak+str(i)))
                    self.loger.log('L after filling: {}'.format(L))
                else:
                    self.loger.log('\n{}. B: {} cannot be broken by {}'.format(i+1,B,whatEnteres))
            P = tmpP
            loopCounter+=1
        self.loger.log("\n")
        self.loger.log('Final P: {}'.format(P))
        automataPrint = getAutomataPrintOut(P,automata)
        self.loger.log("\nMinimized automata transition table:\n")
        self.loger.log(automataPrint)
        return automataPrint;


