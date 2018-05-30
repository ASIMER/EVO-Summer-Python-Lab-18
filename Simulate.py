import random
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument('filepath', nargs=1)
parser.add_argument('-n', nargs=1, type=int, dest='nodes', default=20)
parser.add_argument('-i', nargs=1, type=int, dest='runtimes', default=1000)
parser.add_argument('--gossip', dest='gossip', action='store_true')
parser.add_argument('--my-gossip', dest='my_gossip', action='store_true')
parser.add_argument('--my-gossip100', dest='my_gossip100', action='store_true')
parser.add_argument('--my-gossip-split', dest='my_gossip_split', action='store_true')
varlist = parser.parse_args(sys.argv)

def start_algorithm(algorythm, current, times, nodes, runtimes, *args):
    reslist = []
    iterations = [0]
    for i in range(runtimes):
        list = [0 for i in range(nodes)]
        if len(args) == 0:
            algorythm(current, times, list, iterations)
        else:
            algorythm(current, times, list, iterations, args)
        reslist.append(list.count(1) * 100 / nodes)
    result = 0
    for i in reslist:
        result += i
    result = result / len(reslist)

    return "{0}% with {1} avg iterations({2} total)".format(
        str(round(result, 2)),
        str(iterations[0] / runtimes),
        str(iterations[0]))

def gossip(current, times, list, iterations):
    iterations[0] = iterations[0] + 1
    if list[current] == 0:
        list[current] = 1
        for i in range(times):
            gossip(random.randrange(0,(len(list))), times, list, iterations)
    else:
        return 1

def my_gossip(current, times, list, iterations):
    iterations[0] = iterations[0] + 1
    if list[current] == 0:
        list[current] = 1
        for i in range(times):
            x = random.randrange(0,(len(list)))
            while (x == current):
                x = random.randrange(0,(len(list)))
            my_gossip(x, times, list, iterations)
    else:
        return 1

def my_gossip_split(current, times, list, iterations):
    iterations[0] = iterations[0] + 1
    if list[current] == 0:
        list[current] = 1
        for i in range(times):
            first_part = list[:int(len(list)/2)].count(1)
            second_part = list[int(len(list)/2):].count(1)
            if first_part == int(len(list)/2) and second_part == int(len(list)/2):
                return 1
            elif first_part >= second_part:
                x = random.randrange(int(len(list)/2),len(list))
                while (x == current):
                    x = random.randrange(int(len(list)/2),len(list))
            else:
                x = random.randrange(0,int(len(list)/2))
                while (x == current):
                    x = random.randrange(0,int(len(list)/2))
            my_gossip_split(x, times, list, iterations)
    else:
        return 1

def my_gossip100(current, times, nodelist, iterations, *args):
    iterations[0] = iterations[0] + 1
    if len(args) == 0:
        visited = []
    elif type(args[0]) is list:
        visited = args[0]
    else:
        visited = []

    if nodelist[current] == 0:
        nodelist[current] = 1
        for i in range(times):
            x = random.randrange(0,(len(nodelist)))
            if len(visited) == len(nodelist):
                return 1
            while (x == current or x in visited):
                x = random.randrange(0,(len(nodelist)))
            visited += [x]
            my_gossip100(x, times, nodelist, iterations, visited)
    else:
        return 1


if not (varlist.my_gossip or varlist.my_gossip_split or varlist.my_gossip100):
    print(start_algorithm(gossip, 0, 4, varlist.nodes[0], varlist.runtimes[0]))

else:
    if varlist.gossip:
        print("standart gossip:")
        print(start_algorithm(gossip, 0, 4, varlist.nodes[0], varlist.runtimes[0]))
    if varlist.my_gossip:
        print("my_gossip:")
        print(start_algorithm(my_gossip, 0, 4, varlist.nodes[0], varlist.runtimes[0]))

    if varlist.my_gossip_split:
        print("my_gossip_split:")
        print(start_algorithm(my_gossip_split, 0, 4, varlist.nodes[0], varlist.runtimes[0]))

    if varlist.my_gossip100:
        print("my_gossip100:")
        print(start_algorithm(my_gossip100, 0, 4, varlist.nodes[0], varlist.runtimes[0]))
exit