from tqdm import tqdm

class Graph:

    class Node:

        def __init__(self, name, flow):
            self.name = name
            self.flow = flow

        def __eq__(self, other):
            return (self.name, self.flow) == (other.name, other.flow)

        def __hash__(self) -> int:
            return hash((self.name, self.flow))

        def __repr__(self) -> str:
            return f'name: {self.name}, flow: {self.flow}'

    nodes = {}
    distances = {}
    meaningful_nodes = []

    def __init__(self, graph_desc):
        self.create_all_nodes(graph_desc)
        for line in graph_desc:
            node_name = line.split()[1]
            root = self.get_node_by_name(node_name)
            adjs = line.split()[9:]
            for adj in adjs:
                node = self.get_node_by_name(adj.replace(',', ''))
                self.nodes[root].append(node)
        self.cal_distances()
    
    def create_all_nodes(self, graph_desc):
        for line in graph_desc:
            line = line.split()
            name = line[1]
            flow = int(line[4].split('=')[1].replace(';', ''))
            node = Graph.Node(name, flow)
            self.nodes[node] = []
            if node.flow > 0:
                self.meaningful_nodes.append(node)
        self.meaningful_nodes.append(self.get_node_by_name('AA'))

    def cal_distances(self):
        for m_node in self.meaningful_nodes:
            self.distances[m_node] = []
            dists = self.all_nodes_distances(m_node)
            for n, dist in dists.items():
                if n in self.meaningful_nodes:
                    self.distances[m_node].append((n, dist))

    def get_node_by_name(self, node_name):
        for n in self.nodes:
            if n.name == node_name:
                return n

    def all_nodes_distances(self, start):
        queue = []
        visited = {node:False for node in self.nodes}
        dists = {node:float('inf') for node in self.nodes}

        queue.append(start)
        visited[start] = True
        dists[start] = 0

        while len(queue):
            curr = queue.pop(0)

            for adj in self.nodes[curr]:
                if not visited[adj]:
                    visited[adj] = True
                    dists[adj] = dists[curr]+1
                    queue.append(adj)
        return dists

    def max_flow(self):
        best = 0
        start = [self.meaningful_nodes[-1]]
        subsets = generate_n_intersec_subsets(self.meaningful_nodes[:-1], start.copy(), start.copy())
        for sub_ele, sub_me in tqdm(subsets[:len(subsets)//2+1]):
            best = max(best, self._max_flow(start[0], 26, start, sub_ele) + \
                             self._max_flow(start[0], 26, start, sub_me))
        return best
    
    def _max_flow(self, curr, time_left, valvs_on, subset):

        if time_left <= 0:
            return 0

        best = 0
        for node, dist in self.distances[curr]:
            if node in valvs_on:
                continue
            
            if node not in subset:
                continue

            best = max(best, self._max_flow(node, time_left-(dist+1), [*valvs_on, node], subset))
        
        return best + (curr.flow*time_left)
            
    def __str__(self):
        ans = ''
        for node, value in self.nodes.items():
            ans += f'{node};\tvizinhos: {value}\n'
        return ans

def generate_n_intersec_subsets(remaning, sub_a = [], sub_b = []):
    if not len(remaning):
        return [(sub_a, sub_b)]
    
    next = remaning[0]
    return [*generate_n_intersec_subsets(remaning[1:], [*sub_a.copy(), next], sub_b.copy()),
            *generate_n_intersec_subsets(remaning[1:], sub_a.copy(), [*sub_b.copy(), next])]


g = Graph(open('input.txt').readlines())
print(g.max_flow())