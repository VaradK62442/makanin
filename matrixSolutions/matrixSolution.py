"""
See `matrixSolution.md`.
"""

from typing import List

LETTERS = ["a", "b"]
VARIABLE = "x"


class Equation:
    def __init__(self, text_equation: str):
        """
        expecting something of the form 
        `U = V`
        where U and V are words from LETTERS and VARIABLE
        """
        self.U, self.V = text_equation.replace(" ", "").split("=")

    def __str__(self):
        return f"{self.U} = {self.V}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: "Equation"):
        return (self.U == other.U and self.V == other.V) or (self.U == other.V and self.V == other.U)

    def __ne__(self, other: "Equation"):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.U, self.V))


class MatrixSolution:
    def __init__(self, matrix_A: List[List[str]]):
        # assume matrix_A is valid, i.e.
        # - diagonal
        # - all entries are letters or 1
        # - does not contain both a and b

        self.matrix_A = matrix_A
        self.n = len(matrix_A)
        self.diagonals: List[str] = self._get_diagonals()

    def _get_diagonals(self) -> List[str]:
        return [self.matrix_A[i][i] for i in range(self.n)]
    
    def __str__(self) -> str:
        return str(self.matrix_A)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def _get_options(self) -> List[List[tuple[str, str]]]:
        options = []
        for letter in self.diagonals:
            options.append([])
            if letter in LETTERS:
                options[-1].append((letter, VARIABLE))
                options[-1].append((VARIABLE, letter))
                options[-1].append((VARIABLE, VARIABLE))

            elif letter == "1":
                [options[-1].append((let, let)) for let in LETTERS]

        return options
    
    def _add_to_existing_eqn(self, existing_eqn: str, addition_left: str, addition_right: str) -> str:
        # given a string of the form "xyz = abc", this function adds
        # addition_left and addition_right to respective sides
        # and returns the new equation
        left, right = existing_eqn.replace(" ", "").split("=")
        left += addition_left; right += addition_right
        return f"{left} = {right}"
    
    def _count_variable_difference(self, equation: Equation) -> int:
        # count the number of variables in the equation
        return sum([1 for l in equation.U if l == VARIABLE]) - sum([1 for l in equation.V if l == VARIABLE])
    
    def _remove_invalid_equations(self, equations: List["Equation"]) -> List["Equation"]:
        # remove equations that are U = U
        # remove equations that are V = U, where U = V already exists
        new_eqns = []
        for eqn in equations:
            if self._count_variable_difference(eqn) != 0: # want different num of variables
                if eqn.U != eqn.V:
                    if Equation(f"{eqn.V} = {eqn.U}") not in new_eqns:
                        new_eqns.append(eqn)

        return new_eqns
    
    def _get_equations(self, options: List[List[tuple[str, str]]], prefix_eqn="") -> List[str]:
        """ 
        options is a list of list of tuples
        each tuple represents a pair of letters
        the position in the list of options represents the position of the letter in an equation
        i.e. if options[0] = [("a", "x"), ("x", "a")], then
            the equation will be either a... = x... or x... = a...
        
        given this list, this function generates all possible equations
        
        recursive approach
        """        

        if len(options) == 0:
            return [Equation(prefix_eqn)]
        
        equations = []
        for pair in options[0]:
            if prefix_eqn == "": new_eqn = f"{pair[0]} = {pair[1]}"
            else: new_eqn = self._add_to_existing_eqn(prefix_eqn, pair[0], pair[1])
            equations += self._get_equations(options[1:], new_eqn)

        return self._remove_invalid_equations(equations)
    
    def get_possible_equations(self) -> List[str]:
        options = self._get_options()
        equations = self._get_equations(options)
        return equations
    

def main():
    matrix_A = [
        ["a", "0", "0"],
        ["0", "1", "0"],
        ["0", "0", "a"]
    ]

    ms = MatrixSolution(matrix_A)
    print(ms.get_possible_equations())

if __name__ == "__main__":
    main()    