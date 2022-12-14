"""A Newick parser."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Union, cast
import re


def tokenize(tree: str) -> list[str]:
    """
    Extract the tokens from the text representation of a tree.

    >>> tokenize("A")
    ['A']
    >>> tokenize("(A, (B, C))")
    ['(', 'A', '(', 'B', 'C', ')', ')']
    """
    return re.findall(r'[()]|\w+', tree)


@dataclass(repr=False)
class Leaf:
    """
    A leaf in a tree.

    This will just be a string for our application.
    """

    name: str

    def __str__(self) -> str:
        """Simplified text representation."""
        return self.name
    __repr__ = __str__


@dataclass(repr=False)
class Node:
    """An inner node."""

    children: list[Tree]

    def __str__(self) -> str:
        """Simplified text representation."""
        return f"({','.join(str(child) for child in self.children)})"
    __repr__ = __str__


# A tree is either a leaf or an inner node with sub-trees
Tree = Union[Leaf, Node]
Node([Leaf("A"), Node([Leaf("B"), Leaf("C")])])

def parse(tree: str) -> Tree:
    """
    Parse a string into a tree.

    >>> parse("(A, (B, C))")
    (A,(B,C))
    """
    stack = list()
    for el in tokenize(tree):
        match el:
            case "(":
                stack.append(el)
            case ")":
                new_tree = list()
                leaf= stack.pop()
                while leaf != "(":
                    new_tree.append(leaf)
                    leaf= stack.pop()
                new_tree.reverse()
                stack.append(Node(new_tree))
            case _:
                stack.append(Leaf(el))
    return stack.pop()

