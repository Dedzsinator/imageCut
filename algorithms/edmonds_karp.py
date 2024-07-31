from collections import deque

def edmonds_karp(graph, source, sink):
    def bfs(s, t, parent):
        visited = [False] * graph.V
        queue = deque([s])
        visited[s] = True

        while queue:
            u = queue.popleft()
            for i, e in enumerate(graph.adj[u]):
                if not visited[e.v] and e.flow < e.C:
                    queue.append(e.v)
                    visited[e.v] = True
                    parent[e.v] = (u, i)
                    if e.v == t:
                        return True
        return False

    parent = [-1] * graph.V
    max_flow = 0

    while bfs(source, sink, parent):
        path_flow = float('Inf')
        s = sink
        while s != source:
            u, i = parent[s]
            path_flow = min(path_flow, graph.adj[u][i].C - graph.adj[u][i].flow)
            s = parent[s][0]

        max_flow += path_flow
        v = sink
        while v != source:
            u, i = parent[v]
            graph.adj[u][i].flow += path_flow
            graph.adj[v][graph.adj[u][i].rev].flow -= path_flow
            v = parent[v][0]

    return max_flow
