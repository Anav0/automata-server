import sys
from loger import Loger
from dfa import MinimalistDFA
from hopcroft import HopcroftAlghorithm
from moore import MooreAlghorithm
from symbols import acceptingStateChar, startStateChar, noTransitionChar
import argparse
from helpers import minimalistDFAfromFile

def main():
    parser = argparse.ArgumentParser(description='Minimizes automata from file using Hopcroft or Moore alghorithm')
    parser.add_argument('filePath', metavar='f', help='path to transition table of DFA')
    parser.add_argument('alghorithm', metavar='a', help='alghorithm name to use: moore or hopcroft')
    parser.add_argument('--logPath', metavar='l', help='path to store log file')
    args = parser.parse_args()

    # W pliku log.txt jest szczegółowy opis kroków jakie podejmuje algorytm
    logPath = sys.argv[0]
    fileName = sys.argv[1]
    alghorithmName = sys.argv[2].lower().strip()
    if logPath:
        logPath = 'zad66/log.txt'
    automata = minimalistDFAfromFile(fileName)
    hopcroft = HopcroftAlghorithm(logPath)

    if alghorithmName == 'moore':
        moore = MooreAlghorithm(logPath)
        print(moore.minimize(automata))
    elif alghorithmName == 'hopcroft':
        print(hopcroft.minimize(automata))
    else:
        print(hopcroft.minimize(automata))

if __name__ == "__main__":
    main()

