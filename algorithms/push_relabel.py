import sys
import os
import cv2
import numpy as np
import time
from collections import defaultdict, deque

class Edge:
    def __init__(self, v, flow, capacity, rev):
        self.v = v
        self.flow = flow
        self.capacity = capacity
        self.rev = rev

class Graph:
    def __init__(self, V):
        self.V = V
        self.adj = defaultdict(list)

    def add_edge(self, u, v, capacity):
        a = Edge(v, 0, capacity, len(self.adj[v]))
        b = Edge(u, 0, 0, len(self.adj[u]))
        self.adj[u].append(a)
        self.adj[v].append(b)

def push_relabel(graph, source, sink):
    def push(u, e):
        v = e.v
        delta = min(excess[u], e.capacity - e.flow)
        e.flow += delta
        graph.adj[v][e.rev].flow -= delta
        excess[u] -= delta
        excess[v] += delta
        if excess[v] == delta:
            if v != source and v != sink:
                active.append(v)

    def relabel(u):
        min_height = float('inf')
        for e in graph.adj[u]:
            if e.flow < e.capacity:
                min_height = min(min_height, height[e.v])
        height[u] = min_height + 1

    def gap_heuristic(gap_height):
        for u in range(V):
            if height[u] >= gap_height:
                height[u] = max(height[u], V + 1)

    def discharge(u):
        while excess[u] > 0:
            if current_edge[u] < len(graph.adj[u]):
                e = graph.adj[u][current_edge[u]]
                if e.flow < e.capacity and height[u] == height[e.v] + 1:
                    push(u, e)
                else:
                    current_edge[u] += 1
            else:
                gap_heuristic(height[u])
                relabel(u)
                current_edge[u] = 0

    def global_relabel():
        new_height = [float('inf')] * V
        new_height[sink] = 0
        queue = deque([sink])
        while queue:
            u = queue.popleft()
            for e in graph.adj[u]:
                if graph.adj[e.v][e.rev].capacity > graph.adj[e.v][e.rev].flow and new_height[e.v] == float('inf'):
                    new_height[e.v] = new_height[u] + 1
                    queue.append(e.v)
        return new_height

    V = graph.V
    excess = [0] * V
    height = [0] * V
    current_edge = [0] * V
    active = deque()

    height[source] = V
    excess[source] = float('inf')
    for e in graph.adj[source]:
        push(source, e)

    global_relabel_counter = 0
    global_relabel_threshold = 0.5 * V

    while active:
        u = active.popleft()
        discharge(u)
        global_relabel_counter += 1
        if global_relabel_counter >= global_relabel_threshold:
            height = global_relabel()
            global_relabel_counter = 0

    return excess[sink]