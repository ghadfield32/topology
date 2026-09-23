"""Small finite topology experiments and graph connectivity."""
from itertools import combinations
import numpy as np

def powerset(values):
    values = tuple(values)
    return [frozenset(s) for k in range(len(values) + 1) for s in combinations(values, k)]

def is_topology(universe, opens) -> bool:
    """Finite universes only: binary unions imply all unions of this finite family."""
    x = frozenset(universe)
    t = set(map(frozenset, opens))
    if frozenset() not in t or x not in t or any(not s <= x for s in t):
        return False
    return all((a | b in t and a & b in t) for a in t for b in t)

def is_continuous(domain, domain_opens, codomain, codomain_opens, mapping) -> bool:
    if not is_topology(domain, domain_opens) or not is_topology(codomain, codomain_opens):
        raise ValueError('Both collections must be valid finite topologies.')
    if set(mapping) != set(domain) or not set(mapping.values()) <= set(codomain):
        raise ValueError('Mapping must be a total function with the declared codomain.')
    t = set(map(frozenset, domain_opens))
    return all(frozenset(x for x in domain if mapping[x] in u) in t for u in codomain_opens)

def component_labels(adjacency: np.ndarray) -> np.ndarray:
    a = np.asarray(adjacency, dtype=bool)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or not np.array_equal(a, a.T):
        raise ValueError('An undirected square adjacency matrix is required.')
    labels = np.full(len(a), -1, dtype=int)
    next_label = 0
    for start in range(len(a)):
        if labels[start] >= 0:
            continue
        labels[start] = next_label
        stack = [start]
        while stack:
            v = stack.pop()
            for w in np.flatnonzero(a[v]):
                if labels[w] < 0:
                    labels[w] = next_label
                    stack.append(int(w))
        next_label += 1
    return labels
