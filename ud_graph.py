# Course: CS261 - Data Structures
# Student Name: Steve Thatcher
# Assignment: 6
# Description: This code implements an undirected graph class using the Python dictionary
#              and list ADTs



class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        This method adds a new vertex to the graph,
        nothing done if a vertex with the same name is already present in the graph.
        """
        for key in self.adj_list:
            if v == key:  # if vertex is already in graph, return nothing
                return
        self.adj_list[v] = []  # add list to dictionary
        
    def add_edge(self, u: str, v: str) -> None:
        """
        This method adds a new edge to the graph,
        connecting the two vertices with the provided names.
        If either (or both) vertex names do not exist in the graph,
        this method will first create them and then create an edge between them.
        If an edge already exists in the graph, or if u and v refer to the same vertex,
        the method does nothing (no exception needs to be raised).
        """
        if u == v:  # if passed vertices are the same, return nothing
            return
        if u not in self.adj_list:
            self.add_vertex(u)  # adds first passed vertex if not in graph
        if v not in self.adj_list:
            self.add_vertex(v)  # adds second passed vertex if not in graph
        for key in self.adj_list:
            if u == key:
                if v not in self.adj_list[u]:
                    self.adj_list[key].append(v)  # adds second vertex to first vertex list
            if v == key:
                if u not in self.adj_list[v]:
                    self.adj_list[key].append(u)  # adds first vertex to second vertex list

    def remove_edge(self, v: str, u: str) -> None:
        """
        This method removes an edge between the two vertices with provided names.
        Does nothing if either (or both) vertex names do not exist in the graph,
        or if there is no edge between them.
        """
        if u == v:
            return  # does nothing if vertices match
        if u not in self.adj_list:
            return  # does nothing first vertex is not in graph
        if v not in self.adj_list:
            return  # does nothing first vertex is not in graph
        for key in self.adj_list:
            if u == key:
                if v in self.adj_list[u]:
                    self.adj_list[key].remove(v)  # removes second vertex from first vertex list
            if v == key:
                if u in self.adj_list[v]:
                    self.adj_list[key].remove(u)  # removes first vertex from second vertex list

    def remove_vertex(self, v: str) -> None:
        """
        This method removes a vertex with a given name and
        all edges incident to it from the graph.
        Does nothing if the given vertex does not exist.
        """
        if v not in self.adj_list:
            return  # if vertex not in graph, return nothing
        for key in self.adj_list:
            if v == key:
                for value in self.adj_list[v]:
                    self.adj_list[value].remove(v)
        del self.adj_list[v]
        

    def get_vertices(self) -> []:
        """
        This method returns a list of vertices of the graph.
        The order of the vertices in the list does not matter.
        """
        return list(self.adj_list)

    def get_edges(self) -> []:
        """
        This method returns a list of edges in the graph.
        Each edge is returned as a tuple of two incident vertex names.
        The order of the edges in the list or the order of the vertices incident to each edge does not matter.
        """
        result_list = []
        for key in self.adj_list:
            for value in self.adj_list[key]:
                if (value, key) not in result_list:
                    result_list.append((key, value))
        return result_list

    def is_valid_path(self, path: [], first_key = None, second_key = None) -> bool:
        """
        This method takes a list of vertex names and returns True if the
        sequence of vertices represents a valid path in the graph
        (so one can travel from the first vertex in the list to the last vertex in the list,
        at each step traversing over an edge in the graph). An empty path is considered valid.
        """
        if not path and not first_key and not second_key:
            return True
        elif first_key is None and path:
            first_key = path.pop(0)
            return self.is_valid_path(path, first_key, second_key)
        elif first_key in self.adj_list and not second_key and not path:
            return True
        elif first_key not in self.adj_list:
            return False
        elif second_key is None and path:
            second_key = path.pop(0)
            return self.is_valid_path(path, first_key, second_key)
        elif second_key not in self.adj_list:
            return False  # if second key not in list return False
        elif first_key and second_key:
            if second_key not in self.adj_list[first_key]:
                return False
            elif path:
                first_key = second_key
                second_key = path.pop(0)
                return self.is_valid_path(path, first_key, second_key)
            else:
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
        if v_start not in self.adj_list:
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
                temp_list = self.adj_list[curr_v]
                temp_list = sorted(temp_list)
                while temp_list:
                    temp_val = temp_list.pop(-1)
                    working_stack.append(temp_val)
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
        if v_start not in self.adj_list:
            return []
        result_list = []
        working_queue = []
        working_queue.append(v_start)
        while working_queue:
            curr_v = working_queue.pop(0)
            if curr_v == v_end:
                result_list.append(curr_v)
                return result_list
            elif curr_v not in result_list:
                result_list.append(curr_v)
                temp_list = self.adj_list[curr_v]
                temp_list = sorted(temp_list)
                while temp_list:
                    temp_val = temp_list.pop(0)
                    working_queue.append(temp_val)
        return result_list

    def count_connected_components(self):
        """
        This method returns the number of connected components in the graph.
        """
        vertices = self.get_vertices()
        if not vertices:
            return 0
        v_to_visit = []
        counter = 0
        while vertices:
            v_to_visit.append(vertices.pop(0))
            while v_to_visit:
                curr_v = v_to_visit.pop()
                for value in self.adj_list[curr_v]:
                    if value in vertices:
                        v_to_visit.append(value)
                        vertices.remove(value)
            counter += 1  # count how many vertices are in the component
        return counter

    def has_cycle(self):
        """
        This method returns True if there is at least one cycle in the graph.
        If the graph is acyclic, the method returns False.
        """
        unvisited_vertices = self.get_vertices()
        if not unvisited_vertices:
            return 0
        elif self.count_connected_components() == 0:
            return False
        visited_vertices = []
        traversal_queue = []
        for key in self.adj_list:  # removes vertex with zero or one edges from consideration
            if len(self.adj_list.get(key)) < 2 or len(self.adj_list.get(key)) is None:
                unvisited_vertices.remove(key)
        while unvisited_vertices:
            next_unqueued_vertex = unvisited_vertices.pop(0)
            traversal_queue.insert(0, next_unqueued_vertex)
            while traversal_queue:
                curr_v = traversal_queue.pop(0)
                num_adj_nodes_already_visited = 0
                for adj_v in self.adj_list[curr_v]:
                    if adj_v in visited_vertices:
                        num_adj_nodes_already_visited += 1
                    elif num_adj_nodes_already_visited > 1:
                        return True
                    elif adj_v in unvisited_vertices:
                        traversal_queue.insert(0, adj_v)
                if num_adj_nodes_already_visited > 1:
                    return True
                visited_vertices.append(curr_v)
                if curr_v in unvisited_vertices:
                    unvisited_vertices.remove(curr_v)
        return False



if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
