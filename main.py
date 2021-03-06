import os
import sys
from loger import Loger
from dfa import FrontendDFA, MinimalistDFA
from hopcroft import HopcroftAlghorithm
from moore import MooreAlghorithm
from symbols import acceptingStateChar, startStateChar, noTransitionChar
from helpers import minimalistDFAfromFile, printOutToFrontend
from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
from apiError import ApiError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json


app = Flask(__name__)
cors = CORS(app, origins=['https://www.drawing-automata.xyz', 'localhost'])
app.config['CORS_HEADERS'] = 'Content-Type'
limiter = Limiter(
    app,
    key_func=get_remote_address,
)

@app.route('/minimize',methods=['POST'])
@cross_origin()
@limiter.limit('1 per second')
def minimize():
    try:
        try:
            data = json.loads(request.data)
        except Exception as error:
            raise ApiError('No body','No JSON body found')

        if 'type' in data:
            minimizationType = data['type']
        else:
            minimizationType = 0

        if 'automata' not in data:
            raise ApiError('Bad parameters','No automata provided as parameter in body')

        rawAutomata = data['automata']

        if 'startingState' not in rawAutomata:
            raise ApiError('No start state','No starting state')

        if 'states' not in rawAutomata or len(rawAutomata['states']) == 0:
            raise ApiError('Empty automata','No states found')


        finalStates = [i for i, state in enumerate(rawAutomata["states"]) if state == 1]

        if finalStates is None or len(finalStates) == 0:
            raise ApiError('No final state','No final states found in automata')

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
    except ApiError as error:
        return json.dumps(error.__dict__), 400
    except Exception as erro2:
        return str(erro2), 500

# Remove in production

if 'PORT' in os.environ:
    port = os.environ['PORT']
else:
    port = 5000

app.run(debug=False,host='0.0.0.0',port=port)