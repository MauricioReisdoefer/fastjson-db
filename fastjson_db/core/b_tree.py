from bisect import bisect_left
from typing import Any, List, Optional

class BTreeNode:
    def __init__(self, t: int, leaf: bool = True):
        self.t = t                  # grau mínimo
        self.leaf = leaf            # se é folha
        self.keys: List[Any] = []   # lista de chaves
        self.values: List[List[Any]] = []  # cada chave tem lista de objetos
        self.children: List['BTreeNode'] = []

class BTree:
    def __init__(self, t: int = 3):
        self.root = BTreeNode(t)
        self.t = t

    # ---------------- Inserção ---------------- #
    def insert(self, key: Any, value: Any):
        root = self.root
        if len(root.keys) == (2 * self.t - 1):
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(new_root, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, node: BTreeNode, key: Any, value: Any):
        i = len(node.keys) - 1
        if node.leaf:
            pos = bisect_left(node.keys, key)
            if pos < len(node.keys) and node.keys[pos] == key:
                node.values[pos].append(value)
            else:
                node.keys.insert(pos, key)
                node.values.insert(pos, [value])
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t - 1):
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent: BTreeNode, index: int):
        t = self.t
        node = parent.children[index]
        new_node = BTreeNode(t, leaf=node.leaf)
        parent.keys.insert(index, node.keys[t - 1])
        parent.values.insert(index, node.values[t - 1])
        parent.children.insert(index + 1, new_node)

        new_node.keys = node.keys[t:]
        new_node.values = node.values[t:]
        node.keys = node.keys[:t - 1]
        node.values = node.values[:t - 1]

        if not node.leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]

    # ---------------- Busca ---------------- #
    def search(self, key: Any) -> List[Any]:
        return self._search(self.root, key)

    def _search(self, node: BTreeNode, key: Any) -> List[Any]:
        i = bisect_left(node.keys, key)
        if i < len(node.keys) and node.keys[i] == key:
            return node.values[i]
        elif node.leaf:
            return []
        else:
            return self._search(node.children[i], key)

    # ---------------- Range Search ---------------- #
    def range_search(self, start: Any, end: Any) -> List[Any]:
        result: List[Any] = []
        self._range_search(self.root, start, end, result)
        return result

    def _range_search(self, node: BTreeNode, start: Any, end: Any, result: List[Any]):
        i = 0
        while i < len(node.keys) and node.keys[i] < start:
            i += 1
        while i < len(node.keys) and node.keys[i] <= end:
            if not node.leaf:
                self._range_search(node.children[i], start, end, result)
            result.extend(node.values[i])
            i += 1
        if not node.leaf and i < len(node.children):
            self._range_search(node.children[i], start, end, result)
