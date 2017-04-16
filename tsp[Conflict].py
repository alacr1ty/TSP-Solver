#!/usr/bin/env

'''
# CS325 Project 4 - Traveling Salesman Problem
# Ava Cordero
# Alston Godbolt
# Soo-Min Yoo
    Starting from a degenerate tour consisting of the two farthest 
cities, repeatedly choose the non-tour city with the minimum 
distance to its nearest neighbor among the tour cities, and make 
that city the next in the tour. 2-Opt uncrosses any lines in the 
tour until there are no more mor crossed paths, thereby optimizing 
the tour. 2-opt uses a deque to improve the tour moving in both
directions while accessing each next element in O(n) time.
'''
import sys,time,numpy
from math import *
from collections import OrderedDict,deque
import matplotlib.pyplot as plt

# define a utility function-set to quick-peak a standard deque
# Quick Peak [Right]
def qp (dek):
    # if there are elements in the deque
    if dek:
        # return the value of the next element on the right side of the deque
        var = dek.pop()
        # without popping (deleting that element)
        dek.append(var)
        return var
    # else return boolean false
    else:
        return False
# Quick Peak Left
def qpl (dek):
    if dek:
        var = dek.popleft()
        dek.appendleft(var)
        # returns an analagous value to .qp(), but for the left side of the deque
        return var
    else:
        return False

# define a data container class
class dict_deque (object):
    # it is initialized by calling 'dd = dict_deque()'
    def __init__(self):
        # it stores values in a deque
        self.v = deque()
        # while storing a dict of it's original keys for reverse lookup
        self.k = {}
    # call 'dd = dict_deque() ; dd.mutate(old_dict)' to mutate any dict object into a new dict_deque
    def mutate(self,tour):
        # dd.v stores a deque to traverse the graph in a 2-d plane in O(1)
        self.v = deque(tour.values())
        # and dd.k stores a dict of all previous keys
        self.k = {}
        # which can be accessed as an object like 'dd.k.iteritems()'' etc
        for key,value in tour.iteritems():
            # or individually like 'dd.k[str(value)]'
            self.k[str(value)] = key
    # Append to the right side of the dict_deque like you would any deque
    def append (self,item):
        if item:
            self.v.append(item.values()[0])
            self.k[str(item.values()[0])] = item.keys()[0]
        else:
            return False
    # Append to left side
    def appendleft (self,item):
        if item:
            self.v.appendleft(item.values()[0])
            # they dict items but should be first mutated using dd.mutate(dict)
            self.k[str(item.values()[0])] = item.keys()[0]
        else:
            return False

    # Pop rightmost element dict_deque, returns None if empty
    def pop (self):
        try:
            # the dict_deque item is mutated into a key/value pair
            val = self.v.popleft()
            key = self.k[str(val)]
            # the element is no longer available by 'key' or popping
            del self.k[str(val)]
            # the object is returned as a standard key/value pair
            return {key:val}
        except:
            return False

    # Pop leftmost element in the dict deque
    def popleft (self):
        try:
            val = self.v.popleft()
            key = self.k[str(val)]
            del self.k[str(val)]
            # the object is returned as a standard key/value pair
            return {key:val}
        except:
            return False
    # Quick Peak [Right]
    def qp (self):
        # Checks if the deque is available to popping
        if qp(self.v):
            # calls higher level dd.pop() to get a dict_deque item
            var = self.pop()
            # but leaves the item in the dict_deque for later usage
            self.append(var)
            return var
        else:
            # returns False if dict_deque is empty
            return False
    # Quick Peak Left
    def qpl (self):
        if qpl(self.v):
            var = self.popleft()
            self.appendleft(var)
            # analogous with dd.qp() but for the left side of the dict_deque
            return var
        else:
            return False

# Function Get_Distance returns the distance of two tuples
# or dict_deque items where a=(x1,y1),b=(x2,y2)
def get_distance(a,b):
    # if the items are dict_deques, destringify the coordinates
    if isinstance(a,dict) and isinstance(b,dict):
        if type(a.values()) is list: a[0],a[1] = a.values()[0][0],a.values()[0][1]
        if type(b.values()) is list: b[0],b[1] = b.values()[0][0],b.values()[0][1]
    if isinstance(a,str) and isinstance(b,str):
        a = [float(i) for i in a.strip("[]").split(", ")] ;
        b = [float(i) for i in b.strip("[]").split(", ")] ;
    # uncomment to print distance measured to console
    # print 'distance: ', sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)
    return sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

# Function Get_Line_length returns the length of a line from u to v
def get_line_length (tour):
    seen = []
    distance = 0
    # works for deques, dicts, and ordered dicts
    # if its a deque
    if isinstance(tour,deque):
        while qp(tour):
            cp = tour.pop()
            if len(seen) > 0:
                distance += get_distance(cp,qp(tour))
            seen.append(qp(tour))
        return distance
    # if its a dict
    elif isinstance(tour,dict_deque):
        op = tour.pop()
        cp =  op
        while tour.qp():
            cp = tour.qp()
            distance += get_distance(cp.keys(),tour.pop().keys())
        return distance
    # if its an OrderedDict
    elif isinstance(tour,OrderedDict):
        for node in tour:
            if len(seen) > 0:
                distance += get_distance(tour[next(reversed(seen))],tour[node])
            seen.append(node)
        return distance

# Greedy approximation tour construction algorithm
# Add nodes to graph whose distance to the last tour node is minimal
def greedy_construction (graph):
    # Step 1. Find two cities farthest from each other to create a starting tour.
    # initialize an ordered dict of cities
    tour_coords = OrderedDict()
    # initialize max distance
    max_distance = 0
    # initialize keys of cities to remove from graph
    tour_a = 0; tour_b = 0

    # while there are cities left to be checked,
    for i in range(0, len(graph)-1): # loop a
        for j in range(i+1, len(graph)): # loop b
            # pick next two cities in graph to check inter-city distance
            a = graph[i]; b = graph[j]
            # get distance between first city a and a second city b
            distance = get_distance(a,b)

            # if the calculated distance is greater than the current max distance, update the max distance
            if distance > max_distance:
                max_distance = distance
                # update the keys of cities with the maximum inter-city distance
                tour_a = i; tour_b = j

    # add the cities to the dict of cities
    tour_coords[tour_a] = graph[tour_a]; tour_coords[tour_b] = graph[tour_b]
    # remove the two cities from the graph
    del graph[tour_a]; del graph[tour_b]
    
    # Step 2. Repeatedly add a city from the graph with the maximum distance from the last city added to the tour, until graph is empty.
    # while there are cities left in graph,
    while len(graph) > 0:
        # initialize a second ordered dict for containing a city to later put into the tour
        city = OrderedDict()
        # initialize min distance
        min_distance = float('inf')
        # initialize key of city to remove from graph
        tour_city = 0
        # for each city in graph,
        for key,value in graph.iteritems():
            # set city a as the latest city added to the tour and set city b as the next city to check in graph
            c = tour_coords[next(reversed(tour_coords))]; 
            d = value        
            # get distance between city a and city b
            distance = get_distance(c,d)

            # if the calculated distance is less than the current min distance, update the max distance and key of that farthest city
            if distance < min_distance:
                min_distance = distance
                # update the key of city with the min inter-city distance to latest city in tour
                tour_city = key
                tour_coord = value

        # add the nearest city to the city dict
        city[tour_city] = tour_coord   
        # add nearest city to the tour
        tour_coords.update(city)
        # remove the city from the graph
        if len(graph) > 0:
            del graph[tour_city]

    return tour_coords

# Function 2-OPT(route, i, k):
# Takes a tour and spit out something better.
def two_opt (tour):
    # # convert tour values to deque -- need only happen first time...
    new_tour = dict_deque()
    new_tour.mutate(tour)
    btr = 1
    while btr > 0 :
        # make copy of tour coords
        cur_tour = new_tour
        # initialize a new tour
        new_tour = dict_deque()
        # pop the first and last cities from the old tour to the new
        new_tour.append(cur_tour.pop())
        new_tour.appendleft(cur_tour.popleft())
        # while there are at least two tour cities left to check
        while cur_tour.qp():
            loc_dist = get_distance(new_tour.qp(),new_tour.qpl())
            rem_dist = get_distance(cur_tour.qp(),cur_tour.qpl())
            RR_dist = get_distance(new_tour.qp(),cur_tour.qp())
            RL_dist = get_distance(new_tour.qp(),cur_tour.qpl())
            LL_dist = get_distance(new_tour.qpl(),cur_tour.qpl())
            LR_dist = get_distance(new_tour.qpl(),cur_tour.qp())
            # if the two paths cross
            if (RL_dist < RR_dist) or (LR_dist < LL_dist) or (RR_dist/RL_dist > 1) or (LL_dist/LR_dist > 1):
                # swap dest with neighbors dest
                new_tour.append(cur_tour.popleft())
                new_tour.appendleft(cur_tour.pop())
                btr += 1
            # else leave the tour as it is.
            else:
                new_tour.append(cur_tour.pop())
                new_tour.appendleft(cur_tour.popleft())
                btr -= 1
            print 'btr: ',btr

    return new_tour

# Function Output Tour finds distance and tour and prints to output file
def output_tour (tour,ofile):
    with open(ofile+'.tour','w+') as output:
        print_list = []
        seen = []
        distance = 0
        # if the tour is a dict_deque...
        if isinstance(tour,dict_deque):
            route = OrderedDict(tour.k)
            distance = get_distance(tour.qp(),tour.qpl())
            for k in route:
                print_list.append(route[k])
                if len(seen) > 0:
                    distance += get_distance(k,next(iter(route)))
                seen.append(k)
        # else if the tour is an OrderedDict
        elif isinstance(tour,OrderedDict):
            route = tour
            distance = get_distance(route[next(iter(route))],route[next(reversed(route))])
            for city in route:
                print_list.append(city)
                if len(seen) > 0:
                    distance += get_distance(route[next(reversed(seen))],route[city])
                seen.append(city)
        # print the total distance to output file
        output.write(str(int(distance)))
        output.write('\n')
        # print the tour to output file
        for item in print_list:
            output.write(str(item))
            output.write('\n')
    return

def plot_graph (tour):
    # Test-code to plot the tour
    # Uncomment line 16 for graph plotting (not supported on flip).
    # needs bebugging for dict_deque
    # Assign tour keys for plotting.
    pts = numpy.array(tour.k.keys())
    # Get the indices of the hull points.
    hull_indices = numpy.array(tour.k.values())
    # These are the actual points.
    hull_pts = pts[hull_indices,:]
    # set the graph configurations
    plt.plot(pts[:, 0], pts[:, 1], 'ko', markersize=3)
    plt.fill(hull_pts[:,0], hull_pts[:,1], fill=False, edgecolor='b')
    # plt.xlim(0, x)
    # plt.ylim(0, y)
    plt.show()
    return

#Converts txt file to python dict of format {node:(x,y)}
def file_to_dict (file):
    graph = {}
    file = open(file,'r+')
    for line in file:
        (node,x,y) = line.split()
        graph[int(node)] = [float(x),float(y)]
    return graph

# Validates input file and calls file_to_dict() to return a valid
def validate (arg_list=[],*arg):
    # must have only one argument
    if len(arg_list) is 2:
        arg = arg_list[1]
        # must be a .txt file
        if arg.lower().endswith('.txt'):
            try:
                # attempt to create a dict
                return file_to_dict(arg)
            except:
                # exit if the file is of invalid format
                print "Input file line format must be 'N X Y' for Node number, X-coordinate, and Y-coordinate."
                exit()
            return graph
        # exit if its not
        else:
            print "Accepts .txt files exclusively."
            exit()
    # exit if its not
    else:
        print "Accepts 1 argument input file exclusively."
        exit()

# Main function
def main ():
    # validate the input and assign it to graph
    graph = validate(sys.argv)

    # find the best tour we can and print the runtime.
    t0 = time.clock()

    tour = two_opt(greedy_construction(graph))
    # tour = greedy_construction(graph)

    # print runtime to console
    print 'RUNTIME: ',(time.clock()-t0)

    # output tour data to .tour file
    output_tour(tour,sys.argv[1])

    # plot graph using numpy (not supported on FLIP)
    plot_graph(tour)

    return

if __name__ == '__main__':
    main()
    exit()
