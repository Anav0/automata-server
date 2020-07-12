import sys
from loger import Loger
from dfa import MinimalistDFA
from hopcroft import HopcroftAlghorithm
from moore import MooreAlghorithm
from symbols import acceptingStateChar, startStateChar, noTransitionChar
import argparse
from helpers import minimalistDFAfromFile, printOutToFrontend
from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/minimize',methods=['GET','POST'])
@cross_origin()
def minimize():
    try:
        data = json.loads(request.data)
        minimizationType = int(data['type'])
        rawAutomata = data['automata']

        startingState = rawAutomata['startingState']
        transitionTable = rawAutomata['transitions']
        finalStates = [i for i, state in enumerate(rawAutomata["states"]) if state is 1]

        minimalDFA = MinimalistDFA(startingState,finalStates,transitionTable)
        printOut = ""
        if minimizationType == 0:
            printOut = MooreAlghorithm('log.txt').minimize(minimalDFA)
        else:
            printOut = HopcroftAlghorithm('log.txt').minimize(minimalDFA)

        processed = printOutToFrontend(printOut,rawAutomata["symbolsLookup"], rawAutomata["statesLookup"])
        return json.dumps(processed.__dict__)
    except Exception as error:
        return("Error occured during minimalization")