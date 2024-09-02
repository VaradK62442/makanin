"""
See `matrixSolution.md`.
"""

from typing import List
from pprint import pprint as pp

LETTERS = ["a", "b"]
VARIABLE = "x"
DIAGONAL_SYMBOLS = lambda l_type: ["1"] + [l_type]


class MatrixGenerator:
    """
    Generates all possible n by n diagonal matrices
    """

    def __init__(self, n: int):
        self.n = n

    def _list_to_matrix(self, l: List[str]):
        return [[l[i] if i == j else "0" for i in range(self.n)] for j in range(self.n)]

    def _generate_all_lists(self, letter_type: str, i=0) -> List[List[str]]:
        if i == self.n-1:
            return [[letter_type], ["1"]]
        
        lists = []
        for symbol in DIAGONAL_SYMBOLS(letter_type):
            lists += [[symbol] + l for l in self._generate_all_lists(letter_type, i+1)]

        return lists

    def generate_matrices(self) -> List[List[List[str]]]:
        lists = []
        for l in LETTERS:
            lists += self._generate_all_lists(l)

        return [self._list_to_matrix(l) for l in lists]


def main():
    n = 3
    mg = MatrixGenerator(n)
    pp(mg.generate_matrices())

if __name__ == "__main__":
    main()