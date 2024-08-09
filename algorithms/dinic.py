from collections import deque

def dinic(graph, source, sink):
    def bfs(s, t):
        level = [-1] * graph.V
        level[s] = 0
        queue = deque([s])

        while queue:
            u = queue.popleft()
            for e in graph.adj[u]:
                if level[e.v] < 0 and e.flow < e.C:
                    level[e.v] = level[u] + 1
                    queue.append(e.v)
        graph.level = level  # Store levels in the graph object
        return level[t] >= 0

    def dfs(u, flow):
        if u == sink:
            return flow

        for i in range(start[u], len(graph.adj[u])):
            start[u] = i
            e = graph.adj[u][i]

            if graph.level[e.v] == graph.level[u] + 1 and e.flow < e.C:
                curr_flow = min(flow, e.C - e.flow)
                temp_flow = dfs(e.v, curr_flow)

                if temp_flow > 0:
                    e.flow += temp_flow
                    graph.adj[e.v][e.rev].flow -= temp_flow
                    return temp_flow
        return 0

    max_flow = 0
    while bfs(source, sink):
        start = [0] * graph.V
        while True:
            flow = dfs(source, float('Inf'))
            if flow == 0:
                break
            max_flow += flow

    return max_flow