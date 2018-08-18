def read_state_file( filename ):    
    stateFile = open( filename, 'r' )
    stateInfo = {}
    for aLine in stateFile:
        line = aLine.strip().split(',')
        stateInfo[line[0]] = line[1:]
    stateFile.close()
    return stateInfo

def build_itemDict( stateInfo ):
    itemList = []
    for items in stateInfo.values():
        for item in items:
            if item not in itemList:
                itemList.append( item )
    itemDict = {}
    for item in itemList:
        states = []
        for state in stateInfo:
            if item in stateInfo[state]:
                states.append( state )
        itemDict[item] = states
    return itemDict

def read_person_file( filename ):
    personFile = open( filename, 'r' )
    personInfo = {}
    for aLine in personFile:
        line = aLine.strip().split(',')
        personInfo[line[0]] = line[1:]
    personFile.close()
    return personInfo

def make_suggestion( personDatabase, itemDict ):
    suggestedStates = {}
    for aperson in personDatabase.keys():
        suggestion = set()
        for item in personDatabase[aperson]:
            suggestion = suggestion | set( itemDict[item] )
        suggestedStates[aperson] = sorted( list( suggestion ))
    return suggestedStates

def build_dist_map( filename ):
    distFile = open( filename, 'r' )
    distMap = {}
    states = []
    firstLine = distFile.readline().strip().split(',')
    for element in firstLine:
        states.append( element )
    states = states[1:]
    for line in distFile:
        line = line.strip().split(',')
        distMap[line[0]] = dict( zip( states, line[1:]))
    return distMap

def calculate_min_route( distMap, suggestedStates ):
    driveDist = 0
    currentState = suggestedStates[0]
    route = currentState
    suggestedStates = suggestedStates[1:]
    while( len(suggestedStates) ):
        minDist = 5000
        temp = ''
        for state in suggestedStates:
            if float( distMap[currentState][state] ) < minDist and float( distMap[currentState][state] ) != 0:
                minDist = float( distMap[currentState][state] )
                temp = state
        currentState = temp
        route += ' > ' + currentState
        driveDist += minDist
        suggestedStates.remove( temp )
    return ( route, driveDist )

def main():
    stateInfo = read_state_file( 'states.csv' )
    itemDict = build_itemDict( stateInfo )
    personDatabase = read_person_file( 'person.csv' )
    suggestion = make_suggestion( personDatabase, itemDict )
    distanceMap = build_dist_map( 'dist.csv' )
    ( route, driveDist ) = calculate_min_route( distanceMap, suggestion['Someone'] )
    
    print( route, driveDist )
    
if __name__ == '__main__':
    main()