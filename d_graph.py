# Course: CS261 - Data Structures
# Student Name: Steve Thatcher
# Assignment: 6
# Description: This code implements a directed graph class using the Python list ADT.

import heapq

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        This method adds a new vertex to the graph.
        A vertex name does not need to be provided; instead the vertex
        will be assigned a reference index (integer). The first vertex created
        in the graph will be assigned index 0, subsequent vertices will have
        indexes 1, 2, 3 etc. This method returns a single integer - the number
        of vertices in the graph after the addition.
        """
        for list in self.adj_matrix:
            list.append(0)
        new_list = []
        if len(self.adj_matrix) == 0:
            new_list.append(0)
        else:
            for _ in range(len(self.adj_matrix)):  # adds zero to every list
                new_list.append(0)
            new_list.append(0)
        self.adj_matrix.append(new_list)
        self.v_count += 1
        return len(self.adj_matrix)

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        This method adds a new edge to the graph, connecting the two vertices
        with the provided indices. If either (or both) vertex indices do not
        exist in the graph, or if the weight is not a positive integer, or
        if src and dst refer to the same vertex, the method does nothing.
        If an edge already exists in the graph, the method will update its weight.
        """
        if src < 0 or dst < 0:
            return
        if src > (len(self.adj_matrix) - 1) or dst > (len(self.adj_matrix) - 1):
            return
        if weight < 1 or src == dst:
            return
        else:
            self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        This method removes an edge between the two vertices with provided indices.
        If either (or both) vertex indices do not exist in the graph, or if there is
        no edge between them, the method does nothing.
        """
        if src < 0 or dst < 0:
            return
        if src > (len(self.adj_matrix) - 1) or dst > (len(self.adj_matrix) - 1):
            return
        else:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        This method returns a list of the vertices of the graph.
        The order of the vertices in the list does not matter.
        """
        result_list = []
        for _ in range(len(self.adj_matrix)):
            result_list.append(_)
        return result_list

    def get_edges(self) -> []:
        """
        This method returns a list of edges in the graph.
        Each edge is returned as a tuple of two incident vertex indices and weight.
        The first element in the tuple refers to the source vertex.
        The second element in the tuple refers to the destination vertex.
        The third element in the tuple is the weight of the edge.
        The order of the edges in the list does not matter.
        """
        result_list = []
        for src in range(len(self.adj_matrix)):
            for dst in range(len(self.adj_matrix)):
                if self.adj_matrix[src][dst] != 0:
                    result_list.append((src, dst, self.adj_matrix[src][dst]))
        return result_list

    def is_valid_path(self, path: []) -> bool:
        """
        This method takes a list of vertex indices and returns True if the
        sequence of vertices represents a valid path in the graph
        (one can travel from the first vertex in the list to the last vertex
        in the list, at each step traversing over an edge in the graph).
        An empty path is considered valid.
        """
        if not path:
            return True
        if len(path) == 1 and -1 < path[0] < len(self.adj_matrix):
            return True
        curr_index = 0
        curr_v = path[curr_index]
        if curr_index < (len(path) - 1):
            curr_index += 1
            next_v = path[curr_index]
        while curr_index < len(path):
            if self.adj_matrix[curr_v][next_v] == 0:
                return False
            else:
                if curr_index == (len(path) - 1):
                    return True
                elif curr_index < len(path):
                    curr_v = next_v
                    curr_index += 1
                    next_v = path[curr_index]
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        This method performs a depth-first search (DFS) in the graph and returns a list of vertices
        visited during the search, in the order they were visited. It takes one required parameter,
        name of the vertex from which the search will start, and one optional parameter -
        name of the ‘end’ vertex that will stop the search once that vertex is reached.
        If the starting vertex is not in the graph, the method returns an empty list.
        If the name of the ‘end’ vertex is provided but is not in the graph, the search
        is done as if there was no end vertex. Vertices are added as in ascending lexicographical order
        (so, for example, vertex ‘APPLE’ is explored before vertex ‘BANANA’).
        """
        if -1 > v_start > (len(self.adj_matrix) - 1):
            return []
        result_list = []
        working_stack = []
        working_stack.append(v_start)
        while working_stack:
            curr_v = working_stack.pop(-1)
            if curr_v == v_end:
                result_list.append(curr_v)
                return result_list
            elif curr_v not in result_list:
                result_list.append(curr_v)
                temp_list = self.adj_matrix[curr_v]
                #temp_list = sorted(temp_list)
                index_counter = (len(temp_list) - 1)
                while index_counter > -1:
                    temp_val = temp_list[index_counter]
                    if temp_val != 0:
                        working_stack.append(index_counter)
                    index_counter -= 1
        return result_list

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method performs a breadth-first search (BFS) in the graph and returns a list of vertices
        visited during the search, in the order they were visited. It takes one required parameter,
        name of the vertex from which the search will start, and one optional parameter -
        name of the ‘end’ vertex that will stop the search once that vertex is reached.
        If the starting vertex is not in the graph, the method returns an empty list.
        If the name of the ‘end’ vertex is provided but is not in the graph, the search
        is done as if there was no end vertex. Vertices are added as in ascending lexicographical order
        (so, for example, vertex ‘APPLE’ is explored before vertex ‘BANANA’).
        """
        if -1 > v_start > (len(self.adj_matrix) - 1):
            return []
        result_list = []
        working_stack = []
        working_stack.append(v_start)
        while working_stack:
            curr_v = working_stack.pop(0)
            if curr_v == v_end:
                result_list.append(curr_v)
                return result_list
            elif curr_v not in result_list:
                result_list.append(curr_v)
                temp_list = self.adj_matrix[curr_v]
                #temp_list = sorted(temp_list)
                index_counter = 0
                while index_counter < len(temp_list):
                    temp_val = temp_list[index_counter]
                    if temp_val != 0:
                        working_stack.append(index_counter)
                    index_counter += 1
        return result_list

    def has_cycle(self):
        """
        This method returns True if there is at least one cycle in the graph.
        If the graph is acyclic, the method returns False.
        """
        unvisited_vertices = self.get_vertices()
        if not unvisited_vertices:
            return 0
        visited_vertices = []
        traversal_queue = []
        for row_index in range(self.v_count):
            inbound_vertex = False
            if any(vertex > 0 for vertex in self.adj_matrix[row_index]):
                for col_index in range(self.v_count):  # removes vertex with zero or one edges from consideration
                    if self.adj_matrix[col_index][row_index] != 0:
                        inbound_vertex = True
            if inbound_vertex == False:
                unvisited_vertices.remove(row_index)
        while unvisited_vertices:
            next_unqueued_vertex = unvisited_vertices.pop(0)
            traversal_queue.insert(0, next_unqueued_vertex)
            curr_v = None
            while traversal_queue:
                curr_v = traversal_queue.pop(0)
                num_adj_nodes_already_visited = 0
                for v_index in range(self.v_count):
                    if v_index in unvisited_vertices and self.adj_matrix[curr_v][v_index] != 0:
                        traversal_queue.insert(0, v_index)
                        visited_vertices.append(curr_v)
                    elif v_index in visited_vertices:
                        num_adj_nodes_already_visited += 1
                    elif num_adj_nodes_already_visited > 1:
                        return True
                if num_adj_nodes_already_visited > 1:
                    return True
                if curr_v in unvisited_vertices:
                    unvisited_vertices.remove(curr_v)
        return False

    def dijkstra(self, src: int) -> []:
        """
        This method implements the Dijkstra algorithm to compute the length
        of the shortest path from a given vertex to all other vertices in the
        graph. It returns a list with one value per each vertex in the graph,
        where the value at index 0 is the length of the shortest path from
        vertex SRC to vertex 0, the value at index 1 is the length of the shortest
        path from vertex SRC to vertex 1 etc.
        If a certain vertex is not reachable from SRC, the returned value is INFINITY
        (float(‘inf’)).
        """
        result_list_for_src = []  # list to store the lowest weight between src and the index storing the weight
        vertices_curr_combined_weight_dict = {}  # creates new dictionary to stores indices and their initial weights
        for index in range(len(self.adj_matrix)):
            if src == index:  # if the current vertex is the same as the src, store 0 weight
                vertices_curr_combined_weight_dict[index] = 0
            elif self.adj_matrix[src][index] == 0:  # if src and current index are not adjacent, store 'inf'
                vertices_curr_combined_weight_dict[index] = float('inf')
            else:  # if src and current index are adjacent, store the weight between them for initial value
                vertices_curr_combined_weight_dict[index] = self.adj_matrix[src][index]
        remaining_vertices = []
        visited_vertices = []
        remaining_vertices.insert(0, src)  # initial run, set current vertex to src
        while remaining_vertices:  # all vertices must be checked, so loop until list is empty
            curr_v = remaining_vertices.pop(0)
            if curr_v in remaining_vertices:
                remaining_vertices.remove(curr_v)
            visited_vertices.append(curr_v)
            curr_v_combined_weight = vertices_curr_combined_weight_dict.get(curr_v)  # retrieves current vertex weight
            for index in range(len(self.adj_matrix)):  # iterates through the index of all vertexes
                if self.adj_matrix[curr_v][index] != 0:  # if current index is not adjacent to the current vertex its weights cannot be updated
                    if index not in visited_vertices:
                        remaining_vertices.insert(0, index)
                    if ((curr_v_combined_weight) + self.adj_matrix[curr_v][index]) < vertices_curr_combined_weight_dict.get(index):  # if the combined weight of the current vertex's weight and the edge between the vertex and the current adjacent vertex is less than the weight stored for the current adjacent vertex, update the weight of the current adjacent vertex
                        vertices_curr_combined_weight_dict[index] = (
                                    (curr_v_combined_weight) + self.adj_matrix[curr_v][index])
            adjacent_vertex_with_lowest_weight = float(
                'inf')  # creates a variable to track the index of the vertex that is BOTH adjacent to current vertex and which has the lowest weight
            weight_of_adjacent_vertex_with_lowest_weight = float('inf')
            for index in range(len(self.adj_matrix)):
                if index in remaining_vertices:
                    if vertices_curr_combined_weight_dict[index] < weight_of_adjacent_vertex_with_lowest_weight:
                        weight_of_adjacent_vertex_with_lowest_weight = vertices_curr_combined_weight_dict[index]
                        adjacent_vertex_with_lowest_weight = index
            if adjacent_vertex_with_lowest_weight != float('inf'):
                remaining_vertices.insert(0, adjacent_vertex_with_lowest_weight)
        for index in range(len(self.adj_matrix)):
            result_list_for_src.append(vertices_curr_combined_weight_dict[index])
        return result_list_for_src

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - method has_cycle() example 2")
    print("----------------------------------")
    edges = [(0, 12, 11), (1, 7, 16), (1, 8, 19), (3, 0, 10), (4, 2, 18), (4, 3, 20), (5, 7, 10), (6, 11, 17), (8, 2, 6), (10, 2, 20), (11, 9, 8), (11, 12, 20)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.has_cycle(), sep='\n')


    print("\nPDF - method has_cycle() example 3")
    print("----------------------------------")
    edges = [(0, 2, 2), (2, 4, 2), (3, 9, 6), (3, 10, 16), (4, 1, 20), (5, 4, 7), (8, 4, 5), (8, 5, 13), (10, 1, 13), (11, 3, 6), (11, 12, 14)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.has_cycle(), sep='\n')

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')



    print("\nPDF - dijkstra() example 2")
    print("--------------------------")
    edges = [(0, 12, 10), (1, 8, 18), (4, 2, 16), (6, 10, 4), (6, 12, 15), (7, 6, 19), (7, 8, 20), (9, 3, 8), (10, 5, 3), (10, 12, 14), (11, 6, 10), (11, 8, 19), (11, 9, 18) ]
    g = DirectedGraph(edges)
    print(f'DIJKSTRA {i} {g.dijkstra(11)}')


    print("\nPDF - dijkstra() example 3")
    print("--------------------------")
    edges = [(0, 1, 16), (0, 6, 16), (2, 8, 14), (2, 9, 20), (2, 10, 1), (3, 2, 4), (7, 4, 9), (7, 11, 16), (8, 6, 4), (10, 4, 9), (11, 3, 9), (11, 12, 3), (12, 2, 17), (12, 4, 10)]
    g = DirectedGraph(edges)
    print(f'DIJKSTRA {i} {g.dijkstra(7)}')


    print("\nPDF - dijkstra() example 4")
    print("--------------------------")
    edges = [(0, 2, 5), (1, 12, 18), (2, 10, 8), (3, 8, 18), (4, 1, 15), (4, 7, 8), (5, 7, 12), (5, 10, 14), (7, 0, 14), (7, 2, 7), (7, 5, 6), (10, 8, 5), (11, 4, 17), (12, 9, 19)]
    g = DirectedGraph(edges)
    print(f'DIJKSTRA {i} {g.dijkstra(7)}')