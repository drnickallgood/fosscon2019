'''
Problem Statement:

We will map a 3-node graph onto the D-Wave 2000Q and assume all nodes will start out as a superposition of colors 'red' and 'blue' and any and all colors you can create from the combination of those two. We wish to come up with a solution to get only one node as color 'red' and the rest as color 'blue'

There are 3 possible solutions

node0 = red, node1, node2 = blue
node1 = red, node0, node2 = blue
node2 = red, node0, node1 = blue

For the purposes of the coupling on the D-wave, we have the following values:

  1 = red
 -1 = blue

We will have the following mappings:

node0 -> qubit0
node1 -> qubit5
node2 -> qubit4

Values will be different per adjacent qubit so we need to negatively correlate 

'''
from dwave_sapi2.remote import RemoteConnection
from dwave_sapi2.core import solve_ising
from dwave_sapi2.embedding import find_embedding, embed_problem, unembed_answer
from dwave_sapi2.util import get_hardware_adjacency
import sys
import pprint

# function/method to get API token from local file
def getToken():
    try:
        tokenFile = open("dwave-token.txt", "r")
    except IOError:
        print "Error opening file"
        sys.exit(-1)
    token = tokenFile.read()
    tokenFile.close()
    return token

# Decodes results
def decodeResults(qubits, mapping):
    result_map = dict()
    result_map['node0'] = qubits[0][mapping['node0']]
    result_map['node1'] = qubits[0][mapping['node1']]
    result_map['node2'] = qubits[0][mapping['node2']]

    return result_map
    
url = 'https://cloud.dwavesys.com/sapi'
token = getToken()
conn = RemoteConnection(url, token)
solver_name = "DW_2000Q_2_1"

# Couplers for linked qubits along with coupler strength (dictionary)
J = {(0,4): 1, (0,5): 1}

# Maps node's to qubits
nodeQubitMap = dict()
nodeQubitMap['node0'] = 0
nodeQubitMap['node1'] = 4
nodeQubitMap['node2'] = 5

# Bias values, we only want one solution, and only using 6 qubits
# (list)
# Zero-indexed q0 - q5
#h = [-1,0,0,0,1,1]    # This will get -5.0 energies for num_occurences
h = [-1,0,0,0,0,0]

solver = conn.get_solver(solver_name)

# Results as a histogram, displays in order of num_occurences
# 10,000 samples
params = {"answer_mode": 'histogram', "num_reads": 10000}

#collect results
raw_results = solve_ising(solver, h, J, **params)

pprint.pprint(raw_results['timing'])
# We want -3.0 as the correct ground state energy
sys.stdout.write('Energies: ')
pprint.pprint(raw_results['energies'])
sys.stdout.write('Num Occurences: ')
pprint.pprint(raw_results['num_occurrences'])
print("\n--- RAW RESULTS ---\n")
print(raw_results['solutions'])
print("\n--- DECODED RESULTS ---\n")
#print(decodeResults(raw_results['solutions'],nodeQubitMap))
usefulResults = decodeResults(raw_results['solutions'], nodeQubitMap)

pprint.pprint(usefulResults)

print("\n")
