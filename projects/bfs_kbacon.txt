# bfs_kbacon.py

from collections import deque
import networkx as nx
from matplotlib import pyplot as plt
import time

class Graph(object):
    """A graph object, stored as an adjacency dictionary. Each node in the
    graph is a key in the dictionary. The value of each key is a list of the
    corresponding node's neighbors.

    Attributes:
        dictionary: the adjacency list of the graph.
    """

    def __init__(self, adjacency):
        """Store the adjacency dictionary as a class attribute."""
        self.dictionary = adjacency

    def __str__(self):
        """String representation: a sorted view of the adjacency dictionary.

        Example:
            >>> test = {'A':['B'], 'B':['A', 'C',], 'C':['B']}
            >>> print(Graph(test))
            A: B
            B: A; C
            C: B
        """
        to_print = ""
        for key in sorted(self.dictionary.keys()):
            to_print += str(key) + ": " + "; ".join(sorted(self.dictionary[key]))  +"\n"

        return to_print


    def traverse(self, start):
        """Begin at 'start' and perform a breadth-first search until all
        nodes in the graph have been visited. Return a list of values,
        in the order that they were visited.

        Inputs:
            start: the node to start the search at.

        Returns:
            the list of visited nodes (in order of visitation).

        Raises:
            ValueError: if 'start' is not in the adjacency dictionary.

        Example:
            >>> test = {'A':['B'], 'B':['A', 'C',], 'C':['B']}
            >>> Graph(test).traverse('B')
            ['B', 'A', 'C']
        """
        if start not in self.dictionary.keys():
            raise ValueError("Can't start there")

        current = start
        marked = set()
        visited = list()
        visit_queue = deque()

        

        while len(visited) < len(self.dictionary.keys()):
            visited.append(current)
            marked.add(current)
            for neighbors in self.dictionary[current]:
                if neighbors not in marked:
                    visit_queue.append(neighbors)
                marked.add(neighbors)
            if len(visit_queue) != 0:
                current = visit_queue.popleft()
        return visited


    def shortest_path(self, start, target):
        """Begin at the node containing 'start' and perform a breadth-first
        search until the node containing 'target' is found. Return a list
        containg the shortest path from 'start' to 'target'. If either of
        the inputs are not in the adjacency graph, raise a ValueError.

        Inputs:
            start: the node to start the search at.
            target: the node to search for.

        Returns:
            A list of nodes along the shortest path from start to target,
                including the endpoints.

        Example:
            >>> test = {'A':['B', 'F'], 'B':['A', 'C'], 'C':['B', 'D'],
            ...         'D':['C', 'E'], 'E':['D', 'F'], 'F':['A', 'E', 'G'],
            ...         'G':['A', 'F']}
            >>> Graph(test).shortest_path('A', 'G')
            ['A', 'F', 'G']
        """

        if start not in self.dictionary.keys() or target not in self.dictionary.keys():
            raise ValueError("Elements not in the list")


        current = start
        marked = set()
        visited = list()
        visit_queue = deque()
        go = True
        di = {}
        path = []

        

        while go:
            if current == target:
                go = False
                go_second = True
                back = target
                while go_second:
                    path.append(back)
                    back = di[back]
                    if back == start:
                        go_second = False
                        path.append(start)
                        return path[::-1]
            visited.append(current)
            marked.add(current)
            for neighbors in self.dictionary[current]:
                if neighbors not in marked:
                    visit_queue.append(neighbors)
                    di[neighbors] = current
                marked.add(neighbors)
            current = visit_queue.popleft()
        

def convert_to_networkx(dictionary):
    """Convert 'dictionary' to a networkX object and return it."""
    nx_graph = nx.Graph()
    for node in dictionary.keys():
        for edge in dictionary[node]:
            nx_graph.add_edge(node, edge)
    return nx_graph
    

def parse(filename="movieData.txt"):
    """Generate an adjacency dictionary where each key is
    a movie and each value is a list of actors in the movie.
    """

    # open the file, read it in, and split the text by '\n'
    with open(filename, 'r') as movieFile:
        moviesList = movieFile.read().split('\n')
    graph = dict()

    # for each movie in the file,
    for movie in moviesList:
        # get movie name and list of actors
        names = movie.split('/')
        title = names[0]
        graph[title] = []
        # add the actors to the dictionary
        for actor in names[1:]:
            graph[title].append(actor)

    return graph


class BaconSolver(object):
    """Class for solving the Kevin Bacon problem."""

    def __init__(self, filename="movieData.txt"):
        """Initialize the networkX graph and with data from the specified
        file. Store the graph as a class attribute. Also store the collection
        of actors in the file as an attribute.
        """
        self.dictionary = parse(filename)
        self.networkx = convert_to_networkx(self.dictionary)

    def path_to_bacon(self, start, target="Bacon, Kevin"):
        """Find the shortest path from 'start' to 'target'."""
        if start not in self.networkx:
            raise ValueError("I'm sorry, the person you are looking for cannot be found")
        elif target not in self.networkx:
            raise ValueError("I'm sorry, the person you are looking for cannot be found")
        return nx.shortest_path(self.networkx, start, target)

    def bacon_number(self, start, target="Bacon, Kevin"):
        """Return the Bacon number of 'start'."""
        li = self.path_to_bacon(start, target)
        bacon_numbers = 1
        for i in range(0, len(li)):
            if i % 2 == 0:
                bacon_numbers += 1
        return bacon_numbers - 2


    def average_bacon(self, target="Bacon, Kevin"):
        """Calculate the average Bacon number in the data set.
        Note that actors are not guaranteed to be connected to the target.

        Inputs:
            target (str): the node to search the graph for
        """
        total = 0
        count = 0
        not_connected = 0
        actors = set()
        for actor in self.dictionary.values():
            for a in actor:
                actors.add(a)
        
        for actor in actors:
            try:
                total += self.bacon_number(actor, target)
                count += 1
            except:
                not_connected += 1 

        return total/float(count), not_connected

# =========================== END OF FILE =============================== #

if __name__ == "__main__":
    movie_graph = BaconSolver("movieData.txt")
    print movie_graph.average_bacon()
    # print movie_graph.bacon_number("Jackson, Samuel L.")




