from collections import deque, defaultdict
import sys
import cv2
import os
import numpy as np

class Edge:
    def __init__(self, v, flow, C, rev, capacity = 0):
        self.v = v
        self.flow = flow
        self.C = C
        self.rev = rev
        self.capacity = capacity

class Graph:
    def __init__(self, V):
        self.V = V
        self.adj = defaultdict(list)

    def add_edge(self, u, v, C):
        a = Edge(v, 0, C, len(self.adj[v]))
        b = Edge(u, 0, 0, len(self.adj[u]))
        self.adj[u].append(a)
        self.adj[v].append(b)

    def bfs(self, s, t, parent):
        visited = [False] * self.V
        queue = [s]
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for e in self.adj[u]:
                if not visited[e.v] and e.flow < e.C:
                    queue.append(e.v)
                    visited[e.v] = True
                    parent[e.v] = u
                    if e.v == t:
                        return True
        return False

class ImageSegmentation:
    def __init__(self, img, output_dir, img_name):
        self.image = img
        self.height, self.width, _ = img.shape
        self.foreground = np.zeros_like(img)
        self.background = np.zeros_like(img)
        self.output_dir = output_dir
        self.img_name = img_name

    def save_results(self):
        cv2.imwrite(os.path.join(self.output_dir, f"{self.img_name}_fg.jpg"), self.foreground)
        cv2.imwrite(os.path.join(self.output_dir, f"{self.img_name}_bg.jpg"), self.background)

    def setup_graph(self, bg_threshold):
        V = self.width * self.height + 2
        graph = Graph(V)
        source = V - 2
        sink = V - 1

        for i in range(self.height):
            for j in range(self.width):
                node = i * self.width + j
                intensity = np.mean(self.image[i, j])
                if intensity <= bg_threshold:
                    graph.add_edge(source, node, sys.maxsize)
                else:
                    graph.add_edge(node, sink, sys.maxsize)
                if i > 0:
                    graph.add_edge(node, (i - 1) * self.width + j, 1)
                if i < self.height - 1:
                    graph.add_edge(node, (i + 1) * self.width + j, 1)
                if j > 0:
                    graph.add_edge(node, i * self.width + (j - 1), 1)
                if j < self.width - 1:
                    graph.add_edge(node, i * self.width + (j + 1), 1)
        return graph, source, sink

    def segment(self, bg_threshold, algo):
        graph, source, sink = self.setup_graph(bg_threshold)
        max_flow = algo(graph, source, sink)

        for i in range(self.height):
            for j in range(self.width):
                node = i * self.width + j
                parent = [-1] * graph.V
                if graph.bfs(source, node, parent):
                    self.foreground[i, j] = self.image[i, j]
                else:
                    self.background[i, j] = self.image[i, j]
        self.save_results()