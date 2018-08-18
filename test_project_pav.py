def calculate_min_route(distance_map, suggestion):
    """starting from the first state in the list, calculates and selects the closest state and then from that state again the next closest state and so on, builds a string comprising all the states selected sequentially and returns the total driving distance calculated"""
    state_list = []
    print( suggestion)
    state_list.append(suggestion[0])
    sum = 0
    print( '1' )
    for state in suggestion:
        #state = state_list[-1]
        initial_distances = list(distance_map[state].values())
        str_distances = list(filter(None, initial_distances))
        distances = []
        print('2')
        for value in str_distances:
            distances.append(float(value))
        states = list(distance_map[state].keys())
        smallest_distance = min(distances)
        if states[distances.index(smallest_distance)] in suggestion:
            if states[distances.index(smallest_distance)] not in state_list:
                print('4')
                state_list.append(states[distances.index(smallest_distance)])
                sum += smallest_distance
        states.remove(states[distances.index(smallest_distance)])
        distances.remove(smallest_distance)
    print(state_list)
    return ( state_list, 0 )

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

def main():
    stateInfo = read_state_file( 'states.csv' )
    itemDict = build_itemDict( stateInfo )
    personDatabase = read_person_file( 'person.csv' )
    #suggestion = make_suggestion( personDatabase, itemDict )
    s = make_suggestion( {'A':['food']}, itemDict )
    distanceMap = build_dist_map( 'dist.csv' )
    ( route, driveDist ) = calculate_min_route( distanceMap, s['A'] )
    
    print( route, driveDist )
    
if __name__ == '__main__':
    main()

