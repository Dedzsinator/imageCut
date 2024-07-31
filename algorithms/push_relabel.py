def push_relabel(graph, source, sink):
    def push(u, v, e):
        flow = min(excess[u], e.C - e.flow)
        e.flow += flow
        graph.adj[v][e.rev].flow -= flow
        excess[u] -= flow
        excess[v] += flow

    def relabel(u):
        min_height = float('inf')
        for e in graph.adj[u]:
            if e.flow < e.C:
                min_height = min(min_height, height[e.v])
        height[u] = min_height + 1

    def discharge(u):
        while excess[u] > 0:
            for e in graph.adj[u]:
                if e.flow < e.C and height[u] == height[e.v] + 1:
                    push(u, e.v, e)
                    if excess[u] == 0:
                        break
            if excess[u] > 0:
                relabel(u)

    V = graph.V
    excess = [0] * V
    height = [0] * V

    height[source] = V
    excess[source] = float('inf')
    for e in graph.adj[source]:
        push(source, e.v, e)

    for u in range(V):
        if u != source and u != sink:
            discharge(u)

    return excess[sink]
