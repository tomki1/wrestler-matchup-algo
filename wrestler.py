# wrestler.py
# name: Kimberly Tom
# CS325 Homework 5

import sys
import os

def main():
    wrestlerGraph = parse()

    # Repeat until all wrestlers have been looked at

    while True:
        wrestler = findUnvisited(wrestlerGraph['graph'])

        if wrestler == "all wrestlers looked at":
            break

        # call bfs algorithm
        bfs(wrestlerGraph['graph'], wrestler)

    # vertices with even type are baby faces and all vertices with odd type are heels
    # Check that every edge goes between an even and odd type

    rivalriesOK = True

    graph = wrestlerGraph['graph']
    edges = wrestlerGraph['edges']

    # each edge needs to be between a odd and even vertex to be true
    for edge in edges:
        dist1 = graph[edge[0]]['type']
        dist2 = graph[edge[1]]['type']
        result = dist2 - dist1

        # if there is a result that does not go between an odd or even, then rivalriesOK is set to false
        if result % 2 == 0:
            rivalriesOK = False

    # if rivalries OK is false, then print impossible
    if not rivalriesOK:
        print("Impossible")

    # else, print the teams
    else:
        print("Yes Possible")

        teamBabyFace = ""
        teamHeels = ""

        # if type is even, then wrestler is a babyface, else wrestler is a heel
        for wrestler in wrestlerGraph['graph']:
            if wrestlerGraph['graph'][wrestler]['type'] % 2 == 0:
                teamBabyFace += wrestler + " "
            else:
                teamHeels += wrestler + " "


        print("Babyfaces: " + teamBabyFace)
        print("Heels: " + teamHeels)

# Parse to create a graph where each wrestler is a key in a dictionary
def parse():
    # read the file name that the user types
    textFile = sys.argv[1]

    # assert that it exists
    assert os.path.exists(textFile), "Error: A file with that name is not in the same directory."

    # open the text file
    readFile = open(textFile, "r")

    # Read the lines
    lines = readFile.readlines()

    graph = {}  # create empty dictionary
    wrestlersCount = 0  # number of wrestlers
    edgesCount = 0  # edges between wrestler
    totalEdges = 0  # total edges between wrestlers
    edges = []  # create array of edges between wrestlers
    loopCount = 0  # loop count

    for line in lines:
        # Remove all leading and trailing spaces from string
        line = line.strip()

        # if we are at the first line, then it is the number of wrestlers
        if loopCount == 0:
            wrestlersCount = int(line)

        # create graph that has wrestlers as keys, and values as visited, type, and edges
        if 0 < loopCount <= wrestlersCount:
            if loopCount == 1:
                beginning = line

            # each line represents a wrestler, if it is not a number
            # for each wrestler, initialize visited to false, type to zero, and edges to empty
            graph[line] = {
                'visited': False,
                'type': 0,
                'edges': []
            }

        # once we hit the next integer, it is not a wrestler, but the number of edges
        # store number in totalEdges
        if loopCount == wrestlersCount + 1:
            totalEdges = int(line)

        # create edges between wrestlers, this simulates the pairings
        if loopCount > (wrestlersCount + 1) and edgesCount < totalEdges:
            # split the string into an array of substring
            # https://www.pythonforbeginners.com/dictionary/python-split
            wrestler = line.split()
            edges.append(wrestler)
            graph[wrestler[0]]['edges'].append(wrestler[1])
            graph[wrestler[1]]['edges'].append(wrestler[0])
            # increment edge count
            edgesCount += 1

        # increment loop count
        loopCount += 1

    # close the file
    readFile.close()

    # return the parsed info
    return {
        'beginning': beginning,
        'graph': graph,
        'edges': edges
    }



# BFS algorithm
# with help from https://www.programiz.com/dsa/graph-bfs
def bfs(graph, beginning):
    queue = [beginning]

    # set wrestlers we visited from false to true
    graph[beginning]['visited'] = True

    # while there are still wrestlers in the queue
    while queue:
        wrestler = queue.pop(0) # pop the wrestler
        type = graph[wrestler]['type'] + 1

        for neighborWrestler in graph[wrestler]['edges']:
            if not graph[neighborWrestler]['visited']:
                graph[neighborWrestler]['visited'] = True
                graph[neighborWrestler]['type'] = type
                queue.append(neighborWrestler)

    return graph



# finds unvisited wrestler in the graph
def findUnvisited(graph):
    for wrestler in graph:
        if not graph[wrestler]['visited']:
            return wrestler

    # return all wrestlers looked at once all have been visited
    return "all wrestlers looked at"


# call main function to start program
if __name__ == '__main__':
    main()