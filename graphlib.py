class Node:

    def __init__(self, name: str):
        self.__name = name.lower()
        self.__neighbours = dict()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def neighbours(self) -> dict:
        return self.__neighbours

    def add_neighbour(self, node: "Node", cost: int) -> None:
        self.__neighbours[node.name] = cost

    def __repr__(self):
        return f"Node name: {self.name}. Node neighbours: {self.neighbours} \n"


class Graph:

    def __init__(self):
        self.__graph = list()
        self.__size = 0
        self.__cost_table = dict()
        self.__processed_table = dict()
        self.__begin_node = None
        self.__end_node = None

    @property
    def size(self) -> int:
        return self.__size

    @property
    def get(self) -> list:
        return self.__graph

    @property
    def begin_node(self) -> "Node":
        return self.__begin_node

    @begin_node.setter
    def begin_node(self, node: "Node") -> None:
        self.__begin_node = node

    @property
    def end_node(self) -> "Node":
        return self.__end_node

    @end_node.setter
    def end_node(self, node: "Node") -> None:
        self.__end_node = node

    def add_node(self, node: "Node") -> None:
        self.__graph.append(node)

    def get_node(self, name: str) -> "Node":
        for node in self.__graph:
            if node.name == name.lower():
                return node

    def __prepare_search_proc(self):

        for i in self.__begin_node.neighbours:
            self.__cost_table[i] = self.__begin_node.neighbours[i]
            self.__processed_table[i] = self.__begin_node.neighbours[i]

        for j in self.get:
            curr_node_name = j.name
            if curr_node_name != self.__begin_node.name and \
                    curr_node_name not in self.__begin_node.neighbours:
                self.__cost_table[curr_node_name] = float("+inf")
                self.__processed_table[curr_node_name] = float("+inf")

    def find_min_node_cost(self) -> tuple:
        node_names = [*self.__processed_table.keys()]
        min_node_name = node_names[0]
        min_node_cost = self.__processed_table[min_node_name]

        for i in range(1, len(node_names)):
            if self.__processed_table[node_names[i]] < min_node_cost:
                min_node_name = node_names[i]
                min_node_cost = self.__processed_table[node_names[i]]

        return min_node_name, min_node_cost

    def find_shortest_path(self):
        if self.__begin_node is None or self.__end_node is None:
            raise Exception("Initialize points first!")
        self.__prepare_search_proc()
        while len(self.__processed_table) != 0:
            min_node_name, min_node_cost = self.find_min_node_cost()
            neighbours = self.get_node(min_node_name).neighbours
            if len(neighbours) != 0:
                for neighbour in neighbours:
                    new_cost = min_node_cost + neighbours[neighbour]
                    if new_cost < self.__cost_table[neighbour]:
                        self.__cost_table[neighbour] = new_cost
                        self.__processed_table[neighbour] = new_cost
            self.__processed_table.pop(min_node_name)

    @property
    def end_node_min_cost(self):
        return self.__cost_table[self.__end_node.name]


def graph_init():
    graph = Graph()
    node_names = [*input("Enter nodes names: ").lower().split()]
    nodes = []
    for i in node_names:
        t = Node(i)
        nodes.append(t)
    for node in nodes:
        graph.add_node(node)

    tmp = []
    for j in graph.get:
        while True:
            lp = tuple(input(f"Enter neighbour and cost for node {j.name}: ").split())
            if len(lp) > 0 and lp[0] not in node_names:
                print("This node doesn't exist. Create a node first")
                continue
            if len(lp) > 0 and lp[0] == j.name:
                print("The node cannot be the neighbour itself!")
                continue
            if 0 < len(lp) < 2:
                print("Expected 2 parameters")
                continue
            if len(lp) == 0:
                break
            tmp.append(lp)
        for i, l in tmp:
            j.add_neighbour(graph.get_node(i), int(l))
        tmp.clear()

    start_node = None

    while start_node is None:
        i = input("Enter start node: ")
        noda = graph.get_node(i)
        if noda:
            start_node = noda

    end_node = None

    while end_node is None:
        i = input("Enter end node: ")
        noda = graph.get_node(i)
        if noda:
            end_node = noda

    graph.begin_node = start_node
    graph.end_node = end_node

    return graph


if __name__ == '__main__':
    graph = graph_init()
    graph.find_shortest_path()
    print(graph.end_node_min_cost)
