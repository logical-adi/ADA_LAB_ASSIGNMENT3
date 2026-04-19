# ADA Lab Assignment 3 - Graph Algorithms
# Author: Adarsh Rai

from collections import deque
import heapq
from itertools import permutations

# -------------------- TASK 1 --------------------
# Graph Representation

graph_adj_list = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

def adjacency_matrix():
    nodes = ['A','B','C','D','E','F']
    n = len(nodes)
    index = {node:i for i,node in enumerate(nodes)}
    matrix = [[0]*n for _ in range(n)]

    edges = [('A','B'),('A','C'),('B','D'),('B','E'),('C','F'),('E','F')]
    for u,v in edges:
        matrix[index[u]][index[v]] = 1
        matrix[index[v]][index[u]] = 1

    return matrix


# -------------------- TASK 2 --------------------
# BFS & DFS

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result


def dfs(graph, start, visited=None, result=None):
    if visited is None:
        visited = set()
        result = []

    visited.add(start)
    result.append(start)

    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, result)

    return result


# -------------------- TASK 3 --------------------
# Topological Sort

def topological_sort(graph):
    visited = set()
    stack = []

    def dfs_inner(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs_inner(neighbor)
        stack.append(node)

    for node in graph:
        if node not in visited:
            dfs_inner(node)

    return stack[::-1]


# -------------------- TASK 4 --------------------
# Shortest Path

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))

    return dist


def bellman_ford(graph, start):
    dist = {v: float('inf') for v in graph}
    dist[start] = 0

    edges = []
    for u in graph:
        for v, w in graph[u]:
            edges.append((u, v, w))

    for _ in range(len(graph)-1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    return dist


# -------------------- TASK 5 --------------------
# Minimum Spanning Tree

def prims(graph, start):
    visited = set([start])
    edges = [(w, start, v) for v, w in graph[start]]
    heapq.heapify(edges)

    mst = []
    total = 0

    while edges:
        w, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, w))
            total += w

            for nv, nw in graph[v]:
                if nv not in visited:
                    heapq.heappush(edges, (nw, v, nv))

    return mst, total


def kruskal(graph):
    parent = {v: v for v in graph}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    edges = []
    for u in graph:
        for v, w in graph[u]:
            if (v, u, w) not in edges:
                edges.append((u, v, w))

    edges.sort(key=lambda x: x[2])

    mst = []
    total = 0

    for u, v, w in edges:
        if find(u) != find(v):
            parent[find(u)] = find(v)
            mst.append((u, v, w))
            total += w

    return mst, total


# -------------------- MAIN --------------------

if __name__ == "__main__":
    print("Adjacency List:", graph_adj_list)

    print("\nBFS:", bfs(graph_adj_list, 'A'))
    print("DFS:", dfs(graph_adj_list, 'A'))

    dag = {
        'A': ['B','C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }

    print("\nTopological Sort:", topological_sort(dag))
