import sys
from loger import Loger
from dfa import FrontendDFA, MinimalistDFA
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

        minimizationType = data['type']
        if minimizationType is None: minimizationType = 0

        if 'automata' not in data:
            raise Exception('No automata provided as parameter in body')

        rawAutomata = data['automata']

        if 'startingState' not in rawAutomata:
            raise Exception('No starting state')

        if 'states' not in rawAutomata or len(rawAutomata['states']) == 0:
            raise Exception('No states found')


        finalStates = [i for i, state in enumerate(rawAutomata["states"]) if state is 1]

        if finalStates is None or len(finalStates) is 0:
            raise Exception('No final states found in automata')

        frontendDFA = FrontendDFA(rawAutomata["startingState"],rawAutomata["transitions"],rawAutomata['states'],rawAutomata['statesLookup'],rawAutomata['symbolsLookup'])
        minimalDFA = MinimalistDFA(frontendDFA.startingState,finalStates,frontendDFA.transitions)

        printOut = ""
        if minimizationType == 0:
            printOut = MooreAlghorithm('log.txt').minimize(minimalDFA)
        else:
            printOut = HopcroftAlghorithm('log.txt').minimize(minimalDFA)

        if printOut is None:
            return json.dumps(frontendDFA.__dict__)

        processed = printOutToFrontend(printOut,rawAutomata["symbolsLookup"], rawAutomata["statesLookup"])
        return json.dumps(processed.__dict__)
    except Exception as error:
        return str(error), 400

# Remove in production
app.run(debug=True)